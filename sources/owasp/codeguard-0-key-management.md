---
description: Cryptographic Key Management Security
languages:
- c
- go
- java
- javascript
- kotlin
- python
- ruby
- swift
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## Key Management Security Guidelines

Essential practices for secure cryptographic key management in applications.

### Key Generation

Cryptographic keys shall be generated within cryptographic module with at least FIPS 140-2 compliance. Any random value required by the key-generating module shall be generated within that module using a Random Bit Generator implemented within the cryptographic module.

Hardware cryptographic modules are preferred over software cryptographic modules for protection.

### Key Storage

- Keys must be protected on both volatile and persistent memory, ideally processed within secure cryptographic modules
- Keys should never be stored in plaintext format
- Ensure all keys are stored in a cryptographic vault, such as a hardware security module (HSM) or isolated cryptographic service
- When storing keys in offline devices/databases, encrypt the keys using Key Encryption Keys (KEKs) prior to export
- KEK length and algorithm should be equivalent to or greater in strength than the keys being protected
- Ensure that standard application level code never reads or uses cryptographic keys directly

### Key Usage and Separation

According to NIST, in general, a single key should be used for only one purpose (e.g., encryption, authentication, key wrapping, random number generation, or digital signatures).

Reasons for key separation:
- The use of the same key for two different cryptographic processes may weaken the security provided
- Limiting the use of a key limits the damage that could be done if the key is compromised
- Some uses of keys interfere with each other

### Memory Management

Keys stored in memory for a long time can become "burned in". This can be mitigated by splitting the key into components that are frequently updated.

Plan for the recovery from possible corruption of the memory media necessary for key or certificate generation, registration, and distribution systems.

### Key Backup and Recovery

Data that has been encrypted with lost cryptographic keys will never be recovered. Therefore, it is essential that applications incorporate a secure key backup capability.

When backing up keys, ensure that the database used to store the keys is encrypted using at least a FIPS 140-2 validated module.

Never escrow keys used for performing digital signatures, but consider the need to escrow keys that support encryption.

### Trust Store Security

- Design controls to secure the trust store against injection of third-party root certificates
- Implement integrity controls on objects stored in the trust store
- Do not allow for export of keys held within the trust store without authentication and authorization
- Setup strict policies and procedures for exporting key material
- Implement a secure process for updating the trust store

### Key Security Requirements

- Generate keys only in FIPS 140-2 validated modules or HSMs
- Use NIST-approved algorithms with appropriate key lengths
- Never reuse keys for different cryptographic purposes
- Implement key rotation and lifecycle management
- Use ephemeral keys for Perfect Forward Secrecy
- Monitor and audit all key access operations
- Use only reputable crypto libraries that are well maintained and validated by third-party organizations