---
description: Authentication Security Best Practices
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

Secure authentication is one of the most critical aspects of application development.

- Use non-public, random, and unique identifiers for users internally. For login, allow users to use their verified email address or a username, but ensure error messages are generic (e.g., "Invalid username or password") to prevent attackers from guessing valid accounts.
- Implement proper password strength controls: minimum 8 characters, maximum 64+ characters to support passphrases, allow all characters including unicode and whitespace, and avoid composition rules (no requirements for uppercase/lowercase/numbers/special characters).
- Block common and previously breached passwords using services like HaveIBeenPwned's Pwned Passwords API, and include a password strength meter to help users create stronger passwords.
- Store user passwords using a modern, strong, and slow hashing algorithm like Argon2 (preferred) or bcrypt with recommended parameters. Use a unique salt for each user.
- Support Password Managers: Use standard `<input type="password">` fields and allow pasting to ensure compatibility with password managers.
- Use TLS Everywhere: All communication transmitting credentials, session tokens, or any sensitive data must be over HTTPS.
- When comparing password hashes, use a secure, constant-time comparison function to prevent timing attacks.
- Protect against automated attacks: implement account lockout after failed login attempts, use CAPTCHA to prevent brute force attacks, and consider rate limiting on authentication endpoints.
- Require multi-factor authentication (MFA) using TOTP (authenticator apps) or WebAuthn (hardware keys) for sensitive accounts. Consider making MFA mandatory for all users.
- Implement secure session management: use HttpOnly and Secure flags for session cookies, rotate session IDs after login, and set appropriate session timeouts.
- Before a user can change their password, require them to re-enter their current password. Require re-authentication for all sensitive features and transactions (password changes, email updates, financial transactions).
- Implement secure password recovery mechanisms that don't reveal whether an account exists ("If that email address is in our database, we will send you an email to reset your password").
- Enable comprehensive logging and monitoring: log all authentication failures, successful logins, account lockouts, and password changes for security monitoring and incident response.
- Internal or administrative accounts should not be accessible from public login forms. Use a separate, more secure authentication system for internal users.
- For delegated or federated authentication, use established protocols like OAuth 2.0, OpenID Connect (OIDC), or SAML. DO NOT build your own.