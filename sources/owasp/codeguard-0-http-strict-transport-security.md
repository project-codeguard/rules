---
description: HTTP Strict Transport Security Best Practices
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

## HTTP Strict Transport Security Guidelines

This rule enforces secure configuration of HTTP Strict Transport Security (HSTS) headers to protect users by ensuring all communications occur over HTTPS.

### Introduction

HTTP Strict Transport Security (HSTS) is an opt-in security enhancement specified by a web application through a special response header. Once a supported browser receives this header, it prevents any communications from being sent over HTTP to the specified domain and instead sends all communications over HTTPS. It also prevents HTTPS click through prompts on browsers.

Critical Requirement: The Strict-Transport-Security header is only honored over HTTPS connections and is completely ignored when sent over HTTP, per RFC 6797.

### Threats Addressed

HSTS protects against:
- Man-in-the-middle attacks when users bookmark or manually type `http://example.com`
- Web applications inadvertently containing HTTP links or serving content over HTTP
- Man-in-the-middle attackers using invalid certificates (HSTS prevents users from accepting bad certificates)

### Required Configuration

1. Basic HSTS Header (testing phase):
   ```
   Strict-Transport-Security: max-age=86400; includeSubDomains
   ```

2. Production HSTS Header (1 year minimum):
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains
   ```

3. Preload-Ready HSTS Header:
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ```

### Phased Rollout Requirements

1. Phase 1 - Testing (recommended first step):
   - Use short max-age (600-86400 seconds) for initial testing
   - Monitor for any HTTP content or functionality issues

2. Phase 2 - Production:
   - Increase max-age to minimum 1 year (31536000 seconds)
   - Add `includeSubDomains` only if all subdomains support HTTPS

3. Phase 3 - Preload (optional):
   - Add `preload` directive only after thorough testing
   - Submit domain to HSTS preload list at hstspreload.org
   - Warning: Preload is effectively permanent and affects all subdomains

### Implementation Examples

Simple example using 1 year max-age (dangerous without includeSubDomains):
```
Strict-Transport-Security: max-age=31536000
```

Secure example with subdomain protection:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

Short max-age for initial rollout testing:
```
Strict-Transport-Security: max-age=86400; includeSubDomains
```

### Monitoring and Validation

Required post-deployment actions:
- Verify HSTS header presence in all HTTPS responses
- Monitor browser console for mixed content warnings
- Audit all internal links and redirects for HTTP references
- Test subdomain HTTPS availability before enabling includeSubDomains
- Use tools like Mozilla Observatory or Security Headers to validate configuration

### Browser Support

HSTS is supported by all modern browsers. The only notable exception is Opera Mini.