---
description: SAML Security Guidelines
languages:
- java
- javascript
- python
- xml
alwaysApply: false
---

## SAML Security Guidelines

Essential security practices for implementing Security Assertion Markup Language (SAML) integrations to prevent common vulnerabilities and attacks.

### Transport Security

Use TLS 1.2 or higher for all SAML message transport to guarantee confidentiality and integrity. This protects against eavesdropping, theft of authentication information, bearer token theft, message deletion/modification, and man-in-the-middle attacks.

### Message Integrity and Authentication

Digitally sign SAML messages using certified keys to guarantee message integrity and authentication. This prevents man-in-the-middle attacks, forged assertions, and message modifications.

Encrypt assertions via XMLEnc to prevent disclosure of sensitive attributes after transportation, protecting against theft of user authentication information.

### Protocol Usage Validation

Follow SAML Profile requirements strictly. The AVANTSSAR team identified these required elements:

AuthnRequest Requirements:
- Must contain unique ID and SP (Service Provider) identifier
- Request ID must be returned in response via InResponseTo attribute

Response Requirements:
- Must contain unique ID, SP identifier, IdP identifier, and digitally signed assertion
- InResponseTo must match previously sent request ID

Authentication Assertion Requirements:
- Must contain ID, client identifier, IdP identifier, and SP identifier

### XML Signature Security

Prevent XML Signature Wrapping attacks:

Schema Validation:
- Always perform schema validation before using XML for security purposes
- Use local, trusted copies of schemas for validation
- Never allow automatic schema downloads from third parties
- Inspect and harden schemas to disable wildcard or relaxed processing

Digital Signature Validation:
- For single signing key: use StaticKeySelector with key obtained directly from IdP
- For multiple signing keys: use X509KeySelector with keys stored in local JKS
- Ignore KeyInfo elements in documents
- For heterogeneous documents: implement full PKIX trust model with trusted root certificates

XML Processing Security:
- Never use getElementsByTagName to select security elements without validation
- Always use absolute XPath expressions to select elements
- Use hardened schemas for validation

### Protocol Processing Rules

Validate all required processing steps:

AuthnRequest Processing:
- Follow all SAML Core (3.4.1.4) processing rules
- Prevents man-in-the-middle attacks

Response Processing:
- Follow all SAML Profiles (4.1.4.3) processing rules
- Prevents stolen assertions, man-in-the-middle, forged assertions, and browser state exposure

### Binding Implementation Security

HTTP Redirect Binding:
- Follow SAML Binding (3.4) specifications
- Properly encode/decode messages

HTTP POST Binding:
- Follow SAML Binding (3.5) specifications
- Prevent caching of SAML messages to avoid stolen assertion and replay attacks

### Security Countermeasures

Additional protection measures:

IP Filtering:
- Filter by IP address when appropriate
- Provide separate endpoints for trusted partners
- Prevents stolen assertions and man-in-the-middle attacks

Response Lifetimes:
- Use short lifetimes on SAML responses
- Prevents stolen assertions and browser state exposure

OneTimeUse:
- Mark responses as OneTimeUse
- Prevents browser state exposure and replay attacks

### IdP-Initiated SSO Security

Unsolicited responses are inherently less secure due to lack of CSRF protection. If required:

- Follow SAML Profiles (4.1.5) validation process
- Validate RelayState URLs against allowlists to prevent open redirects
- Implement proper replay detection at response or assertion level

### Identity Provider Best Practices

- Validate X.509 certificates for algorithm compatibility and encryption strength
- Use strong authentication for SAML token generation
- Validate which IdP mints tokens
- Use trusted root CAs when possible
- Synchronize to common Internet time source
- Define levels of assurance for identity verification
- Use asymmetric identifiers over personally identifiable information
- Sign individual assertions or entire response elements

### Service Provider Best Practices

- Validate session state for users
- Ensure assertions or entire responses are signed
- Validate signatures are from authorized IdPs
- Validate IdP certificates for expiration and revocation (CRL/OCSP)
- Validate NotBefore and NotOnOrAfter timestamps
- Validate Recipient attributes
- Exchange assertions only over secure transports
- Define clear criteria for session management and SAML logout
- Verify user identities from SAML assertions when possible

### Input Validation

Treat all SAML input as untrusted external data:
- Perform proper input validation on all SAML providers and consumers
- Validate all elements and attributes in SAML messages
- Sanitize any data extracted from SAML assertions before use

### Cryptographic Requirements

- Use strong encryption for all SAML elements
- Deprecate support for insecure XMLEnc algorithms (e.g., RSA 1.5)
- Follow latest cryptoanalysis developments
- Use modern, secure cryptographic algorithms only

### Summary

Secure SAML implementation requires:
- TLS 1.2+ transport security with message signing and encryption
- Strict validation of all protocol elements and processing rules
- Protection against XML signature wrapping via schema validation and secure XML processing
- Proper binding implementation with caching prevention
- Security countermeasures including IP filtering, short lifetimes, and OneTimeUse
- Careful handling of IdP-initiated SSO with CSRF and replay protection
- Strong certificate validation and session management
- Comprehensive input validation and modern cryptography

SAML security depends on following specifications exactly and treating all inputs as potentially malicious.