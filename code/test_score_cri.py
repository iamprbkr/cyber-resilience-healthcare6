#!/usr/bin/env python3
"""Tests for score_cri.py. Run with: python test_score_cri.py"""

from score_cri import composite, maturity_level, sensitivity, pillar_means

WORKED = dict(zip(
    [f"Q{k}" for k in range(1, 13)],
    [2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1],
))


def test_pillar_means():
    means = pillar_means(WORKED)
    assert abs(means["Governance"] - 1.5) < 1e-9
    assert abs(means["Workforce"] - 1.25) < 1e-9
    assert abs(means["Technology"] - 1.25) < 1e-9


def test_worked_example_composite():
    # Chapter reports 0.525 + 0.375 + 0.4375 = 1.34 (rounded).
    assert abs(composite(WORKED) - 1.3375) < 1e-9


def test_worked_example_level():
    score = composite(WORKED)
    assert maturity_level(score, WORKED) == 2


def test_floor_rule_caps_level():
    all_five = {f"Q{k}": 5 for k in range(1, 13)}
    all_five["Q11"] = 0  # untested backups: a fatal gap
    score = composite(all_five)
    assert score > 4.0                       # high by the average ...
    assert maturity_level(score, all_five) == 2  # ... but capped by the floor


def test_sensitivity_within_bounds():
    # Pillar spread is 0.25, so a 0.10 weight shift moves at most 0.025.
    assert sensitivity(WORKED) < 0.1


if __name__ == "__main__":
    test_pillar_means()
    test_worked_example_composite()
    test_worked_example_level()
    test_floor_rule_caps_level()
    test_sensitivity_within_bounds()
    print("All tests passed.")
