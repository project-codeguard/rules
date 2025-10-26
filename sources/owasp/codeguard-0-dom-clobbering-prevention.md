---
description: DOM Clobbering Prevention Best Practices
languages:
- c
- html
- javascript
- php
- typescript
- vlang
alwaysApply: false
---

## DOM Clobbering Prevention Security Rule

**RULE ENFORCEMENT:** This rule prevents DOM clobbering attacks where malicious HTML elements with `id` or `name` attributes override JavaScript variables and browser APIs, potentially leading to XSS and security bypasses.

## Rule 1: HTML Sanitization Requirements

**YOU MUST sanitize all user-provided HTML** using DOMPurify or Sanitizer API:

```javascript
// REQUIRED: DOMPurify configuration
const clean = DOMPurify.sanitize(userInput, {
  SANITIZE_DOM: true,           // Protects built-in APIs
  SANITIZE_NAMED_PROPS: true,   // MANDATORY: Protects custom variables  
  FORBID_ATTR: ['id', 'name']   // REQUIRED: Remove clobbering attributes
});

// ALTERNATIVE: Sanitizer API
const sanitizer = new Sanitizer({
  blockAttributes: [{'name': 'id', elements: '*'}, {'name': 'name', elements: '*'}]
});
element.setHTML(userInput, {sanitizer});
```

**YOU ARE PROHIBITED FROM:**
* Using `innerHTML` with unsanitized user input
* Allowing `id` or `name` attributes in user-generated content
* Disabling `SANITIZE_NAMED_PROPS` in DOMPurify configuration

## Rule 2: Content Security Policy Requirements

**YOU MUST implement strict CSP** to prevent DOM clobbering exploitation:

```http
Content-Security-Policy: 
  script-src 'self' 'nonce-{random}';
  object-src 'none';
  base-uri 'self';
  require-trusted-types-for 'script';
```

**YOU MUST use Trusted Types** for DOM manipulation:

```javascript
const policy = trustedTypes.createPolicy('dompurify', {
  createHTML: (string) => DOMPurify.sanitize(string, {SANITIZE_NAMED_PROPS: true})
});
element.innerHTML = policy.createHTML(userInput);
```

## Rule 3: Variable Declaration Requirements

**YOU MUST use explicit variable declarations** to prevent global namespace pollution:

```javascript
"use strict";                       // REQUIRED in all JavaScript files
const config = { isAdmin: false };  // REQUIRED: Explicit declarations
let userState = {};                 // REQUIRED: Block-scoped variables

// PROHIBITED: Creates vulnerable globals
config = { isAdmin: false };        // WILL BE FLAGGED AS VIOLATION
```

**YOU ARE PROHIBITED FROM:**
* Storing sensitive data on `window` or `document` objects
* Using implicit global variables without declaration keywords
* Accessing user input on the left side of assignment expressions

## Rule 4: Object Validation Requirements

**YOU MUST validate object types** before accessing potentially clobbered properties:

```javascript
// REQUIRED: Type validation before use
function safePropertyAccess(obj, property) {
  if (obj && typeof obj === 'object' && !(obj instanceof Element)) {
    return obj[property];
  }
  throw new Error('Potential DOM clobbering detected');
}

// REQUIRED: Validate built-in APIs
if (typeof document.getElementById === 'function') {
  const element = document.getElementById('myId');
}
```

## Rule 5: Dynamic Attribute Restrictions

**YOU MUST validate all dynamic HTML attributes:**

```javascript
function setElementAttribute(element, name, value) {
  const forbidden = ['id', 'name', 'onclick', 'onload', 'onerror'];
  if (forbidden.includes(name.toLowerCase())) {
    throw new Error(`Attribute ${name} is prohibited for security`);
  }
  element.setAttribute(name, DOMPurify.sanitize(value, {ALLOWED_TAGS: []}));
}
```

**YOU ARE PROHIBITED FROM:**
* Setting `id` or `name` attributes from user input
* Using dynamic attribute assignment without validation
* Bypassing sanitization for `data-` or `aria-` attributes

## Rule 6: Framework Security Requirements

**React/Vue applications MUST use sanitized HTML rendering:**

```javascript
// REACT: Required safe HTML component
function SafeHtmlComponent({ userContent }) {
  const clean = DOMPurify.sanitize(userContent, {
    SANITIZE_NAMED_PROPS: true,
    FORBID_ATTR: ['id', 'name']
  });
  return <div dangerouslySetInnerHTML={{__html: clean}} />;
}

// VUE: Required directive
Vue.directive('safe-html', {
  update(el, binding) {
    el.innerHTML = DOMPurify.sanitize(binding.value, {
      SANITIZE_NAMED_PROPS: true,
      FORBID_ATTR: ['id', 'name']
    });
  }
});
```

## Rule 7: Runtime Monitoring Requirements

**YOU MUST implement DOM clobbering detection:**

```javascript
// REQUIRED: Runtime monitoring
function detectClobbering() {
  ['config', 'api', 'user', 'admin'].forEach(global => {
    if (window[global] instanceof Element) {
      console.error(`SECURITY VIOLATION: DOM Clobbering detected on ${global}`);
      securityLogger.warn('DOM_CLOBBERING_DETECTED', { variable: global });
    }
  });
}
setInterval(detectClobbering, 5000);
```

## Rule Violation Detection

**The following patterns will trigger security violations:**

```javascript
// VIOLATION: Implicit global creation
config = { sensitive: true };

// VIOLATION: Storing sensitive data on window
window.userRole = 'admin';

// VIOLATION: Unvalidated innerHTML usage
element.innerHTML = userInput;

// VIOLATION: Dynamic property access without validation
obj[userControlledProperty] = value;

// VIOLATION: Missing sanitization
document.body.appendChild(htmlFromUser);
```

## Mandatory Compliance Checks

The following checks MUST be performed:

✅ **DOMPurify imported and configured with `SANITIZE_NAMED_PROPS: true`**
✅ **No direct `innerHTML` usage without sanitization**
✅ **Strict mode enabled in all JavaScript files**
✅ **CSP headers implemented with `script-src 'self'`**
✅ **No `id` or `name` attributes in user content**
✅ **Runtime clobbering detection implemented**
✅ **Type validation before property access**

**NON-COMPLIANCE CONSEQUENCES:** Code that violates these rules creates DOM clobbering vulnerabilities that can lead to XSS attacks and privilege escalation.

**TEST PAYLOAD:** `<a id=config><a id=config name=isAdmin href=true>` must be properly sanitized or blocked.