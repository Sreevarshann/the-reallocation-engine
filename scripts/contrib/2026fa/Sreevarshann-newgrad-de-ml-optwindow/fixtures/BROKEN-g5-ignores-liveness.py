"""BROKEN mutant, for the test suite only. Never import from production code.

A G5 evidence check that forgets the liveness gate: a role with no posting check
passes as scoreable. The scorer would then default liveness to 1.0 (open) and
label it "record" (role-scorer.mjs lines 83-87). tests/test_core.py proves the
suite catches this mutant.
"""
import core

REQUIRED_WITHOUT_LIVENESS = [r for r in core.REQUIRED_EVIDENCE if r[0] != "liveness"]


def evidence_problems(role):
    return core.evidence_problems(role, required=REQUIRED_WITHOUT_LIVENESS)
