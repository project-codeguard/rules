---
description: Security Questions Implementation Guidelines
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

Security questions are no longer considered a strong authentication factor in authentication systems. Modern best practices strongly recommend against using them as a standalone method for authentication or account recovery.

### Preferred Alternatives to Security Questions

*   **Multi-Factor Authentication (MFA):** Implement time-based one-time passwords (TOTP), push notifications, or hardware security keys as your primary account recovery mechanism.
*   **One-Time Recovery Codes:** Generate and provide users with a set of single-use recovery codes when they set up their account.
*   **Email-Based Recovery:** Send a time-limited, single-use recovery link to a verified email address.

### If You Must Use Security Questions (Legacy Systems)

If your organization requires security questions for legacy or compliance reasons, implement these critical safeguards:

#### 1. Question Selection

*   **Provide a Curated List:** Offer a predefined set of strong questions rather than allowing free-form user-created ones.
*   **Question Quality:** Choose questions that are:
    *   **Memorable:** Users can consistently recall the answer over time.
    *   **Stable:** The answer doesn't change over the user's lifetime.
    *   **Confidential:** Not easily discoverable through social media or public records.
    *   **Specific:** Has a single, precise answer rather than multiple possible answers.

#### 2. Answer Handling

*   **Secure Storage:** Hash all answers using Argon2id or bcrypt with per-answer unique salt and system-wide pepper. Store data encrypted at rest with AES-256.
*   **Normalization:** Before comparing answers, normalize them by removing extra spaces, converting to lowercase, and removing punctuation.
*   **Input Validation:**
    *   Enforce a minimum length but allow legitimate short answers.
    *   Implement a denylist for weak answers like "password", "123456", or the user's own username/email.

#### 3. Implementation Best Practices

*   **Multi-Layered Security:** Use multiple questions together for increased security.
*   **Consistent Question:** When a user fails to answer correctly, don't rotate to a different question—this helps prevent attackers from learning all the answers through multiple attempts.
*   **Brute-Force Protection:** Implement rate limiting (max 5 attempts per hour), progressive delays, CAPTCHA after 3 failed attempts, and account lockout to prevent automated attacks.
*   **Verify Email First:** Always verify ownership of the recovery email address before presenting security questions.
*   **Require Authentication:** Require re-authentication (password or MFA) before allowing users to change their security questions or answers.
*   **Secure Transport:** Use HTTPS/TLS 1.3+ for all recovery endpoints and implement certificate pinning where possible to prevent man-in-the-middle attacks.

By following these guidelines, you can minimize the risks associated with security questions while working toward implementing more secure authentication methods.