# Reproducibility

Every number in Section 3 of the chapter can be reproduced from this
repository. The scorer uses only the Python standard library (Python 3.8+).
No network access, credentials or third-party packages are needed. For the
score-to-band map, worked examples and attributed use cases, see
[`CRI-MAP.md`](CRI-MAP.md).

## Environment and commands

```bash
cd code
python test_score_cri.py                 # 9 verified cases
python score_cri.py --csv worked_example.csv
python score_cri.py --scores 3 3 3 3 2 2 2 2 4 4 4 4   # second profile
```

The second command reproduces the chapter's worked example. The third scores a
different profile to show that the calculation is portable across settings;
it uses no country-specific data.

## Verified test cases

| Test | What it verifies | Expected result |
|------|------------------|-----------------|
| `test_weights_sum_to_one` | Weight vector is a proper weighting | 0.35 + 0.30 + 0.35 = 1.0 |
| `test_pillar_means` | Pillar means of the chapter's example | Governance 1.50, Workforce 1.25, Technology 1.25 |
| `test_worked_example_composite_exact` | Weighted composite and its rounded form | 1.3375, reported as 1.34 |
| `test_worked_example_level` | Band assignment of that composite | Level 2 |
| `test_sensitivity_exact_value` | Exact sensitivity, not just an inequality | 0.025, below the chapter's 0.10 bound |
| `test_floor_rule_for_every_indicator` | Floor rule for each of Q1–Q12 (12 cases) | Composite > 4.0 but level capped at 2 |
| `test_cutpoint_boundaries` | All eight band edges, including exact equality (8 cases) | 0.99→1, 1.0→2, 1.99→2, 2.0→3, 2.99→3, 3.0→4, 3.99→4, 4.0→5 |
| `test_cross_setting_profile` | A different scoring profile, G=3 W=2 T=4 | Composite 3.05, Level 4, sensitivity 0.20 |
| `test_determinism` | Five repeated runs give identical results | Same composite, level and sensitivity each time |

The boundary test caught a floating-point drift at exactly 1.0. The scorer now
compares cut-points with a tolerance of `1e-12`, so a hospital at an exact
boundary lands in the correct band.

## The worked calculations

**Chapter example.** Governance 1.5, Workforce 1.25, Technology 1.25:

```
(1.5 x 0.35) + (1.25 x 0.30) + (1.25 x 0.35)
= 0.525 + 0.375 + 0.4375 = 1.3375  ->  reported as 1.34, Level 2
```

The pillar spread is 0.25, so moving 0.10 of weight between any two pillars
changes the composite by at most `0.10 x 0.25 = 0.025`.

**Second profile, for cross-setting use.** Governance 3, Workforce 2,
Technology 4:

```
(3 x 0.35) + (2 x 0.30) + (4 x 0.35)
= 1.05 + 0.60 + 1.40 = 3.05  ->  Level 4
```

Here the pillar spread is 2.0, so the same 0.10 weight shift changes the
composite by up to 0.20, not 0.10. The chapter's 0.10 bound therefore applies
only when pillar means sit within one point of one another. Stating the
condition is part of the reproducibility package: the sensitivity claim is not
universal, and a reader should know that.

## The floor rule

`test_floor_rule_for_every_indicator` checks all twelve positions, not only
backups. A hospital scoring 5 on every indicator except one zero has a
composite above 4.0 but is capped at Level 2. The zero is the priority for
remediation regardless of the average.

## The instrument

`instrument/cri_instrument.csv` is the single source of truth for the anchors,
the harm each indicator guards against, the evidence required for a 5, and the
source DOI or stable URL. The chapter's Table 4 and this file must stay in
agreement.

## Identifier verification

The 27 DOI strings in the reference list were checked against Crossref.
Twenty-five resolve there. The two ENISA reports use DOIs issued by the EU
Publications Office (`10.2824/163953` and `10.2824/397622`); they are not
indexed in the Crossref or DataCite APIs, but both resolve through `doi.org`
to their official `op.europa.eu` publication records. Those two entries carry
both the DOI and the stable URL in the BibTeX and RIS files so a reader is never
dependent on a single resolver. The three institutional sources without DOIs
carry stable URLs or a WHO document number.

## What is verified, and what is not

**Verified here:** arithmetic, band edges, floor rule, sensitivity bound and
its condition, determinism, and agreement between the scorer and the worked
example.

**Not verified by any code:** that 0.35/0.30/0.35 are optimal weights, that
1.0/2.0/3.0/4.0 are the right cut-points against real outcomes, or that two
human raters will agree. The codebook requires a weighted kappa of at least
0.70 before a score is treated as reliable, and prospective validation against
incident outcomes remains the single most valuable next study. Reproducing the
arithmetic is not the same as validating the instrument.

## References

`references/references.bib` and `references/references.ris` list the 30 cited
sources. Peer-reviewed entries carry DOIs; institutional reports carry a DOI
where one was assigned and a stable URL otherwise. The chapter's citation order
is first-use; the BibTeX keys match the keys used in the manuscript.
