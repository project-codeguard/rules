---
description: Cryptographic Storage Best Practices
languages:
- c
- go
- java
- javascript
- kotlin
- matlab
- python
- ruby
- swift
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## Introduction

This rule provides a simple model to follow when implementing solutions to protect data at rest.

Passwords should not be stored using reversible encryption - secure password hashing algorithms should be used instead. The [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) contains further guidance on storing passwords.

## Rule 1: Architectural Design Requirements

**YOU MUST consider the overall architecture** of the system, as this will have a huge impact on the technical implementation.

* **Application level** - REQUIRED for database compromise protection
* **Database level** (SQL Server TDE) - Additional data-at-rest protection  
* **Filesystem level** (BitLocker, LUKS) - Physical theft protection
* **Hardware level** (encrypted RAID/SSDs) - Hardware-based protection

**YOU MUST minimize sensitive data storage** - avoid storing credit card details and implement data minimization policies. Use tokenization when storage is unavoidable.

## Rule 2: Algorithm Requirements

**YOU MUST use approved algorithms:**
* **Symmetric:** AES with ≥128-bit keys (256-bit preferred)
* **Asymmetric:** Curve25519 (ECC preferred) or RSA ≥2048 bits
* **Custom algorithms:** PROHIBITED

**YOU MUST use authenticated cipher modes:**
1. **GCM** or **CCM** (preferred)
2. **CTR/CBC** only with separate authentication (Encrypt-then-MAC)
3. **ECB:** PROHIBITED

**For RSA: YOU MUST enable Random Padding** (OAEP/PKCS#1).

**YOU MUST use cryptographically secure random generators:**

| Platform | PROHIBITED | REQUIRED |
|----------|------------|----------|
| PHP | `rand()`, `mt_rand()` | `random_bytes()`, `random_int()` |
| Java | `java.util.Random` | `java.security.SecureRandom` |
| .NET | `System.Random` | `System.Security.Cryptography.RandomNumberGenerator` |
| Python | `random` module | `secrets` module |
| JavaScript | `Math.random()` | `window.crypto.getRandomValues()` |
| Go | `math/rand` | `crypto/rand` |
| Node.js | `Math.random()` | `crypto.randomBytes()`, `crypto.randomInt()` |

**UUIDs:** Version 1 UUIDs are NOT random. Only trust Version 4 UUIDs if implementation uses CSPRNG.

## Rule 3: Key Management Requirements

**YOU MUST implement formal processes for:**
* Key generation using cryptographically secure functions
* Secure key distribution and deployment
* Regular key rotation and secure decommissioning

**Key Generation:** YOU ARE PROHIBITED from using passwords, phrases, or predictable patterns. Multiple keys MUST be fully independent.

**Key Rotation Requirements - YOU MUST rotate keys when:**
* Key compromise is suspected
* Cryptoperiod expires (see NIST SP 800-57)
* Usage limits reached (2^35 bytes for 64-bit keys, 2^68 bytes for 128-bit)
* Algorithm security changes

**YOU MUST have rotation processes ready BEFORE compromise.**

## Rule 4: Key Storage Requirements

**YOU MUST use secure storage mechanisms where available:**
* Physical/Virtual HSMs
* Cloud key vaults (AWS KMS, Azure Key Vault, Google Cloud KMS)
* External secrets management (HashiCorp Vault, Conjur)
* Framework secure APIs (ProtectedData, Keychain)

**Basic Storage Rules (when secure mechanisms unavailable):**
* PROHIBITED: Hard-coding keys in source code or version control
* REQUIRED: Restrictive permissions on config files
* AVOID: Environment variables (exposure risk)

**Key Separation:** YOU MUST store keys separately from encrypted data where possible.

**Key Encryption:** YOU MUST encrypt stored keys using separate Key Encryption Keys (KEK):
* Data Encryption Key (DEK) encrypts data
* Key Encryption Key (KEK) encrypts DEK
* KEK MUST be stored separately and be ≥ as strong as DEK

## Rule 5: Defense in Depth Requirements

**YOU MUST design applications to be secure even if cryptographic controls fail:**
* Additional security layers for encrypted information
* Strong access control (not relying on encrypted URL parameters alone)
* Logging and monitoring of encrypted data access

## Critical Security Requirements

**COMPLIANCE IS MANDATORY** for all systems handling sensitive data.

**YOU ARE ABSOLUTELY PROHIBITED FROM:**
* Implementing custom cryptographic algorithms
* Using insecure random generators for security purposes
* Hard-coding encryption keys in source code
* Using deprecated algorithms (MD5, SHA-1, DES, RC4)
* Storing keys with encrypted data without proper separation

**YOU MUST ALWAYS:**
* Use authenticated encryption modes where available
* Generate unique, random keys for each operation
* Implement proper key lifecycle management
* Use vetted cryptographic libraries only
* Test key rotation procedures before needed