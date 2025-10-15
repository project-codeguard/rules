---
description: Credential Stuffing Prevention Best Practices
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
version: 0.1.0
severity: medium
---

## Defending Against Credential Stuffing and Password Spraying Attacks

When implementing authentication systems, defend against automated attacks that leverage stolen credentials. These attacks are increasingly sophisticated, and a layered defense strategy is essential.

| Attack Type | Description |
|-------------|-------------|
| Brute Force | Testing multiple passwords from dictionary or other source against a single account |
| Credential Stuffing | Testing username/password pairs obtained from the breach of another site |
| Password Spraying | Testing a single weak password against a large number of different accounts |

MFA is your most effective defense against credential stuffing attacks. Even if attackers have valid credentials, MFA creates a significant barrier.

### 1. Multi-Factor Authentication (MFA): Primary Defense

MFA stops 99.9% of credential-based attacks. Implement risk-based MFA that triggers on:
- New devices or locations
- Proxy/VPN usage
- Recent failed login attempts
- High-risk actions (admin changes, financial transactions)

Always require MFA for administrative functions and sensitive operations.

### 2. Layered Controls: Defense in Depth

* **CAPTCHA:** Trigger based on failed attempts (≥3), proxy/VPN IPs, bot user agents, or high-velocity traffic.

* **Rate Limiting:** Implement multiple layers:
  - Per-IP limits (3-15 attempts based on reputation)
  - Per-user limits (5 attempts per account)
  - Global limits to detect distributed attacks
  - Temporary blocks with automatic expiration

* **Device Fingerprinting:** Track user-agent, language, screen resolution, and TLS fingerprints to detect anomalous patterns.

* **Unpredictable Usernames:** Avoid email addresses as usernames; use generated, non-sequential identifiers.

### 3. Additional Defenses

* **Multi-Step Login:** Require JavaScript token generation or CSRF tokens to complicate automated tools.

* **Breached Password Detection:** Check new passwords against breach databases using [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3) and reject passwords found in data breaches.

* **User Notifications:** Alert users about successful logins from new devices and provide session management dashboards.

### 4. Monitoring and Alerting

* **Attack Detection:** Monitor for:
  - High failed login volumes (>100/min)
  - Many unique attacking IPs (>50/min)
  - Abnormal CAPTCHA solve rates (>95%)
  - Distributed attacks from hosting providers

* **Impossible Travel Detection:** Alert when users appear to login from distant locations within impossible timeframes (faster than commercial flight speed).

* **Breach Intelligence:** Integrate with [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3) to detect newly compromised credentials.

These layered defenses significantly increase attack cost while maintaining good user experience.