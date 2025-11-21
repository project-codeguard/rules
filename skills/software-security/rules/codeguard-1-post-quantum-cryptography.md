---
description: Post-Quantum Cryptography (PQC) guidance and migration best practices
alwaysApply: true
---

rule_id: codeguard-1-post-quantum-cryptography

# Post-Quantum Cryptography (PQC)

Concise Code Guard focused on what to implement and how to test it.

## Implementation (Do this)
- Enforce TLS 1.3 only (or later when available).
- Use vendor‑supported crypto APIs only; never implement custom crypto. Do not hand‑roll hybrids or hardcode experimental group names/OIDs.
- Hybrid KEM: enable vendor‑documented hybrids that include ML‑KEM‑768 with a classical ECDHE group (X25519 or secp256r1). Use ML‑KEM‑1024 for high‑assurance segments after validating overhead.
- Multi-tenant systems that share crypto resources across tenants should select Hybrid KEM with ML‑KEM‑768 + ECDHE; ML‑KEM‑1024 where required.  X25519 is recommended for ECDHE.
- Avoid predecessors: remove legacy/draft “Hybrid‑Kyber” groups (e.g., CECPQ2; X25519Kyber…, P256_Kyber) and draft OIDs.
- Configuration, not code: expose algorithm choices in config/policy; document fallback behavior; keep a classical‑only fallback for incompatible clients if you don't control both client and server.
- Key management: use KMS/HSM; generate keys with a CSPRNG; separate encryption vs signatures; rotate per policy; never hardcode keys/parameters; avoid plain env vars for long‑lived secrets.
- Certificates/signatures: continue ECDSA (P‑256) for mTLS and code signing until ML‑DSA is supported by your stack; plan migration to ML‑DSA.
- Telemetry and limits: capture negotiated groups, handshake sizes, and retry/failure causes. Tune TLS record sizes and proxy/LB limits to avoid fragmentation and timeouts.
- SSH/HPKE: enable only vendor‑supported PQC/hybrid KEX (e.g., sntrup761x25519 in OpenSSH if allowed). For HPKE, rely on native language runtime/vendor/audited libraries that support ML‑KEM.

## Migration
- Inventory endpoints and crypto usage.
- Prioritize external/high‑value/long‑lived flows.
- Roll out hybrids in stages with metrics and rollback; remove predecessor configs after success criteria are met.

## Implementation Checklist
- Hybrid key establishment with ML‑KEM‑768 + ECDHE; ML‑KEM‑1024 where required.
- Avoid ML‑KEM‑512 except in explicitly risk‑accepted, highly constrained device or network environments, with compensating controls and tight scope.
- No draft Kyber groups; only vendor‑documented ML‑KEM hybrids.
- Algorithm agility via configuration (not code); explicit fallback behavior.
- Keys via validated modules; separated by purpose; rotation policy in place.
- TLS version and group selections align with supported PQC options.
- Monitoring in place for handshake success/latency/errors and negotiated groups.

## Test Plan
- Interoperability: verify hybrid ML‑KEM‑768 and ML‑KEM‑1024 handshakes across representative clients; validate negotiated groups and fallback paths.
- Negative: reject legacy/draft Hybrid‑Kyber identifiers and misconfigured groups.
- Performance: measure handshake size and latency (peak and P95) and server CPU after enabling hybrids; tune record sizes and limits as needed.
- Configuration validation: confirm groups/algorithm identifiers in logs and diagnostics; ensure no stale Kyber‑era identifiers remain.
