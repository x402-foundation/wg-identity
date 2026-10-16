# Identity Working Group

The **Identity Working Group** standardizes decentralized agent identity, delegated authority mandates, human-in-the-loop authorization, and hardware-attested execution within the x402 (RFC 9110 HTTP 402) protocol framework.

As autonomous AI agents transact, negotiate, and settle payments across the open web, the Identity Working Group defines how autonomous clients prove their provenance, delegate spend authorities, and enforce non-custodial cryptographic policies without exposing master private keys or credentials.

## Leadership & Governance

* **Chair**: Nicole Dunn
* **Co-Chair**: Amanda McDermott
* **Operating Model**: All work is conducted openly under the Linux Foundation Antitrust Policy and Apache-2.0 license.

## Goals

The primary goals of the Identity Working Group are:

1. **Standardize Agent Identity & Machine Credentials**: Establish normative specifications for agent identification using W3C Decentralized Identifiers (DIDs), Verifiable Credentials (VCs), and cryptographic key attestation across heterogeneous settlement networks.
2. **Intent Delegation & Down-Scoped Spend Mandates**: Specify policy delegation frameworks (e.g., FIDO2/WebAuthn passkeys, time-bounded allowances, and merchant-restricted spend mandates) allowing human operators to delegate economic agency without exposing long-lived signing keys to LLM execution contexts.
3. **Hardware-Enforced Identity Roots & Confidential Attestation**: Codify integration patterns for hardware-isolated execution environments (Confidential Computing enclaves, Intel TDX RTMRs, AMD SEV-SNP, Apple Secure Enclave) so agents can cryptographically prove their running code measurement and operational integrity to upstream counterparties.
4. **Non-Repudiation & Transparency Logging**: Define interoperability profiles with verifiable transparency ledgers (such as IETF SCITT and append-only receipt registries) to ensure immutable audit trails of agent authorization and state transitions.
5. **Cross-Working Group Interoperability**: Harmonize identity and delegation mandates with Domain Discovery (agent capability advertisement), Tax (verifiable attribution and compliance receipts), and Card Acceptance (delegated virtual card tokens).
6. **Data-Subject Permission & Fair Value Allocation**: Specify how paid lookups, queries, or transactions concerning an identified individual carry that person's cryptographically verifiable permission for that request and agent, checked for revocation at request time (e.g., consent receipts, Verifiable Presentations), and define architectural interfaces for locking in or routing the data-subject's allocated share upon settlement.
7. **Payee Identity & Payment-Destination Binding**: Specify how a resource server's payment requirements (`payTo`) and answering origin (harmonized with Domain Discovery `/.well-known/x402` manifests) bind to a verifiable payee identity (e.g., W3C DIDs, institutional KYB/LEI Verifiable Credentials, hardware enclave attestations, or decentralized naming assertions), enabling paying agents to verify at request time—prior to signing—that the answering origin is controlled by the expected counterparty, that the `payTo` destination is authorized by it, and that any data-subject share it locks in or routes under Goal 6 is bound to the data subject the request concerns, independent of any single settlement rail, naming registry, or credential system.

## Anticipated Deliverables

* **Specification**: *x402 Agent Identity & Delegated Authority Framework*.
* **JSON Schema**: Normative schemas for agent identity manifests, payee destination bindings, spend mandates, hardware attestation payloads, and data-subject consent receipts.
* **Reference Vectors**: Test suites for passkey delegation verification, agent-to-agent mutual authentication, and enclave measurement verification.
* **Implementation Guide**: Architectural best practices for non-custodial agent key management, prompt injection defense, and hardware security boundaries.

## Meetings

Bi-weekly on Tuesdays (alternating with Card Acceptance WG)  
10:00 AM CT | 11:00 AM ET | 8:00 AM PT | 4:00 PM BST | 11:00 PM SGT

A schedule of public meetings and calendar links can be found on the [x402 Community Calendar](https://x402.org/get-involved/#calendar).

### Resources

- Past meeting notes and agendas are available [online](https://docs.google.com/document/d/1SPlTQYm_ysVsF_I_TmhwAfQiSjapSaUmSov9-RoMLRI/edit?tab=t.0).
- Recordings of public meetings are accessible through the LFX platform.

## Communication Channels

- **Public Slack**: [#wg-identity](https://x402workspace.slack.com/archives/C0BA2SQK9GU)
- **Mailing List**: [Identity-Working-Group@lists.x402.org](mailto:Identity-Working-Group@lists.x402.org) (Subscribe at [lists.x402.org](https://lists.x402.org/g/Identity-Working-Group))
