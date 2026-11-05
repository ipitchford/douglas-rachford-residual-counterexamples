# Verification scope and commands

Core replay is standard-library Python. Run `python3 -B run_checks.py` and `python3 -B -O run_checks.py`; each reconstructs four exact implementations, compares their stored rational outputs, makes five cross-comparisons and checks 360 finite schedule identities. Logs are exclusive timestamped records. Producer revision replays passed both modes; they are not external reproduction.

Run `python3 -B actual_vector_series.py` for degree-two rational polynomial algebra. It checks the actual vector used by Appendix A, not just an extremal singular value. Analytic remainder and active-set continuity are separate written-proof obligations.

Run `python3 -B test_checker_guards.py --out NEW_DIRECTORY`. The retained checker-repair-specific-20261105/receipt.json records 24 expected outcomes across normal and optimized execution. Invalid witnesses and focused terminal/final-vector mutations are rejected by explicit scientific exceptions; positive output bytes agree across modes. The source/log hashes were verified by the coordinator. No finite mutation set proves all faults detectable.

`optimisation_series_check.py` is an optional SymPy cross-check. It was run in both modes during revision, reproducing the stated coefficients. It is not required to establish the exact rational counterexamples. The public research CI exercises standard-library paths; fresh-extraction publication checks are retained in the publication record.

Neither the finite schedule set nor numerical graphs establish universal minimax statements. Read the manuscript proofs and the precisely located external theorem dependencies. No formal proof assistant, unaffiliated replication, statistical experiment or practical performance trial is claimed.
