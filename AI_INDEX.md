# Evidence index

## Read the result

- [paper.md](paper.md): complete statement, hypotheses, proofs, inherited dependencies and limitations. Propositions 1–2 refute the printed conjecture; Theorem 4 gives the exponent; Theorems 5–6 and Corollary 6.1 have distinct restricted scopes.
- [CLAIMS.json](CLAIMS.json): individual claim boundaries and evidence classes.
- [SOURCES.md](SOURCES.md) and [NOVELTY.md](NOVELTY.md): inspected source passages, contribution comparisons and unresolved full-text overlap.
- [ASSURANCE.md](ASSURANCE.md), [REVISION_RESPONSE.md](REVISION_RESPONSE.md) and [PROVENANCE.md](PROVENANCE.md): internal checking, objections, repairs and validation limits.

## Reproduce bounded checks

- [run_checks.py](run_checks.py): four exact implementations compared with stored baselines and each other. Run normal and optimized Python as documented in README.
- [optimisation_exact_checks.py](optimisation_exact_checks.py) and [independent_exact_verifier.py](independent_exact_verifier.py): rational scalar, rotational and hinge witnesses and finite schedule identities.
- [optimisation_hinge_n9_exact.py](optimisation_hinge_n9_exact.py) and [reviewer_hinge_check.py](reviewer_hinge_check.py): separately implemented nine-evaluation witness checks.
- [actual_vector_series.py](actual_vector_series.py): exact degree-two truncated-series coefficients for the specified initial vector; not analytic remainder proof.
- [test_checker_guards.py](test_checker_guards.py): normal/optimized positive and semantic-negative guard tests.
- [optimisation_series_check.py](optimisation_series_check.py): optional SymPy cross-check; not required for the standard-library replay.
- [RESEARCH_GATES.json](RESEARCH_GATES.json): dated contribution search, limitation triage and extension decisions; structural record, not proof.
- [LICENSES.md](LICENSES.md): component rights.

Do not infer formal verification, global novelty, exact mixed-class constants, objective-value acceleration, or independent external reproduction from successful scripts.
