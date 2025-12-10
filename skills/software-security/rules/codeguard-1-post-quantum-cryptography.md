---
description: Post-Quantum Cryptography (PQC) guidance and migration best practices
alwaysApply: true
---

rule_id: codeguard-1-post-quantum-cryptography

# Post-Quantum Cryptography (PQC)

Concise Code Guard focused on what to implement and how to test it.

## Implementation (Do this)
- Enforce (D)TLS 1.3 only (or later when available).
- (D)TLS PQC key exchange (when supported by your stack):
  - Prefer hybrid named groups per I-D.ietf-tls-ecdhe-mlkem:
    - X25519MLKEM768 (X25519 + ML‑KEM‑768)
    - SecP256r1MLKEM768 (P‑256 + ML‑KEM‑768)
    - SecP384r1MLKEM1024 (P‑384 + ML‑KEM‑1024) for high‑assurance segments
  - Pure PQC (only after interop validation) per I-D.ietf-tls-mlkem-key-agreement:
    - ML‑KEM‑768 baseline; ML‑KEM‑1024 where required; avoid ML‑KEM‑512 except in constrained environments with explicit risk acceptance
  - Use vendor‑documented, supported identifiers; avoid legacy “Hybrid‑Kyber” names and draft‑only aliases
- IPsec: Enforce IKEv2 only; use ESP with AEAD (e.g. AES‑256‑GCM or stronger); require PFS via ECDHE (X25519 or secp256r1); use SHA‑256+ for IKE PRF/auth; configure time/byte‑based lifetimes to re‑key IKE_SA and CHILD_SAs; disable IKEv1 and legacy suites (3DES, DES, MD5, SHA‑1, AES‑CBC).
- IKEv2 PQC support: implement RFC 9242 (IKEv2 Intermediate Exchange) and RFC 9370 (Multiple Key Exchanges in IKEv2) to enable hybrid PQC + ECDHE and handle larger exchanges. Apply to both initial exchanges and re‑key (CREATE_CHILD_SA) so hybrids persist across re‑keys. Select Hybrid KEM with ML‑KEM‑768 + ECDHE; ML‑KEM‑1024 where required.
- Use vendor‑supported crypto APIs only; never implement custom crypto. Do not hand‑roll hybrids or hardcode experimental group names/OIDs.
- Symmetric encryption: Shor's algorithm and quantum computers do not affect symmetric algorithms like AES; using AES‑256 keys (or stronger) is highly recommended.
- Hybrid KEM: enable vendor‑documented hybrids that include ML‑KEM‑768 with a classical ECDHE group (X25519 or secp256r1). Use ML‑KEM‑1024 for high‑assurance segments after validating overhead.
- Multi-tenant systems that share crypto resources across tenants should select Hybrid KEM with ML‑KEM‑768 + ECDHE; ML‑KEM‑1024 where required.  X25519 is recommended for ECDHE.
- Avoid predecessors: remove legacy/draft “Hybrid‑Kyber” groups (e.g., CECPQ2; X25519Kyber…, P256_Kyber) and draft OIDs.
- Configuration, not code: expose algorithm choices in config/policy; document fallback behavior; keep a classical‑only fallback for incompatible clients if you don't control both client and server.
- Key management: use KMS/HSM; generate keys with a CSPRNG; separate encryption vs signatures; rotate per policy; never hardcode keys/parameters; avoid plain env vars for long‑lived secrets; require hardware‑backed keys (HSM/TPM) for private key storage.
- Certificates/signatures: continue ECDSA (P‑256) for mTLS and code signing until hardware‑backed ML‑DSA is available in your stack (e.g., HSM or TPM); plan migration to ML‑DSA once supported.
- Hardware requirement for ML‑DSA: do not enable PQC ML‑DSA signatures using software‑only keys. Require HSM/TPM‑backed key storage and signing paths before migrating.
- Telemetry and limits: capture negotiated groups, handshake sizes, and retry/failure causes. Tune (D)TLS record sizes and proxy/LB/concentrator limits to avoid fragmentation and timeouts.
- SSH/HPKE: enable only vendor‑supported PQC/hybrid KEX (e.g., sntrup761x25519 in OpenSSH if allowed). For HPKE, rely on native language runtime/vendor/audited libraries that support ML‑KEM.
- IPsec re‑key: configure time/byte‑based lifetimes to re‑key IKE_SA and CHILD_SAs; ensure re‑key maintains the same algorithms used during IKEv2 exchanges.

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
  - Hardware‑backed key storage (HSM/TPM) required before enabling ML‑DSA signatures; continue ECDSA (P‑256) for mTLS/signing until hardware support exists.
  - (D)TLS version and group selections align with supported PQC options.
  - IPsec re‑key configured (time/byte lifetimes) with PFS; hybrid ML‑KEM + ECDHE persists across re‑key.
  - Monitoring in place for handshake success/latency/errors and negotiated groups.

## Test Plan
- Interoperability: verify hybrid ML‑KEM‑768 and ML‑KEM‑1024 handshakes across representative clients; validate negotiated groups and fallback paths.
- Interoperability ((D)TLS): verify negotiation of X25519MLKEM768 / SecP256r1MLKEM768 hybrids and fallback to classical ECDHE; validate pure ML‑KEM groups only in staged tests.
- Interoperability (IKEv2/IPsec): verify hybrid ML‑KEM‑768 + ECDHE (X25519 or P‑256) via RFC 9242/9370 multi‑KE; confirm fallback to classical ECDHE; evaluate ML‑KEM‑1024 where required. Use vendor‑documented identifiers;
- Re‑key (IKEv2/IPsec): validate re‑key of IKE_SA and CHILD_SAs maintains hybrid ML‑KEM + ECDHE; confirm no fallback to classical‑only on re‑key; measure re‑key overhead.
- Negative: reject legacy/draft Hybrid‑Kyber identifiers and misconfigured groups.
- Performance: measure handshake size and latency (peak and P95) and server CPU after enabling hybrids; tune record sizes and limits as needed.
