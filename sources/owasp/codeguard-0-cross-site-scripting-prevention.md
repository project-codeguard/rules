---
description: Cross Site Scripting (XSS) Prevention Best Practices
languages:
- c
- html
- javascript
- php
- typescript
- vlang
alwaysApply: false
---

## Introduction

This cheat sheet helps developers prevent XSS vulnerabilities.

Cross-Site Scripting (XSS) attacks are serious and can lead to account impersonation, observing user behaviour, loading external content, stealing sensitive data, and more. XSS occurs when an attacker injects malicious content into a webpage that executes in users' browsers.

**This cheatsheet contains techniques to prevent or limit the impact of XSS. Since no single technique will solve XSS, using the right combination of defensive techniques will be necessary to prevent XSS.**

## Preventing Cross-Site Scripting (XSS) Vulnerabilities

### Core Defensive Strategies

#### 1. Context-Aware Output Encoding

The most important defense against XSS is proper output encoding based on the context where data will be inserted:

* **HTML Body Context:** Use `element.textContent` instead of `innerHTML`, or sanitize with DOMPurify for rich content
* **HTML Attribute Context:** Always quote attributes and HTML encode values: `<div data-user="{{encodedInput}}">` 
* **JavaScript Context:** Avoid dynamic JavaScript generation; use data attributes and event listeners instead
* **CSS Context:** Validate CSS values against strict allow-lists before injection
* **URL Context:** Encode URLs and validate protocols to prevent `javascript:` URLs

* **ARIA Attributes & SVG Context:** Validate ARIA values against allow-lists; sanitize SVG with DOMPurify SVG profiles
* **JavaScript Event Handlers:** Never inject user data into `onclick` attributes; use `addEventListener()` instead

#### 2. Leverage Framework Protections

Modern frameworks provide built-in XSS protections:

* **React:** Auto-escapes values in JSX, but be careful with `dangerouslySetInnerHTML`
* **Angular:** Uses contextual auto-escaping, but be cautious with `[innerHTML]` binding
* **Vue:** Auto-escapes mustache interpolations, but watch out for `v-html`

When using escape hatches like `dangerouslySetInnerHTML`, `[innerHTML]`, or `v-html`, always sanitize with DOMPurify first.

#### 3. Server-Side Input Validation and Sanitization

* **Server-Side Validation is Mandatory:** All input validation must happen on the server. Client-side validation is for user experience only.
* **Validate Against Allow-Lists:** Use strict regex patterns for expected input types (email, username, etc.) with length limits.
* **HTML Sanitization with Trusted Libraries:** Use [DOMPurify](https://github.com/cure53/DOMPurify) with strict configurations:
  ```javascript
  const cleanHtml = DOMPurify.sanitize(userHtml, {
    ALLOWED_TAGS: ['b', 'i', 'p', 'a', 'ul', 'li'],
    ALLOWED_ATTR: ['href', 'target', 'rel'],
    ALLOW_DATA_ATTR: false
  });
  ```

#### 4. Defense-in-Depth Controls

* **Content Security Policy (CSP):** Implement strict CSP headers as additional protection:
  ```http
  Content-Security-Policy: default-src 'self'; 
    script-src 'self' 'nonce-{random}'; 
    style-src 'self' 'unsafe-inline'; 
    object-src 'none'; 
    base-uri 'self';
    require-trusted-types-for 'script';
  ```

* **Trusted Types API:** Use Trusted Types to prevent DOM XSS:
  ```javascript
  // Define trusted types policy
  const policy = trustedTypes.createPolicy('myPolicy', {
    createHTML: (string) => DOMPurify.sanitize(string),
    createScript: () => { throw new Error('Script creation not allowed'); }
  });
  
  // Use with trusted types
  element.innerHTML = policy.createHTML(userInput);
  ```

* **Safe DOM APIs:** Always prefer safe DOM manipulation methods:
  ```javascript
  // Safe approaches
  element.textContent = userInput;          // Always safe for text
  element.setAttribute('data-user', userInput); // Safe for most attributes
  element.classList.add(validatedClassName);     // Safe for CSS classes
  ```

* **Secure Cookie Configuration:** Prevent cookie theft:
  ```http
  Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Strict
  ```

#### 5. Common Pitfalls to Avoid

* **Don't trust any data source:** Even internal APIs or databases can contain malicious data.
* **Beware of indirect inputs:** User data can enter your application through URLs, form fields, HTTP headers, and JSON/XML payloads.
* **Don't rely on client-side sanitization alone:** Always re-validate and sanitize on the server.
* **Keep dependencies updated:** Regularly update your frameworks and libraries to benefit from security patches.

By applying these context-specific encoding strategies and defense-in-depth approaches, you can significantly reduce the risk of XSS vulnerabilities in your web applications.