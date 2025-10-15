---
description: Open Redirect Prevention - Secure handling of user-controlled redirects
  to prevent phishing attacks
languages:
- c
- javascript
- php
- typescript
- vlang
alwaysApply: false
version: 0.1.0
severity: medium
---

# Avoid Open Redirects

- Never use user input directly as a redirect target (e.g., `res.redirect(userInput)` in Node.js/Express).
- If redirection is controlled by user input:
    - Allow only local paths (must start with `/` and not contain protocols like `http:`).
    - OR: Allow only destinations present in a strict allowlist of trusted domains.
- URLs must be parsed and validated using robust libraries, not simple substring checks.
- DO NOT allow wildcard domains like `*.example.com` in any allowlist.
- Add explicit code comments when using redirects to document how the rule is being enforced.