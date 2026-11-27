# CRI score map, worked examples and use cases

This document maps a CRI composite to a maturity band, shows the arithmetic
that produces it, and names the use case and the 2026 evidence behind each
interpretation. It is written for a global audience: no national incidence
table is used, no statutory clock is assumed to be universal, and every figure
is attributed to a named source with its observation window.

The bands are **proposed design levels**, not empirically calibrated cut-points.
The 2026 sources anchor the *failure mechanisms and the practice of rehearsal*;
they do not validate the bands against outcomes.

---

## 1. The score map

`CRI = 0.35 x Governance + 0.30 x Workforce + 0.35 x Technology`, each pillar
being the mean of four indicators scored 0–5. Any indicator at 0 caps the
hospital at Level 2.

| Level | Composite | What the hospital can do | 2026 evidence that anchors the level | What that evidence does **not** show |
|-------|-----------|--------------------------|--------------------------------------|--------------------------------------|
| **1 — Ad hoc** | < 1.0 | Cannot maintain care through an attack; no charter, no drills, unmapped devices | ENISA's health landscape reports that 46% of surveyed health organisations had never performed a risk analysis and 40% had no awareness programme for non-IT staff (ENISA 2023) | That a particular hospital is at Level 1; the figures are EU-wide survey data |
| **2 — Compliance** | 1.0–1.99 | A plan exists on paper but cannot be executed; annual video, perimeter defence | 95% of surveyed health organisations faced difficulty with risk assessment, and only 27% had a dedicated ransomware defence programme (ENISA 2023) | That documents are absent; the problem is untested capability |
| **3 — Integrated** | 2.0–2.99 | Limited care continued for less than four hours; role drills and device segmentation in place | Health-ISAC recorded 317 ransomware events affecting the global health sector in Q3 2026, the highest quarter in its series (189, 190, 213, 317) (Health-ISAC 2026) | That a Level 3 hospital survives every incident; the tracker measures events, not outcomes |
| **4 — Proactive** | 3.0–3.99 | Safe care maintained through an incident; board reporting in clinical terms and early detection | Cyber Europe 2022 involved 918 registered participants from 27 EU member states and two EFTA countries and concluded that frequent local testing is needed; a radiotherapy department restarted treatment in three days and accounted for dose for a year (Cases 2026; Peters 2026) | That rehearsal alone causes good outcomes; the case is one department |
| **5 — Adaptive** | ≥ 4.0 | Dynamic governance and a safety culture; recovery without heroics | Design target aligned with the resilience capacities in the validated RHCA instrument (Ellis 2026) | No 2026 dataset demonstrates a Level 5 hospital; this band is a goal, not an observation |

For contrast, WHO Europe's 2025 instrument scores maturity by the **share of
elements in place** (below 60%, 60–70%, 70–90%, 90% or more). It audits
completeness; the CRI scores behaviour under pressure with a non-compensatory
floor. The two are not interchangeable.

---

## 2. Worked examples

All four are reproducible with `python code/score_cri.py`.

### Example A — the chapter's hospital (hypothetical)

Quarter scores: G = (2+1+1+2)/4 = 1.50, W = (1+1+2+1)/4 = 1.25,
T = (1+1+2+1)/4 = 1.25.

```
(1.50 x 0.35) + (1.25 x 0.30) + (1.25 x 0.35)
= 0.525 + 0.375 + 0.4375 = 1.3375  ->  1.34, Level 2
Sensitivity at a 0.10 weight shift: 0.025 (spread 0.25)
```

`python code/score_cri.py --csv code/worked_example.csv`

Use case: a board asking whether its documented plan is executable. Level 2
with a low sensitivity means the conclusion is robust to the choice of weights.

### Example B — a different profile, cross-setting (hypothetical)

G = 3.00, W = 2.00, T = 4.00.

```
(3 x 0.35) + (2 x 0.30) + (4 x 0.35)
= 1.05 + 0.60 + 1.40 = 3.05  ->  Level 4
Sensitivity at a 0.10 weight shift: 0.20 (spread 2.0)
```

`python code/score_cri.py --scores 3 3 3 3 2 2 2 2 4 4 4 4`

This example exists to show the **condition** on the chapter's sensitivity
claim: 0.10 is the bound only when pillar means sit within one point of one
another. Here they do not, and the bound is 0.20. Publishing both examples is
how the package stays honest with global readers.

### Example C — the floor rule (hypothetical)

Every indicator scored 5 except Q11 (tested backup restoration) scored 0.

```
G = 5.00, W = 5.00, T = (5+5+0+5)/4 = 3.75
Composite = 1.75 + 1.50 + 1.3125 = 4.5625
Raw band = Level 5, but floor rule caps at Level 2
```

`python code/score_cri.py --scores 5 5 5 5 5 5 5 5 5 5 0 5`

Use case: a hospital that has strong governance, training and detection but has
never restored a backup. The average cannot hide the fatal gap. The floor rule
is tested for all twelve positions, not only Q11.

### Example D — a 2026-threat-pattern profile (hypothetical)

Low Q7 (incident reporting known by all) and Q12 (Zero Trust for clinical
systems) reflect the credential-phishing pattern Health-ISAC described in Q3
2026: look-alike single sign-on domains harvesting credentials and unexpected
multi-factor enrolments. G = 2.00, W = (2+3+1+2)/4 = 2.00, T = (3+2+3+1)/4
= 2.25.

```
(2 x 0.35) + (2 x 0.30) + (2.25 x 0.35)
= 0.70 + 0.60 + 0.7875 = 2.0875  ->  Level 3
Sensitivity: 0.025 (spread 0.25)
```

This is a **hypothetical profile**, not a measured hospital. It shows how a
current threat pattern translates into the two indicators that would be
prioritised: Q7 and Q12.

---

## 3. Use cases and attributions

| User | Decision the CRI supports | Indicators | 2026 attribution |
|------|---------------------------|------------|------------------|
| **Board / trustee** | Whether cyber risk is reported in clinical terms and whether recovery is tested | Q4, Q11 | ENISA 2023 notes NIS2 liabilities for top management; WHO Europe 2025 shows how a maturity score can be audited, but by element count rather than behaviour |
| **CISO / security lead** | Which vendors matter and what their contractual recovery time is | Q2, Q12 | ENISA 2023 found supply-chain attacks caused disruption or loss in 7% of health incidents; Health-ISAC 2026 attributes its Q3 surge largely to credential harvesting through look-alike domains |
| **Clinical director** | Whether a ward can work without records, and whether drills cover night and weekend shifts | Q3, Q6 | Cyber Europe 2022 (918 participants, 29 countries) concluded that frequent local testing is needed; Cases 2026 and Peters 2026 document the radiotherapy department that continued treatment |
| **Biomedical engineer** | Which connected devices are inventoried, tiered and segmented | Q9, Q11 | ENISA 2023 reports connected medical devices in 64% of health organisations and calls unsupported devices with no patch path a significant professional challenge |
| **Researcher / auditor** | Whether a score can be reproduced and compared across settings | All twelve, plus sensitivity | Rogge 2026 consolidated 3,459 healthcare incident records from five public international datasets (2021–2024); Health-ISAC 2026 publishes a dated global tracker. Both measure incidents, not CRI scores, and neither validates the index |

---

## 4. What the 2026 data can and cannot support

**Can support.** The problem is current, healthcare-specific and global in
scale: 317 health-sector ransomware events in one quarter (Health-ISAC 2026),
458 tracked health-sector ransomware events in 2024 (Health-ISAC 2025), 3,459
consolidated incident records across four years (Rogge 2026), and EU-wide
prevalence figures (ENISA 2023). Rehearsal is established practice at
cross-border scale (Cyber Europe 2022).

**Cannot support.** None of these datasets contains a CRI score or a hospital
outcome linked to one. They cannot tell us that the weights 0.35/0.30/0.35 are
optimal, that cut-points at 1.0/2.0/3.0/4.0 are correct, or that a given level
causes survival. A ward that recovers quietly does not publish. The CRI remains
proposed, not validated; the codebook's kappa threshold and the call for
prospective validation are the route to that evidence.

---

## 5. Source attributions

- Health Information Sharing and Analysis Center. *Health Sector Heartbeat:
  Cybersecurity Trends and Threats in the Health Sector, Q3 2026*, 21 October
  2026. `https://health-isac.org/health-isac-health-sector-heartbeat-2026-q3/`
- Health Information Sharing and Analysis Center. *2025 Health Sector Cyber
  Threat Landscape*, 14 February 2025.
  `https://health-isac.org/wp-content/uploads/Health-ISAC_2025-Annual-Threat-Report.pdf`
- Rogge G, Bohnet-Joschko S. *Cybersecurity Challenges in Hospitals:
  International Incident Reports Analysis and Expert Validation*. Informatics.
  2026;13(4):54. DOI: `10.3390/informatics13040054`
- European Union Agency for Cybersecurity. *ENISA Threat Landscape: Health
  Sector*, July 2023. DOI: `10.2824/163953`
- European Union Agency for Cybersecurity. *Cyber Europe 2022: After Action
  Report*, December 2022. DOI: `10.2824/397622`
- WHO Regional Office for Europe. *Cybersecurity and Privacy Maturity
  Assessment and Strengthening for Digital Health Information Systems*, 2025.
  Document WHO/EURO:2025-11827-51599-78854
- Cases C et al. *One year after a cyberattack: Lessons learned and dosimetric
  analysis of contingency radiotherapy plans*. IJROBP. 2026;126(2):308–317.
  DOI: `10.1016/j.ijrobp.2026.03.030`
- Peters S et al. *ESTRO framework for radiation oncology departments to
  mitigate against cyberattacks*. Radiotherapy and Oncology. 2026;214:111305.
  DOI: `10.1016/j.radonc.2025.111305`
- Ellis L et al. *Resilience in Healthcare Capacities Assessment (RHCA)*.
  Applied Ergonomics. 2026;135:104768. DOI: `10.1016/j.apergo.2026.104768`
