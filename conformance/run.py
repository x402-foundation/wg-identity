"""Run the RFC 9421 agent-identity cases against a verifier and report each case.

    python conformance/run.py                          # the reference verifier from requirements.txt
    python conformance/run.py --verifier "CMD ARGS"    # your verifier
    python conformance/run.py --write cases.json       # write the case inputs for your own tooling

Each case is a request (method, URL, body, header lines) and the credentials that came with it. The
answer is either accepted (the identity of who acts for whom is established) or refused with a reason
code. The reference answers are pinned twice: the digest of the full case file in cases.sha256, and the
refusal code of every refused case in the package's own table.

--verifier runs CMD with the path of a JSON file of case inputs (no answers) as its last argument. CMD
prints one JSON object to stdout mapping case id to one of the four outcomes of RFP 4.4.1: "verified",
"contradicted", "indeterminate" or "not_evaluated". A case it leaves out counts as not_evaluated. A
case agrees when an accepted case is "verified" and a refused case is "contradicted"; the reason codes
are the reference's own and are reported, not compared.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
from collections import Counter
from importlib.metadata import version
from pathlib import Path

from probity_records.verified_identities_vectors import (
    EXPECTED_REFUSALS,
    judge,
    vectors,
)

HERE = Path(__file__).resolve().parent
OUTCOMES = ("verified", "contradicted", "indeterminate", "not_evaluated")
PACKAGES = ("probity-records", "agent-evidence-verify")


def case_bytes(cases: list[dict]) -> bytes:
    return (json.dumps(cases, sort_keys=True, indent=2) + "\n").encode()


def pinned_digests() -> set[str]:
    lines = (HERE / "cases.sha256").read_text().splitlines()
    return {line.split()[0] for line in lines if line.strip() and not line.startswith("#")}


def inputs(cases: list[dict]) -> list[dict]:
    return [{k: v for k, v in case.items() if k != "expected"} for case in cases]


def expected_outcome(case_id: str) -> str:
    return "contradicted" if case_id in EXPECTED_REFUSALS else "verified"


def reference(cases: list[dict]) -> dict[str, tuple[str, str]]:
    """Each case judged again from its inputs alone: (outcome, reason code or "")."""
    found = {}
    for case in inputs(cases):
        answer = judge(case)
        code = answer.get("refused", "")
        found[case["id"]] = ("contradicted" if code else "verified", code)
    return found


def external(command: str, cases: list[dict]) -> dict[str, tuple[str, str]]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "cases.json"
        path.write_bytes(case_bytes(inputs(cases)))
        run = subprocess.run([*shlex.split(command), str(path)], capture_output=True, text=True, check=False)
    if run.returncode != 0:
        sys.exit(f"verifier exited {run.returncode}: {run.stderr.strip()[:2000]}")
    reported = json.loads(run.stdout)
    found = {}
    for case in cases:
        outcome = reported.get(case["id"], "not_evaluated")
        if outcome not in OUTCOMES:
            sys.exit(f"verifier reported {outcome!r} for {case['id']}; expected one of {', '.join(OUTCOMES)}")
        found[case["id"]] = (outcome, "")
    return found


def report(cases: list[dict], found: dict[str, tuple[str, str]], label: str, codes: bool) -> list[str]:
    """Print and summarise each case; with ``codes`` the reason code must equal the pinned one too."""
    rows, disagree = [], []
    for case in cases:
        want = expected_outcome(case["id"])
        got, code = found[case["id"]]
        reason = EXPECTED_REFUSALS.get(case["id"], "")
        ok = got == want and (not codes or code == reason)
        if not ok:
            disagree.append(case["id"])
        rows.append(f"| {case['id']} | {want} | {got} | {reason} | {'yes' if ok else 'NO'} | "
                    f"{case['description']} |")
    states = Counter(outcome for outcome, _ in found.values())
    head = [f"## RFC 9421 agent-identity cases: {label}", "",
            f"{len(cases) - len(disagree)} of {len(cases)} cases agree. Outcomes: "
            + ", ".join(f"{s} {states.get(s, 0)}" for s in OUTCOMES) + ".", "",
            "| Case | Expected | Reported | Reference reason | Agrees | What the case is |",
            "| --- | --- | --- | --- | --- | --- |"]
    text = "\n".join(head + rows) + "\n"
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as out:
            out.write(text)
    return disagree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--verifier", help="command that judges a case file (see the module docstring)")
    parser.add_argument("--write", type=Path, help="write the case inputs to this path and stop")
    args = parser.parse_args()
    cases = vectors()
    if not cases:
        sys.exit("the package returned no cases")
    if args.write:
        args.write.write_bytes(case_bytes(inputs(cases)))
        print(f"wrote {len(cases)} cases to {args.write}")
        return 0
    digest = hashlib.sha256(case_bytes(cases)).hexdigest()
    print(", ".join(f"{p} {version(p)}" for p in PACKAGES) + f"; case file sha256 {digest}")
    if digest not in pinned_digests():
        sys.exit("the cases differ from every digest in conformance/cases.sha256. A package bump changed them: "
                 "review the release notes and add the new digest in the same pull request.")
    unpinned = sorted(set(EXPECTED_REFUSALS) - {case["id"] for case in cases})
    if unpinned:
        sys.exit(f"refusals pinned for cases the package no longer has: {', '.join(unpinned)}")
    found = external(args.verifier, cases) if args.verifier else reference(cases)
    disagree = report(cases, found, args.verifier or "reference verifier", codes=not args.verifier)
    return 1 if disagree else 0


if __name__ == "__main__":
    sys.exit(main())
