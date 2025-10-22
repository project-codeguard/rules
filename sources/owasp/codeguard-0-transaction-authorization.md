---
description: Transaction Authorization Security
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

## Transaction Authorization Security

Secure implementation of transaction authorization to prevent bypassing of sensitive operations like wire transfers through robust user confirmation and server-side enforcement.

### Transaction Authorization Concept

Transaction authorization requires users to submit a second factor to verify authorization for sensitive operations. This applies beyond financial systems to any operation requiring explicit user consent (account unlocks, privilege changes, data modifications).

Authorization methods include:
- Time-based one-time password (OTP) tokens (OATH TOTP)
- OTP sent by SMS or phone
- Digital signatures from smart cards or smartphones
- Challenge-response tokens including unconnected card readers
- Transaction authorization cards with unique numbers

### Functional Requirements

#### User Identification and Acknowledgment (What You See Is What You Sign)
Transaction authorization must allow users to identify and acknowledge significant transaction data.

Key principles:
- User must verify all significant transaction data during authorization process
- Display critical information: target account, amount, transaction type
- Balance security requirements with user experience and technical constraints
- For external devices with limited displays, show minimum significant data (partial account number, amount)
- Ensure meaningful prompts to prevent social engineering and malware abuse

#### Authorization Token and Method Changes
- Changes to authorization tokens require authorization using current authorization credentials
- Changes to authorization methods require authorization using current authorization method
- Prevent malware from downgrading to least secure authorization method
- Inform users about potential dangers of different authorization methods

#### Authentication vs Authorization Separation
Distinguish authentication process from transaction authorization process to prevent credential reuse attacks.

Prevention strategies:
- Use different methods for authentication and transaction authorization
- Employ different actions in external security components
- Present clear messages about what users are signing
- Prevent malware from using authentication credentials for transaction authorization

#### Unique Authorization per Transaction
Each transaction requires unique authorization credentials to prevent replay attacks and credential reuse during sessions.

### Non-Functional Requirements

#### Server-Side Enforcement
All authorization checks must be performed and enforced server-side.

Implementation requirements:
- Never allow client-side influence on authorization results
- Prevent tampering with transaction data parameters
- Prevent adding/removing parameters that disable authorization checks
- Apply security programming best practices (default deny, no debug code in production)
- Encrypt data for confidentiality and integrity, verify server-side

#### Authorization Method Enforcement
Server-side must enforce chosen authorization method or application policies.

Security considerations:
- Prevent client-side manipulation of authorization method parameters
- Avoid building new authorization methods on old insecure codebases
- Ensure attackers cannot downgrade to older, less secure methods

#### Server-Side Transaction Verification
Generate and store all significant transaction data server-side.

Requirements:
- All transaction data must be verified by user and generated server-side
- Pass data to authorization component without client tampering possibility
- Prevent malware manipulation of transaction data display

#### Brute-Force Protection
Implement protections against authorization credential brute-force attacks.

Controls:
- Restart entire transaction authorization process after failed attempts
- Apply throttling and retry limits
- Use additional automation prevention techniques

#### Transaction State Control
Enforce sequential transaction state transitions.

Standard transaction flow:
1. User enters transaction data
2. User requests authorization from application
3. Application initializes authorization mechanism
4. User verifies/confirms transaction data
5. User responds with authorization credentials
6. Application validates authorization and executes transaction

Protection measures:
- Prevent out-of-order step execution
- Prevent step skipping
- Protect against transaction data overwriting before authorization
- Prevent skipping transaction authorization entirely

#### Transaction Data Protection
Protect transaction data against modification during authorization process.

Implementation strategies:
- Invalidate authorization data if transaction data is modified
- Reset authorization process on transaction data modifications
- Log, monitor, and investigate modification attempts
- Prevent Time of Check to Time of Use vulnerabilities

#### Data Confidentiality
Protect transaction data privacy during all client-server communications throughout the authorization process.

#### Transaction Execution Verification
Implement final control gate before transaction execution.

Verification requirements:
- Verify transaction was properly authorized by user
- Prevent Time of Check to Time of Use attacks
- Prevent authorization check bypass in transaction entry process

#### Time-Limited Authorization
Limit authorization credential validity to prevent delayed abuse by malware.

Controls:
- Restrict time window between challenge/OTP generation and authorization completion
- Balance security with normal user behavior
- Help prevent resource exhaustion attacks

#### Unique Authorization Credentials
Generate unique authorization credentials for every operation to prevent replay attacks.

Generation methods:
- Use timestamps in signed transaction data
- Include sequence numbers in challenges
- Use random values in authorization components

### Implementation Considerations

#### Risk-Based Authorization
Determine which transactions require authorization based on:
- Risk analysis of specific application
- Risk exposure assessment
- Other implemented safeguards

#### Cryptographic Protection
Implement cryptographic operations to ensure:
- Transaction integrity
- Data confidentiality
- Non-repudiation of transactions

#### Secure Key Management
Protect device signing keys during device pairing and signing protocol.

Security measures:
- Prevent malware injection/replacement of signing keys
- Use second factors for key protection (passwords, biometrics)
- Leverage secure elements (TEE, TPM, smart cards)

#### User Awareness
Train users on secure practices:
- Verify transaction data from trusted sources, not computer screens
- Understand risks of different authorization mechanisms
- Recognize social engineering attempts

#### Anti-Malware Integration
Deploy anti-malware solutions as additional protection layer while recognizing they cannot provide 100% effectiveness.

### Security Controls Summary

1. Implement What You See Is What You Sign principle for transaction data verification
2. Separate authentication from transaction authorization processes
3. Use unique, time-limited authorization credentials per transaction
4. Enforce all authorization logic server-side without client trust
5. Protect authorization token and method changes through re-authorization
6. Prevent authorization method downgrade attacks
7. Implement brute-force protection with transaction resets
8. Enforce sequential transaction state transitions
9. Protect transaction data against modification during authorization
10. Secure all client-server communications with encryption
11. Verify proper authorization before transaction execution
12. Use cryptographic signing and secure key storage for integrity
13. Monitor and log suspicious authorization activities
14. Provide user education on authorization security practices