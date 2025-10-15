---
description: OAuth 2.0 Security Best Practices
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## OAuth 2.0 Security Guidelines

Essential security practices for implementing secure OAuth 2.0 authorization flows and protecting against common attacks.

### Essential Basics

Prevent open redirectors that can enable token exfiltration:
- Clients and Authorization Servers must not expose URLs that forward the user's browser to arbitrary URIs obtained from query parameters
- Use exact string matching for redirect URI validation during client registration

Use proper CSRF protection:
- When Authorization Server supports PKCE, clients may rely on PKCE's CSRF protection
- In OpenID Connect flows, the "nonce" parameter provides CSRF protection
- Otherwise, use one-time CSRF tokens in the "state" parameter that are securely bound to the user agent

Prevent mix-up attacks in multi-Authorization Server environments:
- Use the issuer "iss" parameter as a countermeasure when interacting with multiple Authorization Servers
- Alternatively, use distinct redirect URIs to identify different authorization and token endpoints
- Authorization Servers should avoid accidentally forwarding requests containing user credentials

### PKCE - Proof Key for Code Exchange

PKCE mitigates authorization code interception attacks, especially for public clients:

- Use PKCE flow to prevent injection (replay) of authorization codes into authorization responses
- Use PKCE code challenge methods that do not expose the verifier in the authorization request
- Use S256 as the code challenge method instead of plain text
- Authorization servers must support PKCE and enforce correct "code_verifier" usage at the token endpoint
- Prevent PKCE downgrade attacks by accepting "code_verifier" only when "code_challenge" was present in the authorization request

### Authorization Code vs Implicit Grant

Prefer Authorization Code Grant over Implicit Grant:
- Use response type "code" (authorization code grant) or "code id_token" instead of implicit flows
- This allows the Authorization Server to detect replay attempts and reduces attack surface
- Access tokens are not exposed in URLs and can be sender-constrained

### Token Replay Prevention

Implement sender-constraining mechanisms:
- Use Mutual TLS for OAuth 2.0 or OAuth Demonstration of Proof of Possession (DPoP) to prevent token replays
- Implement refresh token rotation or ensure refresh tokens are sender-constrained

### Access Token Privilege Restriction

Apply the principle of least privilege:
- Restrict token privileges to the minimum required for the particular application or use case
- Implement audience restriction by associating access tokens with specific Resource Servers
- Resource Servers must verify that tokens were intended for their use
- Restrict tokens to specific resources and actions using "scope" and "authorization_details" parameters
- Use "scope" and "resource" parameters to determine the intended Resource Server

### Avoid Insecure Grant Types

Never use Resource Owner Password Credentials Grant:
- This grant type insecurely exposes Resource Owner credentials to the client
- Increases the attack surface of the application

### Client Authentication

Use strong authentication methods:
- Implement client authentication whenever possible
- Prefer asymmetric (public-key based) methods like mTLS or "private_key_jwt" (OpenID Connect)
- Asymmetric methods eliminate the need to store sensitive symmetric keys on Authorization Servers
- This approach is more robust against various attacks

### Additional Security Controls

Protect sensitive claims and enforce secure communications:
- Authorization Servers must not allow clients to influence their "client_id" or "sub" values
- Prevent clients from controlling any claims that could be confused with genuine Resource Owner data
- Use end-to-end TLS for all communications
- Never transmit authorization responses over unencrypted network connections
- Prohibit redirect URIs using "http" scheme except for native clients using Loopback Interface Redirection

### Implementation Summary

Secure OAuth 2.0 implementations require:
- PKCE implementation for all public clients
- Proper CSRF protection through state parameters or nonce
- Authorization Code Grant preference over Implicit Grant
- Token sender-constraining mechanisms (mTLS or DPoP)
- Strict privilege restriction and audience validation
- Strong client authentication using asymmetric methods
- Elimination of insecure grant types
- Comprehensive TLS enforcement and redirect URI validation

Following these practices ensures robust protection against authorization code interception, token replay, privilege escalation, and mix-up attacks while maintaining the flexibility and security benefits of OAuth 2.0.