---
description: Third Party JavaScript Management Security
languages:
- c
- javascript
- typescript
alwaysApply: false
---

## Third Party JavaScript Management Security

Secure third-party JavaScript tags to prevent arbitrary code execution, data leakage, and loss of application control.

### Major Risks

Third-party JavaScript poses three critical risks:
1. Loss of control over client application changes
2. Execution of arbitrary code on client systems
3. Disclosure of sensitive information to third parties

### Security Strategies

#### Server Direct Data Layer (Recommended)
Create controlled data layer that third-party scripts can access instead of direct DOM access.

Key principles:
- Only first-party code populates the data layer
- Third-party scripts read exclusively from sanitized data layer
- Tag JavaScript can only access host data layer values, never URL parameters

Benefits:
- Only your JavaScript executes on user browsers
- Only validated data sent to vendors
- Scalable for large sites with multiple vendor tags

#### Subresource Integrity (SRI)
Ensure only reviewed code executes by adding integrity metadata.

```html
<script src="https://analytics.vendor.com/v1.1/script.js"
   integrity="sha384-MBO5IDfYaE6c6Aao94oZrIOiC7CGiSNE64QUbHNPhzk8Xhm0djE6QqTpL0HzTUxk"
   crossorigin="anonymous">
</script>
```

Requirements:
- Vendor host must have CORS enabled
- Monitor vendor JavaScript for changes regularly
- Update integrity hashes when vendor updates scripts

#### Sandboxing with iframe
Isolate vendor JavaScript to prevent direct DOM and cookie access.

```html
<!-- Host page with sandboxed iframe -->
<html>
   <head></head>
     <body>
       ...
       <iframe
       src="https://somehost-static.net/analytics.html"
       sandbox="allow-same-origin allow-scripts">
       </iframe>
   </body>
</html>

<!-- somehost-static.net/analytics.html -->
<html>
   <head></head>
     <body>
       ...
       <script>
       window.addEventListener("message", receiveMessage, false);
       function receiveMessage(event) {
         if (event.origin !== "https://somehost.com:443") {
           return;
         } else {
         // Make some DOM here and initialize other
        //data required for 3rd party code
         }
       }
       </script>
       <!-- 3rd party vendor javascript -->
       <script src="https://analytics.vendor.com/v1.1/script.js"></script>
       <!-- /3rd party vendor javascript -->
   </body>
 </html>
```

Communication requirements:
- Use postMessage mechanism for secure data exchange
- Validate event origins before processing messages
- Consider Content Security Policy (CSP) for additional protection

#### Content Sanitization
Clean DOM data before sending to third parties using:
- DOMPurify: XSS sanitizer for HTML, MathML and SVG
- MentalJS: JavaScript parser and sandbox

#### Tag Manager Controls
For tag management systems:
- Restrict JavaScript access to data layer values only
- Disable custom HTML tags and JavaScript code where possible
- Verify tag manager security practices and access controls
- Implement two-factor authentication for tag configuration

### Operational Security

#### Keep Libraries Updated
- Regularly update JavaScript libraries to address vulnerabilities
- Use tools like RetireJS to identify vulnerable libraries

#### Vendor Agreements
Contractual controls:
- Require evidence of secure coding practices and code integrity monitoring
- Include penalties for serving malicious JavaScript
- Mandate source code monitoring and change detection

#### Complete Prevention Strategy
Most effective controls:
1. Data layer architecture with API calls to marketing servers
2. Subresource Integrity implementation
3. Virtual frame containment deployment

### Implementation Guidelines

1. Implement server-direct data layer architecture for analytics tags
2. Use Subresource Integrity for all external script requests
3. Deploy iframe sandboxing for high-risk third-party scripts
4. Sanitize all dynamic data before including in tag payloads
5. Maintain updated JavaScript libraries and monitor for vulnerabilities
6. Establish vendor agreements with security requirements
7. Regularly audit and monitor third-party script changes