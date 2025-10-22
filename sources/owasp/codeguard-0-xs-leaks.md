---
description: Preventing Cross-Site Leaks (XS-Leaks)
languages:
- c
- javascript
- typescript
alwaysApply: false
---

Protecting your applications from Cross-Site Leaks is crucial for safeguarding user privacy. XS-Leaks are a class of vulnerabilities that exploit subtle browser behaviors to extract sensitive user information across origins. 

XS-Leaks occur when an attacker's website can infer information about a user's state on another website through side-channels like:

- Error messages
- Frame counting
- Resource timing
- Cache probing
- Response size detection

These attacks can reveal sensitive information such as whether a user is logged in, specific account details, or even extract data from cross-origin resources.

Properly configured cookies are your first line of defense against XS-Leaks. For example:

```javascript
// Setting cookies in JavaScript with secure attributes
document.cookie = "sessionId=abc123; SameSite=Strict; Secure; HttpOnly; Path=/";
```

For server-side cookie setting (example in Express.js):

```javascript
app.use(session({
  secret: 'your-secret-key',
  cookie: {
    sameSite: 'strict',  // Options: strict, lax, none
    secure: true,         // Requires HTTPS
    httpOnly: true        // Prevents JavaScript access
  }
}));
```

In your HTTP response headers:

```http
Set-Cookie: sessionId=abc123; SameSite=Strict; Secure; HttpOnly; Path=/
```



* Always specify a `SameSite` attribute:
  * Use `SameSite=Strict` for cookies related to sensitive actions
  * Use `SameSite=Lax` for cookies needed on normal navigation to your site
  * Use `SameSite=None; Secure` only when third-party usage is absolutely required

* Never rely on browser defaults as they may vary across browsers and versions

### Framing Protection

Prevent your site from being framed by potentially malicious sites:

```javascript
// In your Express.js application
app.use((req, res, next) => {
  // CSP frame-ancestors directive (modern approach)
  res.setHeader(
    'Content-Security-Policy',
    "frame-ancestors 'self' https://trusted-parent.com"
  );
  
  // X-Frame-Options (legacy fallback)
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  
  next();
});
```

Use Fetch Metadata headers to detect and block suspicious cross-origin requests:

```javascript
// Express.js middleware for protecting sensitive endpoints
function secureEndpoint(req, res, next) {
  // Get Fetch Metadata headers
  const fetchSite = req.get('Sec-Fetch-Site') || 'unknown';
  const fetchMode = req.get('Sec-Fetch-Mode') || 'unknown';
  const fetchDest = req.get('Sec-Fetch-Dest') || 'unknown';
  
  // Block cross-site requests to sensitive endpoints
  if (fetchSite === 'cross-site' && req.path.startsWith('/api/sensitive')) {
    return res.status(403).send('Cross-site requests not allowed');
  }
  
  // Block embedding in iframes from untrusted sites
  if (fetchDest === 'iframe' && fetchSite === 'cross-site') {
    return res.status(403).send('Embedding not allowed');
  }
  
  next();
}

app.use(secureEndpoint);
```

### Secure Cross-Origin Communication

When using `postMessage` for cross-origin communication:

```javascript
// UNSAFE - Never do this
window.postMessage(sensitiveData, '*');

// SAFE - Always specify the exact target origin
window.postMessage(sensitiveData, 'https://trusted-receiver.com');

// When receiving messages, always verify the origin
window.addEventListener('message', (event) => {
  // Always verify message origin
  if (event.origin !== 'https://trusted-sender.com') {
    console.error('Received message from untrusted origin:', event.origin);
    return;
  }
  
  // Process the message
  processMessage(event.data);
});
```

### Isolating Browsing Contexts

Use Cross-Origin-Opener-Policy (COOP) to isolate your site from potential attackers:

```http
Cross-Origin-Opener-Policy: same-origin
```

In Express.js:

```javascript
app.use((req, res, next) => {
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  next();
});
```

For maximum isolation, combine with Cross-Origin-Embedder-Policy (COEP):

```javascript
app.use((req, res, next) => {
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  next();
});
```

### Preventing Cache-Based Leaks

Protect sensitive resources from cache probing attacks:

```javascript
// Express.js middleware for sensitive endpoints
app.get('/api/sensitive-data', (req, res) => {
  // Add user-specific token to prevent cache probing
  const userToken = req.user.securityToken;
  
  // Disable caching for sensitive resources
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Pragma', 'no-cache');
  
  // Add user token to response to ensure uniqueness
  const data = { userToken, sensitiveData: 'secret information' };
  res.json(data);
});
```

For static resources that might reveal user state:

```javascript
// Add user-specific tokens to URLs of sensitive resources
function getUserSpecificUrl(baseUrl) {
  const userToken = generateUserToken();
  return `${baseUrl}?token=${userToken}`;
}

const profileImageUrl = getUserSpecificUrl('/images/profile.jpg');
```

### Comprehensive Defense Strategy

Implement these headers for a robust defense against XS-Leaks:

```javascript
app.use((req, res, next) => {
  // Framing protection
  res.setHeader('Content-Security-Policy', "frame-ancestors 'self'");
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  
  // Resource isolation
  res.setHeader('Cross-Origin-Resource-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  
  // Cache control for dynamic content
  if (req.path.startsWith('/api/')) {
    res.setHeader('Cache-Control', 'no-store');
  }
  
  next();
});
```