#!/usr/bin/env python3
"""Verified test cases for score_cri.py. Run with: python test_score_cri.py

The cases below check the arithmetic used in the book chapter, the
non-compensatory floor rule, the maturity cut-points, the sensitivity bound,
and a second scoring profile chosen to show that the instrument is portable
across settings (no country-specific data is used).
"""

from score_cri import (
    ALL_QUESTIONS,
    WEIGHTS,
    composite,
    maturity_level,
    pillar_means,
    sensitivity,
)

WORKED = dict(zip(ALL_QUESTIONS, [2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1]))

# A second, deliberately different profile: G=3, W=2, T=4.
# 3*0.35 + 2*0.30 + 4*0.35 = 1.05 + 0.60 + 1.40 = 3.05 -> Level 4.
CROSS_SETTING = dict(
    zip(ALL_QUESTIONS, [3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4])
)


def close(a, b, tol=1e-9):
    return abs(a - b) < tol


def test_weights_sum_to_one():
    assert close(sum(WEIGHTS.values()), 1.0)
    assert WEIGHTS == {"Governance": 0.35, "Workforce": 0.30, "Technology": 0.35}


def test_pillar_means():
    means = pillar_means(WORKED)
    assert close(means["Governance"], 1.5)
    assert close(means["Workforce"], 1.25)
    assert close(means["Technology"], 1.25)


def test_worked_example_composite_exact():
    # Chapter: 0.525 + 0.375 + 0.4375 = 1.3375, reported as 1.34.
    assert close(composite(WORKED), 1.3375)
    assert close(round(composite(WORKED), 2), 1.34)


def test_worked_example_level():
    assert maturity_level(composite(WORKED), WORKED) == 2


def test_sensitivity_exact_value():
    # Pillar spread 0.25; a 0.10 shift moves the composite by at most 0.025.
    assert close(sensitivity(WORKED), 0.025)
    assert sensitivity(WORKED) < 0.1


def test_floor_rule_for_every_indicator():
    # A zero on ANY indicator caps the hospital at Level 2, even when the
    # weighted average would put it in Level 5.
    for q in ALL_QUESTIONS:
        scores = {key: 5 for key in ALL_QUESTIONS}
        scores[q] = 0
        assert composite(scores) > 4.0
        assert maturity_level(composite(scores), scores) == 2, q


def test_cutpoint_boundaries():
    # With every indicator at t, the weighted composite is exactly t.
    cases = [
        (0.99, 1), (1.0, 2), (1.99, 2), (2.0, 3),
        (2.99, 3), (3.0, 4), (3.99, 4), (4.0, 5),
    ]
    for t, expected in cases:
        scores = {q: t for q in ALL_QUESTIONS}
        assert close(composite(scores), t)
        assert maturity_level(composite(scores), scores) == expected, t


def test_cross_setting_profile():
    means = pillar_means(CROSS_SETTING)
    assert close(means["Governance"], 3.0)
    assert close(means["Workforce"], 2.0)
    assert close(means["Technology"], 4.0)
    assert close(composite(CROSS_SETTING), 3.05)
    assert maturity_level(composite(CROSS_SETTING), CROSS_SETTING) == 4
    # Spread is 2.0 here, so the bound is 0.20, not 0.10. The chapter's
    # 0.10 bound applies only when pillar means sit within one point.
    assert close(sensitivity(CROSS_SETTING), 0.20)


def test_determinism():
    for _ in range(5):
        assert close(composite(WORKED), 1.3375)
        assert close(sensitivity(WORKED), 0.025)
        assert maturity_level(composite(WORKED), WORKED) == 2


if __name__ == "__main__":
    tests = [
        test_weights_sum_to_one,
        test_pillar_means,
        test_worked_example_composite_exact,
        test_worked_example_level,
        test_sensitivity_exact_value,
        test_floor_rule_for_every_indicator,
        test_cutpoint_boundaries,
        test_cross_setting_profile,
        test_determinism,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"All {len(tests)} tests passed.")
