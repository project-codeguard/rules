---
description: REST API Security Guidelines
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
- yaml
alwaysApply: false
---

## REST API Security Guidelines

Essential security practices for developing secure RESTful web services, covering transport security, authentication, input validation, and proper error handling.

### Core REST Security Principles

REST APIs are stateless - each request must contain all necessary information for processing. State refers to resource state, not session state. Avoid passing client state to backend as this creates replay and impersonation attack vectors.

Each REST endpoint must independently verify authorization for the requested operation on the specific resource.

### HTTPS Requirements

Secure REST services must only provide HTTPS endpoints to protect:
- Authentication credentials (passwords, API keys, JSON Web Tokens)
- Data integrity and confidentiality
- Client authentication of the service

Consider mutually authenticated client-side certificates for highly privileged web services.

### Access Control

Non-public REST services must perform access control at each API endpoint:
- Take access control decisions locally at REST endpoints to minimize latency
- Use centralized Identity Provider (IdP) for user authentication that issues access tokens
- Avoid relying on global session state across distributed services

### JWT Security

When using JSON Web Tokens for security tokens:

Essential Requirements:
- Ensure JWTs are integrity protected by signature or MAC
- Never allow unsecured JWTs with `{"alg":"none"}`
- Prefer signatures over MACs for integrity protection
- Verify JWT integrity based on local configuration, not JWT header information

Standard Claims Validation:
- `iss` (issuer): Verify trusted issuer and signing key ownership
- `aud` (audience): Confirm relying party is in target audience
- `exp` (expiration): Validate current time is before token expiration
- `nbf` (not before): Validate current time is after token validity start

Token Revocation:
- Implement JWT denylist for explicit session termination
- Submit hash of revoked JWTs to denylist until natural expiration

### API Keys

For public REST services requiring access control:
- Require API keys for every request to protected endpoints
- Return `429 Too Many Requests` for rate limit violations
- Revoke API keys for usage agreement violations
- Do not rely exclusively on API keys for sensitive or high-value resources

### HTTP Method Restrictions

- Apply allowlist of permitted HTTP methods (GET, POST, PUT, DELETE)
- Reject unauthorized methods with `405 Method not allowed`
- Verify caller authorization for specific HTTP method on resource
- Be especially careful with Java EE HTTP verb tampering vulnerabilities

### Input Validation

Never trust input parameters or objects:
- Validate input length, range, format, and type
- Use strong types (numbers, booleans, dates) for implicit validation
- Constrain string inputs with regular expressions
- Reject unexpected or illegal content
- Define appropriate request size limits, return `413 Request Entity Too Large`
- Log input validation failures for attack detection
- Use secure parsers resistant to XXE and similar attacks

### Content Type Validation

Request Validation:
- Reject requests with unexpected or missing Content-Type headers (`406 Unacceptable` or `415 Unsupported Media Type`)
- Allow missing Content-Type only for Content-Length: 0 requests
- Explicitly define supported content types in framework configurations
- Ensure XML parser hardening against XXE attacks

Response Security:
- Never copy Accept header directly to Content-Type response header
- Reject requests with unsupported Accept headers (`406 Not Acceptable`)
- Send intended content type headers matching response body content

### Management Endpoints

- Avoid exposing management endpoints via Internet
- Require strong authentication (multi-factor) if Internet-accessible
- Use different HTTP ports, hosts, or network interfaces
- Restrict access via firewall rules or access control lists

### Error Handling

- Respond with generic error messages
- Never reveal technical details (call stacks, internal hints) to clients
- Avoid exposing system information that aids attackers

### Audit Logging

- Write audit logs before and after security-related events
- Log token validation errors for attack detection
- Sanitize log data to prevent log injection attacks

### Security Headers

Include these headers in all API responses:

Required Headers:
- `Cache-Control: no-store`: Prevents sensitive information caching
- `Content-Security-Policy: frame-ancestors 'none'`: Prevents clickjacking
- `Content-Type`: Specify correct content type to prevent MIME sniffing
- `Strict-Transport-Security`: Enforce HTTPS-only access
- `X-Content-Type-Options: nosniff`: Prevent MIME type confusion
- `X-Frame-Options: DENY`: Additional clickjacking protection

### CORS Configuration

- Disable CORS headers if cross-domain calls are not required
- Be as specific as possible when setting allowed origins
- Avoid wildcard origins in production environments

### Sensitive Information Protection

Never include sensitive data in URLs:
- Use request body or headers for POST/PUT sensitive data
- Use HTTP headers for GET request sensitive data
- Avoid query parameters for passwords, tokens, or API keys
- URLs may be logged by web servers, proxies, and browsers

### HTTP Status Codes

Use semantically appropriate status codes:
- `200 OK`: Successful operations
- `201 Created`: Resource creation with Location header
- `400 Bad Request`: Malformed requests
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authorization failed
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: HTTP method not supported
- `406 Not Acceptable`: Unsupported Accept header
- `413 Payload Too Large`: Request size exceeded
- `415 Unsupported Media Type`: Unsupported Content-Type
- `429 Too Many Requests`: Rate limiting triggered
- `500 Internal Server Error`: Generic server error (no details)

### Implementation Summary

Secure REST API development requires:
- HTTPS-only endpoints with proper certificate validation
- Stateless design with per-endpoint authorization
- Secure JWT handling with proper validation and revocation
- Comprehensive input validation and content type enforcement
- Protected management interfaces with strong authentication
- Generic error responses without information disclosure
- Complete audit logging with injection prevention
- Appropriate security headers for defense in depth
- Careful CORS configuration and sensitive data handling
- Semantically correct HTTP status codes for proper client behavior