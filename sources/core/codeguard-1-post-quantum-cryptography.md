---
description: Post-Quantum Cryptography (PQC) guidance and migration best practices
alwaysApply: true
---

# Post-Quantum Cryptography (PQC)

Post-quantum cryptography protects long-lived secrets and future-proof communications against adversaries with quantum capabilities. Adopt PQC via supported libraries and protocols, favoring algorithm agility and incremental, interoperable rollout.

## Goals
- Prefer standardized primitives and vendor-supported APIs; never implement custom crypto.
- Maintain algorithm agility (configurable algorithms, decoupled from business logic).
- Use hybrid key establishment during transition to preserve interoperability and defense-in-depth.
- Validate interoperability and performance before broad rollout.

## Algorithm Selection (Key Establishment and Signatures)
- Key establishment (KEM): Use NIST-standardized ML-KEM (FIPS 203). Select parameter sets per risk and performance.
- Digital signatures: Use standardized ML-DSA (FIPS 204) where supported. Consider SLH-DSA (FIPS 205) where required by policy; account for larger signatures.
 - Continue to rely on vendor-provided, audited implementations. Do not hardcode experimental group names or OIDs; use library-provided options.

## ML-KEM Parameter Set Selection and Packet Size Considerations
- Minimum baseline: ML-KEM-768 should be the minimum consideration for general-purpose and multi-tenant deployments. Avoid ML-KEM-512 for broad use; only consider in highly constrained environments after explicit risk acceptance and compensating controls.
- High-assurance option: ML-KEM-1024 for regulated or high-assurance segments where added overhead is acceptable; validate capacity and latency budgets.
- Packet/message size impacts:
  - ML-KEM public keys and ciphertexts increase handshake sizes; expect larger ClientHello/ServerHello and key exchange messages.
  - Plan for path MTU and fragmentation: tune TLS record sizing as supported; validate middlebox tolerance to larger handshakes; monitor for handshake failures/timeouts.
  - Assess QUIC vs TCP/TLS behavior in your environment; verify congestion and packetization with your vendor’s stack.
  - Measure peak and P95 handshake size and latency before/after enabling hybrids; adjust proxy/load balancer limits as needed (e.g., header/body/initial settings).
- Operational guidance:
  - Prefer vendor-documented hybrid groups or ciphersuites that include ML-KEM-768; avoid experimental or draft identifiers.
  - Document fallback behavior and client capability detection; surface algorithm choices in configuration, not code.
  - Ensure telemetry captures negotiated groups and retry causes to support safe rollouts and rollbacks.

## Recommendation for Multi-Tenant Ecosystems
- Use a hybrid key establishment that combines a classical ECDHE group with ML-KEM-768.
- Rationale: ML-KEM-768 provides a widely recommended balance of security and performance suitable for shared, multi-tenant environments where diverse client capabilities and high request volume demand efficient handshakes.
- Implementation guidance:
  - Enable the library’s supported hybrid mode pairing ML-KEM-768 with a classical group such as X25519 or secp256r1, as documented by the vendor.
  - For example, use X25519 + ML-KEM-768 as the default hybrid pairing; use secp256r1 + ML-KEM-768 when X25519 is unavailable due to policy or platform constraints.
  - Avoid bespoke or ad-hoc hybrids. Do not assemble hybrid handshakes manually; use stable, supported configuration flags or cipher/group selections provided by the stack.

## Deprecations and Disallowed Predecessors
- Discontinue pre-standard, draft, or experiment-only Kyber-based hybrid groups and ciphers (often labeled generically as “Hybrid-Kyber” or with draft names like X25519Kyber…/P256_Kyber/CECPQ2). These predecessors must be replaced with a hybrid ML-KEM alternative provided by the vendor.
- Do not introduce new dependencies on legacy Kyber draft identifiers or OIDs. Migrate configuration and policy to ML-KEM-based hybrids in accordance with FIPS 203 and vendor guidance.

## Protocol Guidance (e.g., TLS, SSH, HPKE)
- Prefer TLS 1.3 where hybrid KEMs are supported by your stack. New solutions should mandate using TLS 1.3 only and avoid TLS 1.2 and earlier versions where possible.
- Use vendor-documented hybrid groups that include ML-KEM-768 during transition. Avoid TLS 1.2 and earlier versions where possible.
- Only enable pure-PQC key establishment when interoperability with required clients is verified. Otherwise, deploy hybrid modes to preserve compatibility while adding PQC assurances.
- For signatures, adopt ML-DSA when supported by the protocol and vendor stack; validate message sizes, handshake overhead, and client support.

## Key Management and Operations
- Generate keys via FIPS-validated or vendor-audited modules (KMS/HSM where available). Use a CSPRNG suitable for the platform.
- Maintain separate keys by purpose (encryption, signatures). Rotate per policy, compromise, or cryptoperiod changes.
- Store keys in KMS/HSM or secure vaults. Never hardcode keys or parameters; avoid plain environment variables for long-lived secrets. Prefer HW-based key protections over Software-only solutions.
- Ensure algorithm identifiers, parameters, and certificates reflect ML-KEM/ML-DSA selections from supported libraries; avoid stale Kyber-era identifiers.
- TPM-backed keys typically do not support ML-DSA today; for mTLS client/server authentication, continue to use EC algorithms supported by your TPM (e.g., ECDSA with secp256r1) until suitable ML-DSA TPM implementations are available in hardware.
- You can deploy hybrid ML-KEM key establishment while continuing to authenticate with ECDSA mTLS certificates; plan migration to ML-DSA-signed certificates when vendor hardware and ecosystem support becomes available.

## Authenticators and Credentials
- FIDO2/WebAuthn: Platform and roaming authenticators today primarily use ECC (e.g., ECDSA/EdDSA). PQC attestation is not broadly deployed; continue using supported authenticators and track vendor roadmaps for PQC or hybrid attestation.
- TPM-backed mTLS: Current TPMs typically do not support ML-DSA. For client/server mTLS certificates, continue to use ECDSA (e.g., secp256r1) until suitable ML-DSA TPM implementations are available in hardware.
- Tokens and credentials: Hybrid ML-KEM key establishment protects transport but does not change token formats. Keep token signing on widely supported algorithms today and design for algorithm agility to adopt ML-DSA when ecosystems support it.
- Policy and configurability: Surface algorithm choices in configuration/policy (not code), define safe defaults and explicit fallback behavior, and capture telemetry for negotiated groups and failures.

## Digital Signatures and Code/Artifact Signing
- Current practice: Use vetted, widely supported signatures (e.g., ECDSA P-256 or Ed25519) for code, container, and SBOM signing while PQC HSM/TPM support is nascent.
- Migration path: Plan for algorithm agility and adopt ML-DSA (FIPS 204) when your toolchain, HSMs/TPMs, and verifiers support it. Expect larger signatures and potential format/verification updates.
- Avoid drafts: Do not adopt draft/proprietary PQC signatures. Prefer standardized ML-DSA when available from audited libraries and hardware.
- Operational checks: Verify verifier support across CI/CD, registries, update servers, and clients; measure artifact size impact; ensure revocation and audit logs remain effective.

## Adoptable Today (Open Source Projects)
- TLS 1.3 hybrid KEM with ML-KEM-768 is available using OpenSSL 3 with the oqs-provider (Open Quantum Safe) or OQS-OpenSSL builds. Use in controlled environments where you manage both client and server. Keep classical fallback enabled; note these builds are not yet FIPS-validated.
- SSH: OpenSSH supports a hybrid key exchange (sntrup761x25519). While not ML-KEM, it provides a PQC KEX option. Adopt per your policy until ML-KEM hybrids are supported in your SSH stack.
- HPKE and libraries: Open Quantum Safe libraries (liboqs) can be used to develop ML-KEM-based HPKE and related constructs.
- FIDO/WebAuthn (production today): Continue to use platform/hardware authenticators with classical algorithms (COSE ES256/ECDSA P-256; allow EdDSA where supported). Keep accepted COSE algorithms configurable on the RP/server, log negotiated algorithms, and maintain attestation/trust metadata. PQC authenticators/attestations are not broadly available today; track standards and vendor roadmaps.

## Migration Plan
- Inventory cryptography usage and endpoints. Identify where key establishment and signature algorithms are configured or negotiated.
- Prioritize externally facing, high-value, and long-lived data flows for hybrid deployment first.
- Roll out hybrid ML-KEM-768 in stages with monitoring, fallbacks, and explicit client compat testing.
- Decommission predecessor “Hybrid-Kyber” configurations and remove any policy allowances or feature flags that enable them.

## Implementation Checklist
- Hybrid key establishment enabled with ML-KEM-768 alongside a classical ECDHE group.
- No usage of predecessor draft Kyber hybrids; configurations updated to ML-KEM hybrids.
- Algorithms are configurable (algorithm agility) and surfaced in policy/config, not compiled into business logic.
- Keys generated with a CSPRNG in validated modules; stored in KMS/HSM; separated by purpose; rotation documented.
- Protocol versions and cipher/group selections align with vendor-documented, supported PQC options.
- Monitoring in place for handshake success rates, latency, and error codes after enabling hybrids.

## Test Plan
- Interoperability tests across representative clients/agents for hybrid ML-KEM-768 handshakes; verify negotiation and fallback behavior.
- Negative tests: reject configurations attempting legacy Hybrid-Kyber or draft-only group names.
- Performance/regression tests: measure handshake latency and server CPU for peak and P95 after enabling hybrids.
- Configuration validation: confirm algorithm identifiers and parameters map to ML-KEM/ML-DSA in logs and diagnostics; ensure no stale Kyber draft identifiers remain.
