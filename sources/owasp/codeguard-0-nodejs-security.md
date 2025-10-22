---
description: Node.js Security Best Practices
languages:
- c
- javascript
- typescript
alwaysApply: false
---

## Node.js Security Guidelines

Essential security practices for developing secure Node.js applications to prevent common vulnerabilities and attacks.

### Application Security

#### Use Flat Promise Chains

Avoid callback hell and improve error handling by using flat Promise chains or async/await:

```javascript
// Avoid callback hell
func1("input1")
   .then(function (result){
      return func2("input2");
   })
   .then(function (result){
      return func3("input3");
   })
   .then(function (result){
      return func4("input4");
   })
   .catch(function (error) {
      // error operations
   });
```

Using async/await:
```javascript
(async() => {
  try {
    let res1 = await func1("input1");
    let res2 = await func2("input2");
    let res3 = await func3("input2");
    let res4 = await func4("input2");
  } catch(err) {
    // error operations
  }
})();
```

#### Set Request Size Limits

Prevent resource exhaustion by limiting request body sizes:

```javascript
app.use(express.urlencoded({ extended: true, limit: "1kb" }));
app.use(express.json({ limit: "1kb" }));
```

For custom limits using raw-body:
```JavaScript
const contentType = require('content-type')
const express = require('express')
const getRawBody = require('raw-body')

const app = express()

app.use(function (req, res, next) {
  if (!['POST', 'PUT', 'DELETE'].includes(req.method)) {
    next()
    return
  }

  getRawBody(req, {
    length: req.headers['content-length'],
    limit: '1kb',
    encoding: contentType.parse(req).parameters.charset
  }, function (err, string) {
    if (err) return next(err)
    req.text = string
    next()
  })
})
```

#### Perform Input Validation

Use allowlists and sanitize all inputs to prevent injection attacks. Consider modules like validator and express-mongo-sanitize for input validation.

#### Perform Output Escaping

Escape all HTML and JavaScript content to prevent XSS attacks using libraries like escape-html or node-esapi.

#### Monitor Event Loop Health

Use monitoring to detect when your server is overloaded:

```javascript
const toobusy = require('toobusy-js');
app.use(function(req, res, next) {
    if (toobusy()) {
        res.status(503).send("Server Too Busy");
    } else {
    next();
    }
});
```

#### Prevent Brute Force Attacks

Implement rate limiting and delays for authentication endpoints:

```javascript
const bouncer = require('express-bouncer');
bouncer.blocked = function (req, res, next, remaining) {
    res.status(429).send("Too many requests have been made. Please wait " + remaining/1000 + " seconds.");
};
app.post("/login", bouncer.block, function(req, res) {
    if (LoginFailed){  }
    else {
        bouncer.reset( req );
    }
});
```

#### Use Anti-CSRF Protection

Protect state-changing requests against Cross-Site Request Forgery. Note: csurf package is deprecated; use alternative CSRF protection packages.

#### Prevent HTTP Parameter Pollution

Use the hpp module to handle multiple parameters with the same name:

```javascript
const hpp = require('hpp');
app.use(hpp());
```

#### Return Only Necessary Data

Limit data exposure by returning only required fields:

```javascript
exports.sanitizeUser = function(user) {
  return {
    id: user.id,
    username: user.username,
    fullName: user.fullName
  };
};
```

### Error and Exception Handling

#### Handle Uncaught Exceptions

Bind to uncaughtException events to clean up resources before shutdown:

```javascript
process.on("uncaughtException", function(err) {
    // clean up allocated resources
    // log necessary error details to log files
    process.exit(); // exit the process to avoid unknown state
});
```

#### Handle EventEmitter Errors

Always listen to error events when using EventEmitter objects:

```javascript
const events = require('events');
const emitter = new myEventEmitter();
emitter.on('error', function(err){
    //Perform necessary error handling here
});
```

### Server Security

#### Set Secure Cookie Flags

Configure cookies with appropriate security flags:

```javascript
const session = require('express-session');
app.use(session({
    secret: 'your-secret-key',
    name: 'cookieName',
    cookie: { secure: true, httpOnly: true, path: '/user', sameSite: true}
}));
```

#### Use Security Headers

Implement security headers using helmet:

```javascript
const helmet = require("helmet");
app.use(helmet()); // Add various HTTP headers
```

Key headers include:
- HSTS: `app.use(helmet.hsts());`
- Frame protection: `app.use(helmet.frameguard());`
- XSS protection: `app.use(helmet.xssFilter());`
- Content Security Policy: `app.use(helmet.contentSecurityPolicy({...}));`
- Content type protection: `app.use(helmet.noSniff());`
- Hide powered by: `app.use(helmet.hidePoweredBy());`

### Platform Security

#### Keep Packages Updated

Regularly audit and update dependencies:

```bash
npm audit
npm audit fix
```

Use tools like OWASP Dependency-Check and Retire.js to identify vulnerable packages.

#### Avoid Dangerous Functions

Exercise caution with potentially dangerous functions:
- Avoid `eval()` with user input (remote code execution risk)
- Be careful with `child_process.exec` (command injection risk)
- Sanitize inputs when using `fs` module (directory traversal risk)
- Use `vm` module within proper sandboxes

#### Prevent ReDoS Attacks

Test regular expressions for denial of service vulnerabilities using tools like vuln-regex-detector.

#### Use Security Linters

Implement static analysis tools like ESLint and JSHint with security-focused rules in your development workflow.

#### Enable Strict Mode

Always use strict mode to catch common JavaScript errors:

```javascript
"use strict";

func();
function func() {
  y = 3.14;   // This will cause an error (y is not defined)
}
```

### Application Activity Logging

Implement comprehensive logging for security monitoring:

```javascript
const logger = new (Winston.Logger) ({
    transports: [
        new (winston.transports.Console)(),
        new (winston.transports.File)({ filename: 'application.log' })
    ],
    level: 'verbose'
});
```

By following these practices, you can significantly improve the security posture of your Node.js applications and protect against common web application vulnerabilities.