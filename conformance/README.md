# Conformance cases

Reference cases with fixed answers, run on every pull request. The first
set covers agent identity carried in an RFC 9421 HTTP message signature: a request signed over its
method, target, authority, body digest and a field naming who acts for whom (a user, the agent chain
acting for that user, and the digests of their credentials). There are 78 cases: 14 the verifier
accepts and 64 it refuses, each refusal with its reason code.

```sh
python -m pip install -r conformance/requirements.txt
python conformance/run.py                        # the reference verifier
python conformance/run.py --verifier "your-cmd"  # your verifier, on the same cases
python conformance/run.py --write cases.json     # the case inputs, for your own tooling
```

`--verifier` runs your command with the path of a JSON file of case inputs as its last argument. It
prints one JSON object mapping each case id to one of the four outcomes of RFP 4.4.1: `verified`,
`contradicted`, `indeterminate` or `not_evaluated`. A case it leaves out is `not_evaluated`. The run
prints a table of every case and writes it to the job summary.

## What the cases bear on

| Where | Cases |
| --- | --- |
| RFP 4.1.6, prevention of identity spoofing | a forged signature (VS2), a pinned key id signed by another key (VS4), a signature replayed on another target, method or authority (VS8 to VS10), principals swapped after signing (VS11), forged or unsigned credentials (VR1, VR2, VR13) |
| RFP 4.1.3, no trust because a party supplied the value | a credential naming its own key (VR3, VR4), an issuer or signing key the verifier does not pin (VR9, VR10, VS3, VS29, VS30) |
| RFP 4.2.2, principal authorization | an agent acting for a user and a sub-agent chain (VI1, VI2); a credential naming another agent (VR15) or issued to another client (VR16); a signature that names the user acting alone (VS25) or an agent acting for no user (VS26) |
| RFP 4.1.4, third-party verification | every case: the verifier needs only the case file and the keys it pins |
| x402 extension `http-message-signatures` | the verification rules the extension leaves open: covered components and their order (VS15, VS16), tag (VS17), algorithm (VS18), a required expiry, a five-minute lifetime cap and clock checks (VS5, VS19 to VS21), the body digest (VS6, VS7, VS33) and strict structured-field parsing (VS12, VS22, VS31, VS34) |

## Pins

`requirements.txt` pins the case package and the verifier exactly, and Dependabot opens a pull request
for each new release. `cases.sha256` holds the digest of the case file each pinned release builds, and
`run.py` also checks every refusal against the code the package pins for it. A release that changes
the cases fails its Dependabot pull request until the new digest is added there, so a changed answer is
always reviewed before it lands.
