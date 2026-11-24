# CRI Codebook and Rater Training

This codebook defines the twelve Cyber Resilience Index (CRI) indicators and
the decision rules a rater applies when scoring a hospital. Its purpose is to
make the scoring reproducible and, eventually, reliable between raters.

## Scoring scale

Each indicator is scored on the behavioural anchors in `cri_instrument.csv`:

- **0** — the safeguard is absent.
- **3** — the safeguard exists on paper (documented but not demonstrated).
- **5** — the safeguard is demonstrated and evidence-gated.

Scores of 1, 2, and 4 are permitted as intermediate judgements and follow the
same logic: a score above 3 means the hospital can point to something it *did*,
not something it *wrote*.

## Evidence rule (non-negotiable)

A score of **5** requires a named artefact: a dated drill log, a contract
clause, a restoration record, a trended dashboard, or equivalent. If the rater
cannot be shown the artefact, the score is at most 3. This rule exists to
reduce the self-report bias that otherwise inflates self-assessment.

## Floor rule (non-compensatory)

Any indicator scored **0** caps the hospital's maturity at **Level 2**, no
matter how high the composite average is. One missing safeguard — untested
backups, no reporting mechanism, no device inventory — can be fatal on its own,
so it must not be averaged away.

## Maturity mapping

| Band | Level | Meaning |
|------|-------|---------|
| < 1.0 | 1 Ad hoc | No policy, no training, no controls |
| 1.0–1.99 | 2 Compliance | Audit-driven policy; plans exist but cannot be executed |
| 2.0–2.99 | 3 Integrated | Domains connected; care continues for under four hours |
| 3.0–3.99 | 4 Proactive | Early detection; safe care through an incident |
| >= 4.0 | 5 Adaptive | Dynamic governance; recovery without heroics |

The floor rule overrides this table: a hospital with any indicator at 0 cannot
be rated above Level 2.

## Rater training protocol

1. Both raters read this codebook and the anchors in `cri_instrument.csv`.
2. Raters score the same synthetic hospital (start with `worked_example.csv`)
   and reconcile any disagreement against the anchors before scoring real data.
3. Raters score a calibration set of at least five hospitals independently.
4. Agreement is computed as a weighted kappa across the twelve indicators.
   The score is treated as reliable only when the weighted kappa reaches 0.70.

## Change control

The weights (0.35 / 0.30 / 0.35) and cut-points are author-set priors, not
measured optima. Any future change should be versioned here and accompanied by
a re-run of the sensitivity sweep in `score_cri.py`.
