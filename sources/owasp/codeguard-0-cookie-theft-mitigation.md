---
description: Cookie Theft Mitigation Best Practices
languages:
- java
- javascript
- php
- python
- ruby
- typescript
alwaysApply: false
---

## Cookie Theft Mitigation Guidelines

This rule advises on detecting and mitigating session cookie theft through server-side monitoring:

- Session Fingerprinting
  - Store session environment information when sessions are established: IP address, User-Agent, Accept-Language, Date.
  - Save additional headers for enhanced detection: Accept, Accept-Encoding, sec-ch-ua headers (when available).
  - Associate fingerprint data with session ID for comparison on subsequent requests.

- Cookie Theft Detection
  - Monitor for significant changes in session environment information across requests.
  - Compare current request headers against stored session fingerprint data.
  - Account for legitimate variations (IP subnet changes, browser updates) vs. suspicious changes.
  - Use multiple detection vectors rather than relying on single header changes.

- Risk-Based Response to Anomalies
  - For high-risk operations: require re-authentication when suspicious changes detected.
  - For medium-risk operations: implement CAPTCHA challenges or additional verification.
  - For low-risk operations: log suspicious activity and continue monitoring.
  - Always regenerate session ID when potential hijacking is detected.

- Session Validation Implementation
  - Implement detection as middleware that runs before sensitive operations.
  - Apply validation selectively to high-value endpoints to manage performance impact.
  - Log all suspicious session activities with sufficient context for investigation.
  - Handle false positives gracefully to maintain user experience.

- Secure Session Storage
  - Store session fingerprint data securely on server-side (never client-side).
  - Use secure session storage mechanisms provided by your framework.
  - Ensure session data is properly encrypted and protected.

Code Example (from OWASP):
```js
const session = SessionStorage.create()
session.save({
  ip: req.clientIP,
  user_agent: req.headers.userAgent,
  date: req.headers.date,
  accept_language: req.headers.acceptLanguage,
  // ...
})

function cookieTheftDetectionMiddleware(req, res) {
  const currentIP = req.clientIP
  const expectedIP = req.session.ip
  if (checkGeoIPRange(currentIP, expected) === false) {
     // Validation
  }
  const currentUA = req.userAgent
  const expectedUA = req.session.ua
  if (checkUserAgent(currentUA, expectedUA)) {
    // Validation
  }
  // ...
}
```

Summary:  
Implement server-side session fingerprinting to detect cookie theft, monitor environment changes across requests, apply risk-based responses to suspicious activity, and maintain secure session storage. Consider future standards like Device Bound Session Credentials for enhanced protection.