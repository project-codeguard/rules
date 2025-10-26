---
description: Password Storage Security
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
alwaysApply: false
---

## Password Storage Security Guidelines

Essential practices for securely storing passwords using modern hashing algorithms to protect against offline attacks.

### Core Principles

Passwords must be hashed, NOT encrypted. Hashing is a one-way function that prevents retrieval of the original password even if the database is compromised. Encryption is reversible and should only be used in rare edge cases where the original password must be recovered.

Strong passwords stored with modern hashing algorithms and proper configuration should be effectively impossible for attackers to crack.

To sum up our recommendations:

- **Use [Argon2id](#argon2id) with a minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism.**
- **If [Argon2id](#argon2id) is not available, use [scrypt](#scrypt) with a minimum CPU/memory cost parameter of (2^17), a minimum block size of 8 (1024 bytes), and a parallelization parameter of 1.**
- **For legacy systems using [bcrypt](#bcrypt), use a work factor of 10 or more and with a password limit of 72 bytes.**
- **If FIPS-140 compliance is required, use [PBKDF2](#pbkdf2) with a work factor of 600,000 or more and set with an internal hash function of HMAC-SHA-256.**
- **Consider using a [pepper](#peppering) to provide additional defense in depth (though alone, it provides no additional secure characteristics).**

### Recommended Algorithms and Parameters

Use these algorithms in order of preference:

#### Argon2id (Preferred)
Argon2id was the winner of the 2015 Password Hashing Competition and provides balanced resistance to side-channel and GPU-based attacks.

Configuration options (choose one):
- m=47104 (46 MiB), t=1, p=1
- m=19456 (19 MiB), t=2, p=1  
- m=12288 (12 MiB), t=3, p=1
- m=9216 (9 MiB), t=4, p=1
- m=7168 (7 MiB), t=5, p=1

All configurations provide equal security with different CPU/RAM trade-offs.

#### scrypt (If Argon2id unavailable)
Configuration options (choose one):
- N=2^17 (128 MiB), r=8 (1024 bytes), p=1
- N=2^16 (64 MiB), r=8 (1024 bytes), p=2
- N=2^15 (32 MiB), r=8 (1024 bytes), p=3
- N=2^14 (16 MiB), r=8 (1024 bytes), p=5
- N=2^13 (8 MiB), r=8 (1024 bytes), p=10

#### bcrypt (Legacy systems only)
Use work factor of 10 or more. Maximum password length is 72 bytes for most implementations.

#### PBKDF2 (FIPS-140 compliance required)
- PBKDF2-HMAC-SHA1: 1,300,000 iterations
- PBKDF2-HMAC-SHA256: 600,000 iterations
- PBKDF2-HMAC-SHA512: 210,000 iterations

### Salting

Modern hashing algorithms (Argon2id, bcrypt, scrypt, PBKDF2) automatically handle salting. Salts must be:
- Unique for every password
- Generated using a cryptographically secure random number generator
- Stored alongside the hash

Never manually implement salting when using modern algorithms.

### Peppering (Optional Defense in Depth)

A pepper is a secret value shared between stored passwords, unlike salts which are unique per password. Peppers provide additional protection if the database is compromised but the application server remains secure.

Requirements for peppering:
- Store pepper separately from the password database
- Use secure storage (secrets vaults, HSMs)
- Generate securely using cryptographically strong methods
- Changing pepper requires all users to reset passwords

Implementation strategies:
- Pre-hashing: Add pepper to password before hashing
- Post-hashing: HMAC the password hash with pepper as key

### Work Factor Tuning

Balance security and performance by adjusting work factors:
- Target less than one second for hash calculation
- Increase work factors over time as hardware improves
- Test on your specific server hardware
- Higher work factors slow down both legitimate authentication and attacker cracking

### Upgrading Legacy Hashes

For applications using weak algorithms (MD5, SHA-1):

Method 1: Force password reset
- Expire old hashes for inactive users
- Require password reset on next login
- More secure but less user-friendly

Method 2: Layer hashing
- Use existing hash as input to secure algorithm
- Example: `bcrypt(md5($password))`
- Upgrade to direct hashing when user next authenticates
- Store algorithm and parameters using PHC string format

### bcrypt Pre-Hashing Considerations

If pre-hashing with bcrypt is necessary:
- Use `bcrypt(base64(hmac-sha384(data:$password, key:$pepper)), $salt, $cost)`
- Store pepper outside database
- Avoid simple pre-hashing like `bcrypt(sha512($password))` due to password shucking vulnerability

### International Character Support

Password hashing libraries must:
- Accept full Unicode character range
- Support null bytes in passwords
- Preserve entropy without reduction
- Handle characters from various languages and pictograms

### Performance Guidelines

- Hash calculation should take less than one second
- Benchmark on production hardware
- Monitor authentication performance
- Adjust parameters based on server capacity and user load
- Consider denial of service risks from overly high work factors

### Implementation Summary

Secure password storage requires:
- Modern slow hashing algorithms (Argon2id preferred)
- Proper algorithm configuration with adequate work factors
- Automatic salt handling by the hashing library
- Optional pepper for defense in depth
- Upgrade path for legacy hashes
- Performance tuning for your environment
- Support for international characters

Following these practices protects user passwords against offline attacks even if the database is compromised.