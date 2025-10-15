---
description: AJAX Security Best Practices for Client-Side Scripts
languages:
- c
- html
- javascript
- php
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

It is crucial to follow AJAX security best practices to prevent common web vulnerabilities. Here are some guidelines to keep in mind:

### 1. Avoid Dangerous JavaScript Functions

Dynamically evaluating code with functions like `eval()`, `new Function()`, `setTimeout()`, and `setInterval()` with dynamic, unvalidated string arguments is a significant security risk. User input or untrusted data can lead to code injection vulnerabilities.

Best Practice:

Instead of using these functions with dynamic strings, use safer alternatives. For example, use anonymous functions for `setTimeout` and `setInterval`.

Example of what to avoid:

```javascript
// Unsafe: susceptible to injection
setTimeout("alert('hello')", 1000);

// Safe:
setTimeout(() => alert('hello'), 1000);
```

### 2. Prevent Cross-Site Scripting (XSS) with `innerHTML`

Using `.innerHTML` to insert content into your web page can lead to XSS if the content is not properly sanitized.

Best Practice:

Use `.innerText` or `.textContent` when you only need to insert text. If you must insert HTML, use context-aware sanitization libraries before using `.innerHTML`.

Example:

```javascript
// Unsafe:
document.getElementById("div1").innerHTML = untrusted_user_input;

// Safe for text content:
document.getElementById("div1").textContent = untrusted_user_input;
```

### 3. Secure Client-Side Encryption and Secret Handling

Never perform encryption or handle secrets on the client side. Client-side code is visible and can be manipulated by attackers.

Best Practice:

All sensitive operations, including encryption and secret management, must be performed on the server.

### 4. Safe JSON and XML Creation

Building JSON or XML using string concatenation is error-prone and can lead to injection vulnerabilities.

Best Practice:

Use built-in browser APIs like `JSON.stringify()` or trusted third-party libraries to serialize data.

Example:

```javascript
// Unsafe:
let jsonString = '{"name":"' + name + '","email":"' + email + '"}';

// Safe:
let jsonString = JSON.stringify({ name: name, email: email });
```

### 5. Server-Side Enforcement of Security and Business Logic

Client-side validation is for user experience, not security. An attacker can easily bypass it.

Best Practice:

Always enforce all security checks and business logic on the server. The server should never trust any data coming from the client.

### Additional Recommendations:

*   Input Validation: Rigorously validate all inputs on the server, as AJAX services can be called directly by attackers.
*   CSRF Protection: Use anti-CSRF tokens for any state-changing AJAX requests. Store authentication tokens securely with HttpOnly and Secure flags for cookies.
*   JSON Hijacking: Return JSON responses with an object as the outermost element to prevent JSON hijacking in older browsers.
*   Schema Validation: Use JSON or XML schemas to validate the structure and types of data in AJAX requests and responses.
*   OWASP Resources: The [OWASP Java Encoder Project](https://owasp.org/www-project-java-encoder/) is an excellent resource for server-side encoding.