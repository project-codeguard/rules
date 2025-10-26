---
description: Content Security Policy (CSP) Best Practices
languages:
- c
- html
- javascript
- php
- typescript
alwaysApply: false
---

## Content Security Policy (CSP): A Defense-in-Depth Strategy

Implementing a strong Content Security Policy (CSP) is one of the most effective ways to mitigate cross-site scripting (XSS), clickjacking, and other injection attacks. CSP works by declaring which dynamic resources are allowed to load, effectively creating an allowlist that the browser enforces.

### Implementation

#### 1. Deliver CSP via HTTP Headers

The most effective way to implement CSP is through HTTP response headers:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com;
```

When testing a new policy, use the report-only mode to monitor without blocking:

```http
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self';
```

**Note:** Avoid using the meta tag approach (`<meta http-equiv="Content-Security-Policy"...>`) except when you cannot modify HTTP headers, as it provides less protection and doesn't support all directives.

#### 2. Adopt a Strict CSP Strategy

Modern CSP best practices favor nonce-based or hash-based approaches over domain whitelisting:

**Nonce-based approach:**

```http
Content-Security-Policy: script-src 'nonce-random123' 'strict-dynamic';
```

With corresponding HTML:

```html
<script nonce="random123">alert('Hello');</script>
```

**Important:** Generate a unique, cryptographically strong nonce for each page load. The nonce should be at least 128 bits of entropy encoded in base64.

**Server-side nonce generation examples:**

```javascript
// Node.js: crypto.randomBytes(16).toString('base64')
// Python: base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
```

**Hash-based alternative:**
```http
Content-Security-Policy: script-src 'sha256-hashOfYourScriptContent' 'strict-dynamic';
```

#### 3. Baseline CSP for Getting Started

```http
Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'self'; form-action 'self'; object-src 'none'; base-uri 'none'; upgrade-insecure-requests;
```

This policy:
- Restricts resources to the same origin
- Allows inline styles (necessary for many applications initially)
- Prevents clickjacking by controlling framing
- Limits form submissions to the same origin
- Blocks plugin content (Flash, Java applets)
- Prevents base tag injection attacks
- Automatically upgrades HTTP requests to HTTPS (when `upgrade-insecure-requests` is used)

#### 4. Refactor Your Code for CSP Compatibility

To make CSP implementation easier:

1. **Move inline code to external files:**
   ```html
   <!-- Instead of this -->
   <button onclick="doSomething()">

   <!-- Do this -->
   <button id="myButton">
   <script src="buttons.js"></script> <!-- With event listeners -->
   ```

2. **Eliminate inline styles:**
   ```html
   <!-- Instead of this -->
   <div style="color: red">

   <!-- Do this -->
   <div class="red-text">
   ```

#### 5. Key CSP Directives You Should Know

- **`default-src`**: The fallback for other fetch directives
- **`script-src`**: Controls JavaScript sources
- **`style-src`**: Controls CSS sources - use `'self'` for external stylesheets, add `'unsafe-inline'` only if needed for inline styles
- **`img-src`**: Controls image sources
- **`connect-src`**: Controls fetch, XHR, WebSocket connections
- **`object-src`**: Controls `<object>`, `<embed>`, and `<applet>` elements - set to `'none'` to block Flash/plugins
- **`frame-ancestors`**: Controls which sites can embed your pages (replaces X-Frame-Options) - use `'none'` to prevent all framing
- **`form-action`**: Controls where forms can be submitted
- **`upgrade-insecure-requests`**: Automatically upgrades HTTP requests to HTTPS

#### 6. Enable Violation Reporting

Set up a reporting endpoint to collect CSP violations:

```http
Content-Security-Policy: default-src 'self'; report-uri https://your-domain.com/csp-reports;
```

#### 7. Implementation Steps

1. Start with `Content-Security-Policy-Report-Only`
2. Analyze violation reports
3. Gradually tighten policy
4. Switch to enforcing mode
5. Continue monitoring

Remember that CSP is a defense-in-depth measure. It complements, but does not replace, proper input validation, output encoding, and other secure coding practices.