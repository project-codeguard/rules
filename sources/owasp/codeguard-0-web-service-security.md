---
description: Web Service Security
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
- xml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Web Service Security

Secure web services through transport protection, authentication, input validation, and XML attack prevention.

### Transport Security

All web service communications with sensitive features or data must use well-configured TLS. TLS provides confidentiality, integrity protection, replay defenses, and server authentication.

Server certificate validation requirements:
- Issued by trusted provider
- Not expired or revoked
- Matches service domain name
- Proven private key ownership

### Authentication

- Avoid Basic Authentication; use Client Certificate Authentication with Mutual-TLS when appropriate
- Enforce consistent encoding styles between client and server

### Message Protection

For XML data requiring integrity beyond TLS:
- Use XML digital signatures with sender's private key
- Encrypt sensitive data with strong ciphers for both transport and at-rest protection when required

### Authorization

- Authorize clients for every web service method and request
- Check privileges for requested resources on every request
- Separate administrative functions from regular service endpoints
- Add challenge-response mechanisms for sensitive operations (password changes, contact details, payment instructions)

### Input Validation

Schema validation:
- Validate SOAP payloads against XML schema definition (XSD)
- Define maximum length and character sets for all parameters
- Use strong allow-list patterns for fixed format parameters (zip codes, phone numbers)

Content validation for XML input:
- Validate against malformed XML entities
- Validate against XML Bomb attacks
- Use strong allowlists for input validation
- Validate against external entity attacks

### XML Attack Protection

Configure XML parsers to protect against:
- Recursive payloads
- Oversized payloads
- XML entity expansion
- Overlong element names (SOAP Actions)

Build test cases to verify parser resistance to these attacks.

### Output Protection

Apply proper output encoding to prevent XSS when web service data is consumed by web clients.

### Resource Protection

- Limit SOAP message sizes to prevent DoS attacks
- Limit CPU cycles, memory usage, and simultaneous connections
- Optimize configuration for maximum message throughput
- Implement virus scanning for SOAP attachments before storage

### Compliance

Ensure compliance with Web Services-Interoperability (WS-I) Basic Profile for security baseline.