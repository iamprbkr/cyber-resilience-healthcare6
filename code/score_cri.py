#!/usr/bin/env python3
"""Cyber Resilience Index (CRI) scorer.

Implements the healthcare-specific Cyber Resilience Index described in the
book chapter "Cyber Resilience in Healthcare 6.0" (IntechOpen).

    CRI = 0.35 * G + 0.30 * W + 0.35 * T

where G, W, T are the means of four indicators each, scored 0-5 against
behavioural anchors:

    Governance  : Q1-Q4
    Workforce   : Q5-Q8
    Technology  : Q9-Q12

Scoring rules (as stated in the chapter):
  * A score of 5 is evidence-gated: it requires a named artefact (a drill log,
    a contract clause, or a restoration record), never an assertion alone.
  * Non-compensatory floor: any indicator scored 0 caps maturity at Level 2,
    because one missing safeguard can be fatal regardless of the average.
  * Maturity cut-points: 1.0, 2.0, 3.0, 4.0.

The weights are author-set priors, so the scorer also reports the sensitivity
of the composite to a 0.10 reallocation of weight between any two pillars.

Usage:
    python score_cri.py --scores 2 1 1 2 1 1 2 1 1 1 2 1
    python score_cri.py --csv worked_example.csv
"""

import argparse
import csv
import sys

PILLARS = {
    "Governance": ["Q1", "Q2", "Q3", "Q4"],
    "Workforce": ["Q5", "Q6", "Q7", "Q8"],
    "Technology": ["Q9", "Q10", "Q11", "Q12"],
}
WEIGHTS = {"Governance": 0.35, "Workforce": 0.30, "Technology": 0.35}
# Level bands: <1.0 -> 1; 1.0-1.99 -> 2; 2.0-2.99 -> 3; 3.0-3.99 -> 4; >=4.0 -> 5.
CUTPOINTS = [(1.0, 2), (2.0, 3), (3.0, 4), (4.0, 5)]
EPS = 1e-12  # guard against float drift at an exact cut-point
ALL_QUESTIONS = [q for qs in PILLARS.values() for q in qs]


def pillar_means(scores):
    """Return {pillar: mean} from a dict of Q1..Q12 -> float."""
    return {p: sum(scores[q] for q in qs) / len(qs) for p, qs in PILLARS.items()}


def composite(scores):
    """Weighted composite score (0-5)."""
    means = pillar_means(scores)
    return sum(WEIGHTS[p] * means[p] for p in WEIGHTS)


def _raw_level(score):
    # Default to Level 1 (Ad hoc); each cut-point raises the band.
    level = 1
    for bound, lvl in CUTPOINTS:
        if score + EPS >= bound:
            level = lvl
    return level


def maturity_level(score, scores):
    """Maturity level with the non-compensatory floor rule applied."""
    if any(scores[q] == 0 for q in scores):
        return min(2, _raw_level(score))
    return _raw_level(score)


def sensitivity(scores, step=0.10):
    """Maximum |change| in the composite when `step` weight is moved between
    any two pillars (sum of weights held at 1)."""
    means = pillar_means(scores)
    pillars = list(WEIGHTS)
    max_delta = 0.0
    for i in range(len(pillars)):
        for j in range(len(pillars)):
            if i == j:
                continue
            delta = step * (means[pillars[i]] - means[pillars[j]])
            max_delta = max(max_delta, abs(delta))
    return max_delta


def report(scores):
    means = pillar_means(scores)
    score = composite(scores)
    level = maturity_level(score, scores)
    sens = sensitivity(scores)
    print("Pillar means:")
    for p, m in means.items():
        print(f"  {p:<12} {m:.2f}")
    print(f"Composite: {score:.4f}")
    print(f"Maturity level: {level}")
    print(f"Sensitivity (0.10 weight shift): {sens:.4f}")
    return score, level, sens


def load_csv(path):
    scores = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            q = row["id"].strip()
            scores[q] = float(row["score"])
    return scores


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scores", nargs=12, type=float, metavar="Q",
                       help="12 scores for Q1..Q12, in order")
    group.add_argument("--csv", help="CSV with columns id,score")
    args = parser.parse_args(argv)

    if args.csv:
        scores = load_csv(args.csv)
    else:
        scores = dict(zip(ALL_QUESTIONS, args.scores))
    report(scores)


if __name__ == "__main__":
    main(sys.argv[1:])
