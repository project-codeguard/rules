---
description: XSS Filter Evasion Prevention - Advanced techniques attackers use to
  bypass input filtering and blacklists
languages:
- c
- javascript
- typescript
alwaysApply: false
---

Relying solely on input filtering or blacklists is insufficient because attackers use numerous techniques to bypass these defenses:

- Mixed encoding schemes: Combining HTML, URL, and Unicode encodings
- Whitespace manipulation: Using tabs, newlines, and other whitespace characters to confuse parsers
- Malformed tags: Creating deliberately broken HTML that browsers will "fix" during rendering
- Obfuscation: Using JavaScript encoding functions like `String.fromCharCode()` to hide malicious code

### Context-Aware Output Encoding

The most effective defense is to apply the appropriate encoding based on where the data will be used:

#### HTML Context (Content between tags)

```javascript
// VULNERABLE
const userName = request.getParameter("user");
document.getElementById("welcome").innerHTML = "Hello, " + userName;

// SECURE
import { encodeForHTML } from 'your-encoding-library';
const userName = request.getParameter("user");
document.getElementById("welcome").innerHTML = "Hello, " + encodeForHTML(userName);
```

#### HTML Attribute Context

```javascript
// VULNERABLE
const userColor = request.getParameter("color");
document.getElementById("profile").innerHTML = 
  `<div class="profile" style="background-color:${userColor}">Profile</div>`;

// SECURE
import { encodeForHTMLAttribute } from 'your-encoding-library';
const userColor = request.getParameter("color");
document.getElementById("profile").innerHTML = 
  `<div class="profile" style="background-color:${encodeForHTMLAttribute(userColor)}">Profile</div>`;
```

#### JavaScript Context

```javascript
// VULNERABLE
const userInput = request.getParameter("input");
const script = document.createElement("script");
script.textContent = `const userValue = "${userInput}";`;

// SECURE
import { encodeForJavaScript } from 'your-encoding-library';
const userInput = request.getParameter("input");
const script = document.createElement("script");
script.textContent = `const userValue = "${encodeForJavaScript(userInput)}";`;
```

#### URL Context

```javascript
// VULNERABLE
const redirectUrl = request.getParameter("url");
location.href = redirectUrl;

// SECURE
import { encodeForURL } from 'your-encoding-library';
const redirectUrl = request.getParameter("url");
// Validate URL pattern first
if (isValidRedirectURL(redirectUrl)) {
  location.href = encodeForURL(redirectUrl);
}
```

#### CSS Context

```javascript
// VULNERABLE
const userTheme = request.getParameter("theme");
document.getElementById("custom").style = userTheme;

// SECURE
import { encodeForCSS } from 'your-encoding-library';
const userTheme = request.getParameter("theme");
document.getElementById("custom").style = encodeForCSS(userTheme);
```

### Using Established Sanitization Libraries

Avoid creating your own sanitization logic. Use well-maintained libraries instead:

#### JavaScript/DOM

```javascript
// Using DOMPurify
import DOMPurify from 'dompurify';

function displayUserContent(content) {
  // Configure DOMPurify to only allow specific tags and attributes
  const config = {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'target']
  };
  
  const sanitized = DOMPurify.sanitize(content, config);
  document.getElementById('user-content').innerHTML = sanitized;
}
```

#### Java

```java
// Using OWASP Java Encoder
import org.owasp.encoder.Encode;

@Controller
public class UserController {
    @GetMapping("/profile")
    public String showProfile(Model model, @RequestParam String username) {
        model.addAttribute("encodedUsername", Encode.forHtml(username));
        return "profile";
    }
}

// In your template (e.g., Thymeleaf)
// <div th:text="${encodedUsername}">Username</div>
```

#### PHP

```php
// Using HTMLPurifier
require_once 'HTMLPurifier.auto.php';

$config = HTMLPurifier_Config::createDefault();
$purifier = new HTMLPurifier($config);

$userBio = $_POST['bio'];
$cleanBio = $purifier->purify($userBio);

echo '<div class="bio">' . $cleanBio . '</div>';
```

### Avoiding Dangerous Patterns

Certain coding patterns are particularly vulnerable to XSS attacks:

#### Avoid Unsafe JavaScript APIs

```javascript
// DANGEROUS - Never do this with user input
eval(userInput);
document.write(userInput);
new Function(userInput);
setTimeout(userInput, 100);
setInterval(userInput, 100);
element.innerHTML = userInput;

// SAFER ALTERNATIVES
// Instead of eval, parse JSON safely
const data = JSON.parse(userInput);

// Instead of innerHTML, use textContent
element.textContent = userInput;

// Or create elements properly
const div = document.createElement('div');
div.textContent = userInput;
parentElement.appendChild(div);
```

#### Avoid Inline Scripts and Event Handlers

```html
<!-- DANGEROUS - Inline event handlers are vulnerable to XSS -->
<button onclick="doSomething('<?php echo $userInput; ?>')">Click me</button>

<!-- SAFER - Use addEventListener instead -->
<button id="safeButton">Click me</button>
<script>
  document.getElementById('safeButton').addEventListener('click', function() {
    doSomething(sanitizedUserInput);
  });
</script>
```

### Defense in Depth Strategy

Implement multiple layers of protection:

#### Content Security Policy (CSP)

```http
# Strong CSP header that blocks inline scripts and restricts sources
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; style-src 'self'; img-src 'self' data:;
```

```javascript
// Setting CSP in Express.js
const helmet = require('helmet');
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", 'trusted-cdn.com'],
    objectSrc: ["'none'"],
    styleSrc: ["'self'"],
    imgSrc: ["'self'", 'data:']
  }
}));
```

#### Secure Cookie Configuration

```http
Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Strict
```

#### Input Validation

```javascript
// Validate input format before processing
function validateUsername(username) {
  // Only allow alphanumeric characters and limited symbols
  const usernameRegex = /^[a-zA-Z0-9_.-]{3,30}$/;
  if (!usernameRegex.test(username)) {
    throw new Error('Invalid username format');
  }
  return username;
}
```