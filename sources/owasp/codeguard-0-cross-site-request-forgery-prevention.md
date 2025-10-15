---
description: Cross-Site Request Forgery (CSRF) Prevention Best Practices
languages:
- c
- go
- html
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

## Introduction

A Cross-Site Request Forgery (CSRF) attack occurs when a malicious web site, email, blog, instant message, or program tricks an authenticated user's web browser into performing an unwanted action on a trusted site. If a target user is authenticated to the site, unprotected target sites cannot distinguish between legitimate authorized requests and forged authenticated requests.

**IMPORTANT: Remember that Cross-Site Scripting (XSS) can defeat all CSRF mitigation techniques!** Consider the client and authentication method to determine the best approach for CSRF protection in your application.

## Preventing Cross-Site Request Forgery (CSRF) Attacks

### Implementation Best Practices

#### 1. Fix XSS Vulnerabilities First

Cross-Site Scripting (XSS) vulnerabilities can bypass CSRF protections. Always address XSS issues alongside CSRF mitigations.

#### 2. Use Framework-Native CSRF Protection

Use framework built-in CSRF protection with correct implementation:

* **Angular**: Configure HttpClient with XSRF protection:
  ```typescript
  // app.config.ts
  provideHttpClient(withXsrfConfiguration({
    cookieName: 'XSRF-TOKEN',
    headerName: 'X-XSRF-TOKEN'
  }))
  ```

* **Next.js**: Use csrf middleware in API routes:
  ```javascript
  // pages/api/protected.js
  import { csrf } from 'csrf';
  export default csrf(async (req, res) => {
    // Your protected endpoint logic
  });
  ```

* **Spring Security**: Enable CSRF protection properly:
  ```java
  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
      return http.csrf(Customizer.withDefaults()).build(); // CSRF enabled by default
    }
  }
  ```

* **Django**: Use CSRF middleware and template tags:
  ```python
  # settings.py - ensure CsrfViewMiddleware is enabled
  MIDDLEWARE = ['django.middleware.csrf.CsrfViewMiddleware', ...]
  ```

#### 3. Implement the Synchronizer Token Pattern

Generate unique, unpredictable tokens per session:

```javascript
// Token generation: use HMAC with session ID + secret
const csrfToken = crypto.createHmac('sha256', process.env.CSRF_SECRET)
  .update(req.session.id).digest('hex');
```

**Form submissions**: Include token as hidden field:
```html
<input type="hidden" name="_csrf" value="{{csrfToken}}">
```

**AJAX requests**: Send token in custom header:
```javascript
headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content }
```

#### 4. Protect All State-Changing Requests

* **Never use GET for state changes**: All operations that change state should use POST, PUT, DELETE, or PATCH.
* **Validate tokens on all unsafe methods**: Verify CSRF tokens on every state-changing request.

#### 5. Secure Token Transmission and Storage

**Mandatory HTTPS**: Always enforce HTTPS for CSRF token transmission:
```javascript
// Redirect HTTP to HTTPS
app.use((req, res, next) => {
  if (!req.secure && process.env.NODE_ENV === 'production') {
    return res.redirect(`https://${req.headers.host}${req.url}`);
  }
  next();
});
```

**Secure Cookie Configuration**: Use proper cookie attributes for CSRF tokens and sessions:
```http
Set-Cookie: __Host-XSRF-TOKEN=abc123; Path=/; Secure; SameSite=Lax
Set-Cookie: __Host-sessionid=xyz789; Path=/; Secure; HttpOnly; SameSite=Lax
```

Cookie attribute requirements:
* **Secure**: Mandatory - prevents transmission over HTTP
* **SameSite=Lax**: Balances security and usability; use `Strict` for high-security applications
* **__Host- prefix**: Prevents subdomain cookie injection attacks
* **HttpOnly**: For session cookies only (CSRF tokens need JavaScript access)

#### 6. Defense-in-Depth Strategies

**Combine Multiple Protections**: Layer CSRF tokens with origin validation and rate limiting:

```javascript
// Comprehensive CSRF protection middleware
function csrfProtection(req, res, next) {
  // 1. Validate Origin/Referer headers
  const origin = req.headers.origin || req.headers.referer;
  if (!origin || !isValidOrigin(origin)) {
    return res.status(403).json({error: 'Invalid origin'});
  }
  
  // 2. Validate CSRF token
  const token = req.headers['x-csrf-token'] || req.body._csrf;
  if (!isValidCsrfToken(token, req.session.id)) {
    return res.status(403).json({error: 'Invalid CSRF token'});
  }
  
  // 3. Rate limiting per session
  if (exceedsRateLimit(req.session.id)) {
    return res.status(429).json({error: 'Rate limit exceeded'});
  }
  
  next();
}

function isValidOrigin(origin) {
  const allowedOrigins = ['https://yourdomain.com', 'https://app.yourdomain.com'];
  return allowedOrigins.includes(new URL(origin).origin);
}
```

**Token-Based Authentication (SPAs)**: For SPAs using JWT/bearer tokens:
```javascript
// Custom header approach for token-based auth
function apiCsrfProtection(req, res, next) {
  // Require custom header for state-changing operations
  if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(req.method)) {
    if (!req.headers['x-requested-with']) {
      return res.status(403).json({error: 'Missing required header'});
    }
  }
  next();
}
```

#### 7. Special Cases

**Login CSRF Protection**: Use pre-session tokens for login forms:
```javascript
// Generate token before authentication, destroy session after login
const loginToken = crypto.randomBytes(32).toString('hex');
req.session.loginCsrfToken = loginToken;
```

**Client-Side CSRF Prevention**: Validate input sources in JavaScript:
```javascript
// Avoid using URL parameters/fragments for generating requests
// Validate endpoint URLs against allow-lists before making requests
const allowedEndpoints = ['/api/profile', '/api/settings'];
if (!allowedEndpoints.includes(requestEndpoint)) {
  throw new Error('Invalid endpoint');
}
```

#### 8. Testing and Validation

Essential CSRF defense tests:
* Cross-origin form submissions should be blocked
* CSRF tokens must be validated on all state-changing requests  
* Test with various SameSite cookie settings
* Verify Origin/Referer header validation works correctly

These layered defenses provide robust CSRF protection while maintaining usability.