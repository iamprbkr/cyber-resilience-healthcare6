# Contributing

Thanks for helping make the Cyber Resilience Index (CRI) better.

This repository is the reproducibility package for the book chapter
*Cyber Resilience in Healthcare 6.0*. The instrument is proposed rather than
validated, so constructive change is welcome: sharper anchors, better decision
rules, additional language translations, or evidence that recalibrates the
weights and cut-points.

## Ways to contribute

- **Report a problem.** Open an issue describing the file, the expected
  behaviour, and what you observed.
- **Improve the instrument.** Propose a change to an anchor, the evidence
  rule, the floor rule, or the maturity mapping, with a rationale.
- **Add a translation** of the instrument and codebook to another language.
- **Improve the code.** Keep the implementation dependency-free and keep the
  tests passing.

## Ground rules

1. **Do not change the worked example** without also updating the chapter and
   the sensitivity claim, or the numbers will no longer reproduce.
2. **Keep every change evidence-linked.** Any new indicator or control must
   trace to a cited, verifiable source.
3. **Do not weaken the evidence gate or the floor rule** silently; these are
   the parts of the instrument that keep it honest.
4. **No credentials, contact details, or personal information** belong in this
   repository. Never commit tokens, keys, emails, or addresses.

## Pull requests

1. Fork the repository and create a branch.
2. Make a focused change; one concern per pull request.
3. Run the test suite (`python code/test_score_cri.py`) and keep it green.
4. Update the relevant documentation (README, codebook, or a doc under `docs/`).
5. Open a pull request explaining what changed and why.

## Scope

This repository covers the instrument and its reproducibility materials only.
The manuscript itself is not maintained here.
