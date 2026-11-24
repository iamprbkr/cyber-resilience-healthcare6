# Reproducibility

Every number in Section 3 of the chapter can be reproduced from this
repository with no third-party dependencies.

## The worked example

The chapter scores a synthetic hospital:

| Pillar | Scores | Mean |
|--------|--------|------|
| Governance | Q1=2, Q2=1, Q3=1, Q4=2 | 1.5 |
| Workforce | Q5=1, Q6=1, Q7=2, Q8=1 | 1.25 |
| Technology | Q9=1, Q10=1, Q11=2, Q12=1 | 1.25 |

Reproduce it:

```bash
cd code
python test_score_cri.py
python score_cri.py --csv worked_example.csv
```

Expected:

```
Composite: 1.3375      (the chapter rounds this to 1.34)
Maturity level: 2
Sensitivity (0.10 weight shift): 0.0250
```

The composite is `(1.5 × 0.35) + (1.25 × 0.30) + (1.25 × 0.35) = 1.3375`.

## The sensitivity claim

The chapter states that moving 0.10 of weight between any two pillars changes
the composite by no more than 0.1 points for a hospital whose pillar scores sit
within one point of one another. The bound follows from the arithmetic: the
maximum change is the weight shift (0.10) times the largest pillar spread
(<= 1.0), so it is at most 0.1. `score_cri.py` computes the exact value for any
given hospital; the worked example yields 0.025.

## The floor rule

`test_score_cri.py` checks the non-compensatory rule: a hospital that scores 5
on every indicator except a 0 on backups (Q11) has a composite above 4.0 but is
capped at Level 2, because the floor rule forbids averaging a fatal gap away.

## The instrument

`instrument/cri_instrument.csv` is the single source of truth for the anchors,
the harm each indicator guards against, the evidence required for a 5, and the
source DOI. The chapter's Table 4 and this file must stay in agreement.

## References

`references/references.bib` and `references/references.ris` list the 25 cited
sources with DOIs. The chapter's citation order is first-use; the BibTeX keys
match the keys used in the manuscript.
