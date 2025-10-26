---
description: Forgot Password Security Best Practices
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

## Forgot Password Security Guidelines

This rule advises on secure password reset implementation to prevent user enumeration, token abuse, and unauthorized access:

- Password Reset Request Security
  - Return consistent messages for both existent and non-existent accounts to prevent user enumeration.
  - Ensure consistent response times by using asynchronous processing or identical code paths.
  - Implement rate limiting per account and IP address to prevent flooding attacks.
  - Apply input validation and SQL injection prevention to reset request forms.
  - Use CSRF tokens to protect password reset forms and endpoints.

- Token Generation and Storage
  - Generate tokens using cryptographically secure random number generators.
  - Make tokens sufficiently long to protect against brute-force attacks (minimum 32 bytes).
  - Store password reset tokens securely using hashing (same practices as password storage).
  - Link tokens to individual users in the database with expiration times.
  - Make tokens single-use and invalidate immediately after successful use.

- Password Reset Process Security
  - Require users to confirm new passwords by entering twice.
  - Enforce consistent password policy throughout the application.
  - Store new passwords following secure password storage practices.
  - Send confirmation emails without including the actual password.
  - Never automatically log users in after password reset.
  - Invalidate all existing user sessions after successful password reset.

- URL Token Implementation
  - Generate secure tokens and attach to URL query strings for email delivery.
  - Use hardcoded or validated trusted domains for reset URLs (avoid Host header injection).
  - Enforce HTTPS for all password reset URLs.
  - Add referrer policy with 'noreferrer' value to prevent referrer leakage.
  - Implement rate limiting to prevent token brute-forcing attempts.

- PIN Implementation
  - Generate PINs between 6-12 digits using cryptographically secure methods.
  - Create limited sessions from PINs that only permit password reset operations.
  - Format PINs with spaces for better user readability.
  - Apply same security practices as tokens (single-use, expiration, secure storage).

- Security Questions Integration
  - Use security questions only as additional layer, never as sole mechanism.
  - Follow secure question selection practices from OWASP guidance.
  - Validate security question answers using secure comparison methods.

- Logging and Monitoring (Code-Level)
  - Log password reset attempts with user context but never log tokens or passwords.
  - Implement structured logging for security monitoring integration.
  - Include sufficient context for security analysis (IP, user agent, timestamp).
  - Never log sensitive information in application logs.

- Account Lockout Prevention
  - Never lock accounts in response to password reset requests.
  - Implement alternative abuse prevention through rate limiting and monitoring.
  - Separate password reset abuse protection from authentication lockout mechanisms.

Summary:  
Implement secure password reset functionality through consistent response handling, cryptographically secure token generation and storage, CSRF protection, proper session management, and comprehensive logging while preventing user enumeration and account lockout attacks.