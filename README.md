# Douglas–Rachford residual counterexamples

**Author:** Anonymous. **Revision date:** 5 November 2026. **Status:** unrefereed, AI-assisted research candidate.

This package corrects a particular fixed-point residual guarantee, not the practical speed of every splitting solver. Exact scalar and planar examples refute Conjecture 3.5 of Abbaszadehpeivasti and Zamani, arXiv:2509.06676v2. For each fixed admissible parameter triple, the uniform worst-case squared residual has order 1/N, rather than the proposed 1/N². A fixed witness can still converge geometrically: the lower-bound family varies with the horizon.

## Reading route

- `paper.md` and `paper.pdf`: standalone argument, scope table, hypotheses and bibliography.
- `CLAIMS.json`: claim-by-claim evidence and limitations.
- `ASSURANCE.md`: scientific checking and source-access boundaries.
- `REVISION_RESPONSE.md`: substantive objections and their disposition.
- `VERIFICATION.md` and retained replay records: executable commands and actual outcomes.

## Scope

The prescribed-schedule envelope concerns linear B with A=0. The adaptive minimax theorem permits arbitrary real multiples of the current residual, returns the last iterate, and measures its unrelaxed residual. Its optimal scalar can exceed the conventional DRS interval. The conventional-range corollary is a **linear A=0 minimax infimum only**, not attained by an admissible policy. Anchoring, inertia, matrix steps and extrapolated output lie outside the policy class.

The sharp proximal-point upper constant, contraction polynomial inequality and rotation product have acknowledged antecedents. He et al. (2021) full-text overlap remains unknown after lawful access attempts. No historical-priority claim is made for the minimax synthesis or its elementary corollary. The source's objective-value Conjectures 5.1, 5.6 and 5.7 remain unresolved here.

## Replay

From a fresh extraction, using Python 3:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B run_checks.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -O run_checks.py
```

The exact certificate path uses standard-library rational arithmetic. Filenames containing “independent” identify separately authored implementations within this coordinated producer workflow, not unaffiliated reproduction. Finite agreement does not prove universal quantifiers.

`checker-repair-specific-20261105/receipt.json` records 24 passing expected outcomes in normal and optimized execution, exact positive-output agreement, an actual-vector appendix series fixture and guard probes for its bound source snapshot. Focused terminal-equality and final-vector mutants require the intended scientific error messages. All retained source and output hashes were checked. Later source changes require fresh checks; these bounded tests are not universal checker validation.

The optional symbolic script requires SymPy. Exploratory search/performance-estimation scripts are excluded from this public export because they are not necessary for the elementary refutations. Numerical agreement with other conjectures is not proof.

## Rebuilding and integrity

`build_figure.py` requires NumPy and Matplotlib. The manuscript was built using Pandoc and pdfLaTeX with `tex_header.tex`: `pandoc paper.md --standalone --include-in-header tex_header.tex -o paper.tex`, followed by two runs of `pdflatex -interaction=nonstopmode -halt-on-error paper.tex`. The figure illustrates exact formulas; no strict inequality depends on plotted floating-point values.

The final manifest binds file bytes, not correctness. AI-assisted internal review and implementation diversity are not external peer review or independent reproduction. No proof-assistant formalisation or practical performance impact is claimed.
