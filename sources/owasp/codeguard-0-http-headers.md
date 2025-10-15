---
description: HTTP Security Headers Best Practices
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

## HTTP Security Headers Guidelines

This rule enforces secure configuration of HTTP response headers to protect against common web vulnerabilities including XSS, Clickjacking, Information Disclosure, and MIME-type attacks.

### Required Security Headers

1. Content Security Policy (CSP)
   - Must include default-src directive
   - Must include script-src directive with appropriate restrictions
   - Must include frame-ancestors directive for clickjacking protection
   - Example: `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; frame-ancestors 'none'`

2. Cookie Security
   - All session/sensitive cookies must have Secure flag
   - All session/sensitive cookies must have HttpOnly flag
   - All cookies must have SameSite attribute (Strict or Lax)
   - Example: `Set-Cookie: session=123; Secure; HttpOnly; SameSite=Strict`

3. Cross-Origin Isolation
   - Must set Cross-Origin-Embedder-Policy (COEP)
   - Must set Cross-Origin-Resource-Policy (CORP)
   - Must set Cross-Origin-Opener-Policy (COOP)
   - Examples:
     ```
     Cross-Origin-Embedder-Policy: require-corp
     Cross-Origin-Resource-Policy: same-origin
     Cross-Origin-Opener-Policy: same-origin
     ```

4. Transport Security
   - Must set Strict-Transport-Security (HSTS)
   - Must include appropriate max-age (minimum 1 year)
   - Example: `Strict-Transport-Security: max-age=31536000; includeSubDomains`

5. Cache Control
   - Must set appropriate Cache-Control for sensitive data
   - Example: `Cache-Control: no-store, max-age=0`

6. Content Type Protection
   - Must set X-Content-Type-Options
   - Example: `X-Content-Type-Options: nosniff`

### Prohibited Headers

The following headers must not be present or must be removed:
- X-Powered-By
- Server (or must contain non-revealing value)
- X-AspNet-Version
- X-AspNetMvc-Version

### Required Header Combinations

Certain security features require multiple headers to work effectively:

1. Clickjacking Protection:
   - Must use CSP frame-ancestors OR
   - Must use X-Frame-Options: DENY

2. XSS Protection:
   - Must use CSP with appropriate script-src
   - Must not rely solely on X-XSS-Protection

3. CORS Security:
   - Must not use Access-Control-Allow-Origin: *
   - Must explicitly list allowed origins

### Implementation Examples

PHP:
```php
header("X-Frame-Options: DENY");
```

Apache (.htaccess):
```apache
<IfModule mod_headers.c>
Header always set X-Frame-Options "DENY"
</IfModule>
```

IIS (Web.config):
```xml
<system.webServer>
...
 <httpProtocol>
   <customHeaders>
     <add name="X-Frame-Options" value="DENY" />
   </customHeaders>
 </httpProtocol>
...
</system.webServer>
```

HAProxy:
```
http-response set-header X-Frame-Options DENY
```

Nginx:
```nginx
add_header "X-Frame-Options" "DENY" always;
```

Express.js:
```javascript
const helmet = require('helmet');
const app = express();
// Sets "X-Frame-Options: SAMEORIGIN"
app.use(
 helmet.frameguard({
   action: "sameorigin",
 })
);
```

### Testing Tools

Mozilla Observatory is an online tool which helps you to check your website's header status.

SmartScanner has a dedicated test profile for testing security of HTTP headers. Online tools usually test the homepage of the given address. But SmartScanner scans the whole website, ensuring all web pages have the right HTTP Headers in place.