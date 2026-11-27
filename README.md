# Cyber Resilience Index for Healthcare 6.0

A reproducible, clinically scored instrument for measuring whether a hospital
can keep treating patients while its systems are under attack or offline.

This repository is the **reproducibility package** for the book chapter
*Cyber Resilience in Healthcare 6.0: Connecting Governance, Workforce, and
Technology* (IntechOpen). It contains the instrument, the scoring
implementation, and everything needed to reproduce every number in the
chapter. The manuscript itself is **not** part of this repository.

---

## What the CRI measures

Healthcare security metrics (firewall rules, patch rates, training hours) tell
the security team it is busy. They do not tell the board whether the hospital
can treat patients through an attack. The Cyber Resilience Index (CRI) closes
that gap by scoring **observable capability** on a 0–5 scale, where the score
expresses *what the hospital does*, never *what its policy claims*.

```
CRI = 0.35 × Governance  +  0.30 × Workforce  +  0.35 × Technology
```

Each pillar is the mean of four indicators:

| Pillar | Indicators |
|--------|-----------|
| Governance | Q1 decision authority · Q2 vendor tiering · Q3 tabletop exercises · Q4 board framing |
| Workforce | Q5 role-specific training · Q6 downtime procedures · Q7 reporting · Q8 readiness by behaviour |
| Technology | Q9 IoMT inventory/segmentation · Q10 AI-assisted detection · Q11 tested backups · Q12 zero trust |

### Three scoring rules that matter

1. **Evidence gate.** A score of 5 requires a named artefact (a drill log, a
   contract clause, a restoration record) — never an assertion alone.
2. **Non-compensatory floor.** Any indicator scored 0 caps the hospital at
   maturity Level 2, because one missing safeguard can be fatal regardless of
   the average.
3. **Maturity bands.** < 1.0 = Level 1 (Ad hoc); 1.0–1.99 = Level 2
   (Compliance); 2.0–2.99 = Level 3 (Integrated); 3.0–3.99 = Level 4
   (Proactive); ≥ 4.0 = Level 5 (Adaptive).

The weights are **author-set priors**, not measured optima. The scorer reports
the sensitivity of the composite to a 0.10 shift in any weight so the result is
honest about that choice.

---

## Positioning for global use

This instrument is designed to travel across jurisdictions without carrying one
country's statistics or legal calendar with it.

- **Behaviour, not paperwork.** Every anchor asks what the hospital *does*; a
  score of 5 needs a named artefact. The twelve questions are language-neutral
  and do not depend on a named national framework.
- **No country-specific data points.** The chapter's figures are EU-wide,
  multinational, or from a global tracker. This repository contains no national
  incidence table, and none is needed to score a hospital.
- **Gates, not a fixed calendar.** The Safe-Care Resilience Readiness Cycle ends
  each phase when its evidence exists, not after a set number of days. NIS2,
  GDPR and other statutory clocks appear in the chapter as examples of local
  duties a hospital must map; they are not built into the score.
- **Honest priors.** The 0.35/0.30/0.35 weights are author-set priors. The
  scorer reports sensitivity so a board can see how much the result depends on
  that choice. Cut-points and dashboard thresholds are defaults to reset against
  local clinical tolerance.
- **Proposed, not validated.** The package exists so that anyone can test,
  translate or challenge the instrument. Field validation against incident
  outcomes is the next study, not a claim made here.

---

## Repository structure

```
.
├── instrument/              The twelve indicators, anchors, codebook, and checklist
│   ├── cri_instrument.csv
│   ├── cri_schema.json
│   ├── codebook.md
│   └── reporting_checklist.md
├── code/                    The scoring implementation and its tests
│   ├── score_cri.py
│   ├── test_score_cri.py
│   └── worked_example.csv
├── references/              The 30 cited sources, with DOIs or stable URLs, in two formats
│   ├── references.bib
│   └── references.ris
├── docs/
│   ├── USAGE.md             How to run, score, and interpret the CRI
│   ├── CRI-MAP.md           Score bands, four worked examples, use cases and 2026 attributions
│   └── REPRODUCIBILITY.md   How to reproduce every number in the chapter
├── CONTRIBUTING.md
├── CITATION.cff
├── LICENSE                  Apache License 2.0
└── README.md
```

---

## Quick start

```bash
git clone <repository-url>
cd cyber-resilience-healthcare6/code

# Run the 9 verified test cases (worked example, floor rule, cut-points,
# sensitivity, cross-setting profile and determinism)
python test_score_cri.py

# Score the worked example
python score_cri.py --csv worked_example.csv
```

Expected output:

```
Pillar means:
  Governance    1.50
  Workforce     1.25
  Technology    1.25
Composite: 1.3375
Maturity level: 2
Sensitivity (0.10 weight shift): 0.0250
```

Requires Python 3.8+ with no third-party dependencies.

---

## Usage

See [`docs/USAGE.md`](docs/USAGE.md) for the full guide: how to score a real
hospital, what evidence a score of 5 requires, how to apply the floor rule, and
how to interpret a maturity level. See [`docs/CRI-MAP.md`](docs/CRI-MAP.md) for
the score-to-band map, four worked examples, the use cases for each stakeholder,
and the 2026 sources attributed to each claim. See
[`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) to reproduce every figure
and table in the chapter's Section 3.

## Instrument

The twelve indicators and their 0/3/5 behavioural anchors are in
[`instrument/cri_instrument.csv`](instrument/cri_instrument.csv), with a
machine-readable response schema in
[`instrument/cri_schema.json`](instrument/cri_schema.json). The codebook
([`instrument/codebook.md`](instrument/codebook.md)) defines the decision rules
and the rater-training protocol (a weighted kappa of 0.70 before the score is
treated as reliable).

## License

Apache License 2.0 — see [`LICENSE`](LICENSE).

## Citation

Cite this package with the metadata in [`CITATION.cff`](CITATION.cff), or in
BibTeX:

```bibtex
@misc{damor2026cri,
  author       = {Prabhakar Damor},
  title        = {Cyber Resilience Index for Healthcare 6.0: Instrument, codebook, and scoring code},
  year         = {2026},
  version      = {1.1.0},
  license      = {Apache-2.0},
  note         = {Reproducibility package for the IntechOpen book chapter of the same name}
}
```

## Contributing

Bug reports, instrument refinements, and new language translations are welcome.
See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Status and limits

The CRI is **proposed, not validated**. Its weights, cut-points, and cycle
gates are stated defaults; its propositions are stated with the conditions
that would falsify them. Prospective validation against real incident outcomes
is the single most valuable next study. This repository exists so that work can
be done by anyone, without the authors in the room.
