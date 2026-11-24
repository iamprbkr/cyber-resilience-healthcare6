# Usage

This guide walks through scoring a hospital with the Cyber Resilience Index
(CRI), from reading the anchors to interpreting the maturity level.

## 1. Read the codebook

Start with [`instrument/codebook.md`](../instrument/codebook.md). It defines the
three scoring rules that matter most:

- **Evidence gate** — a score of 5 requires a named artefact, not an assertion.
- **Floor rule** — any indicator at 0 caps the hospital at maturity Level 2.
- **Maturity bands** — < 1.0 (Level 1) to >= 4.0 (Level 5).

## 2. Score the twelve indicators

For each of Q1–Q12 in
[`instrument/cri_instrument.csv`](../instrument/cri_instrument.csv), choose the
anchor (0, 3, or 5) that matches what the hospital *does*. Scores of 1, 2, and 4
are allowed as intermediate judgements. A score above 3 requires the hospital to
show something it did, not something it wrote.

Record the result as a CSV with columns `id,score` (see
[`code/worked_example.csv`](../code/worked_example.csv)), or as a JSON document
valid against [`instrument/cri_schema.json`](../instrument/cri_schema.json).

## 3. Compute the score

```bash
python code/score_cri.py --csv path/to/scores.csv
```

The scorer prints the three pillar means, the weighted composite, the maturity
level, and the sensitivity of the composite to a 0.10 weight shift.

## 4. Interpret the result

- Read the **maturity level** first, then the **composite**.
- If the **floor rule** fired (any indicator at 0), treat that indicator as the
  priority regardless of the composite.
- The **sensitivity** tells you how much the score depends on the author-set
  weights; a small value means the level is robust to that choice.

## 5. Report honestly

Use [`instrument/reporting_checklist.md`](../instrument/reporting_checklist.md)
when you publish a score. Report all twelve indicators, not only the composite,
and state that the index is proposed rather than validated.

## 6. Rater reliability (for research use)

For any use where the score will be treated as evidence, have two independent
raters score the same hospital against the codebook and compute a weighted
kappa. Treat the score as reliable only at kappa >= 0.70.
