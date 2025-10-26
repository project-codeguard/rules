---
description: DOM-based XSS Prevention Best Practices
languages:
- c
- html
- javascript
- php
- typescript
- vlang
alwaysApply: false
---

## DOM-based XSS Prevention Security Rule

**RULE ENFORCEMENT:** This rule prevents DOM-based XSS vulnerabilities where untrusted data from user-controllable sources is inserted into DOM sinks without proper encoding or sanitization.

## Rule 1: DOM Sink Restrictions by Context

**YOU MUST secure DOM sinks** based on risk level:

### High-Risk HTML Sinks

```javascript
// VIOLATION: Direct assignment to HTML sinks
element.innerHTML = userInput;           // DANGEROUS
element.outerHTML = userInput;           // DANGEROUS
document.write(userInput);               // DANGEROUS

// REQUIRED: Use safe alternatives
element.textContent = userInput;         // SAFE
element.innerHTML = DOMPurify.sanitize(userInput); // SAFE
```

### Critical JavaScript Execution Sinks

```javascript
// VIOLATION: Code execution sinks
eval(userInput);                         // CRITICAL VULNERABILITY
new Function(userInput);                 // CRITICAL VULNERABILITY
setTimeout(userInput, 100);              // CRITICAL VULNERABILITY

// REQUIRED: Safe alternatives
setTimeout(() => processData(userInput), 100);  // SAFE
JSON.parse(userInput);                   // SAFE for JSON
```

### Medium-Risk URL/Event Sinks

```javascript
// VIOLATION: Unvalidated assignments
location.href = userInput;               // DANGEROUS
element.onclick = userInput;             // DANGEROUS

// REQUIRED: Validate and use safe patterns
if (/^https?:\/\/trusted-domain\.com/.test(userInput)) {
  location.href = encodeURI(userInput);
}
element.addEventListener('click', () => handleClick(userInput));
```

## Rule 2: Mandatory CSP and Trusted Types

**YOU MUST implement strict CSP:**

```http
Content-Security-Policy: 
  script-src 'self' 'nonce-{random}';
  object-src 'none';
  base-uri 'self';
  require-trusted-types-for 'script';
```

**YOU MUST use Trusted Types:**

```javascript
const policy = trustedTypes.createPolicy('dom-xss-prevention', {
  createHTML: (string) => DOMPurify.sanitize(string, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
    ALLOWED_ATTR: []
  })
});
element.innerHTML = policy.createHTML(userInput);
```

## Rule 3: Server-Side Validation Requirements

**YOU MUST validate all user input server-side:**

```javascript
function validateInput(input, context) {
  if (input.length > 1000) throw new Error('Input too long');
  
  const patterns = {
    html: /<script|javascript:|on\w+\s*=/i,
    url: /^https?:\/\/[a-zA-Z0-9.-]+/,
    text: /<[^>]*>/g
  };
  
  if (patterns[context] && patterns[context].test(input)) {
    throw new Error('Invalid input detected');
  }
  return input;
}
```

## Rule 4: Context-Aware Encoding

**YOU MUST apply proper encoding by context:**

```javascript
// HTML Context
function encodeHTML(str) {
  return str.replace(/[&<>"'\/]/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;', '/': '&#x2F;'
  })[char]);
}

// JavaScript Context  
function encodeJS(str) {
  return str.replace(/[\\'"<>/\n\r\t]/g, char => ({
    '\\': '\\\\', "'": "\\'", '"': '\\"', '<': '\\u003C', 
    '>': '\\u003E', '/': '\\u002F', '\n': '\\n', '\r': '\\r', '\t': '\\t'
  })[char]);
}

// URL Context
function encodeURL(str) {
  return encodeURIComponent(str).replace(/['"<>]/g, char => 
    '%' + char.charCodeAt(0).toString(16).toUpperCase());
}
```

## Rule 5: Safe DOM API Usage

**YOU MUST use safe DOM construction:**

```javascript
function createSafeElement(tagName, textContent, attributes = {}) {
  const element = document.createElement(tagName);
  if (textContent) element.textContent = textContent;
  
  const safeAttrs = ['class', 'id', 'title', 'alt', 'src', 'href', 'role'];
  for (const [key, value] of Object.entries(attributes)) {
    if (safeAttrs.includes(key.toLowerCase())) {
      element.setAttribute(key, value);
    }
  }
  return element;
}
```

## Rule 6: Source Validation

**YOU MUST validate untrusted data sources:**

### URL Parameters & PostMessage

```javascript
// URL parameter validation
function getURLParam(name) {
  const value = new URLSearchParams(location.search).get(name);
  if (!value || value.length > 100 || /<script|javascript:/i.test(value)) {
    throw new Error('Invalid parameter');
  }
  return value;
}

// PostMessage validation
window.addEventListener('message', (event) => {
  const allowedOrigins = ['https://trusted-domain.com'];
  if (!allowedOrigins.includes(event.origin)) return;
  processMessage(event.data);
});
```

## Rule 7: Framework Integration

**Framework-specific safe patterns:**

```javascript
// React: Safe HTML rendering
function SafeComponent({ htmlContent }) {
  const clean = DOMPurify.sanitize(htmlContent, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br']
  });
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}

// Vue: Safe directive
Vue.directive('safe-html', {
  update: (el, binding) => {
    el.innerHTML = DOMPurify.sanitize(binding.value, {
      ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br']
    });
  }
});
```

## Violation Detection Patterns

**These patterns will trigger security violations:**

```javascript
// VIOLATION: Direct DOM manipulation
element.innerHTML = userInput;
eval(userData);
setTimeout(userData, 100);
location.href = userUrl;
element.onclick = userHandler;

// VIOLATION: Unescaped template literals
const html = `<div>${userInput}</div>`;

// VIOLATION: Missing validation
window.addEventListener('message', (e) => processMessage(e.data));
```

## Mandatory Compliance Checks


✅ **DOMPurify imported and used for HTML insertion**
✅ **No innerHTML/outerHTML without sanitization**
✅ **No eval(), new Function(), setTimeout/setInterval with strings**
✅ **CSP implemented with script-src 'self'**
✅ **Trusted Types policy implemented**
✅ **URL validation before location assignments**
✅ **Origin validation for postMessage**

**VIOLATION CONSEQUENCES:** DOM-based XSS vulnerabilities allow arbitrary JavaScript execution, leading to account compromise, data theft, and malicious user actions.

**TEST PAYLOADS:** Code must safely handle:
- `<script>alert('XSS')</script>`
- `javascript:alert('XSS')`
- `"><script>alert('XSS')</script>`
- `'; eval('alert(1)'); //`