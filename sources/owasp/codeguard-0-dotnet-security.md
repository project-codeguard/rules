---
description: DotNet Security Best Practices
languages:
- c
- javascript
- xml
alwaysApply: false
version: 0.1.0
severity: medium
---

## .NET Security Guidelines

This rule advises on critical .NET security practices to prevent common web vulnerabilities:

- General Security Configuration
  - Keep .NET Framework, .NET Core, and all NuGet packages up-to-date.
  - Use Software Composition Analysis (SCA) tools in CI/CD pipelines.
  - Subscribe to .NET Core and ASP.NET Core security announcements on GitHub.

- Access Control and Authorization
  - Use `[Authorize]` attributes at controller or method level for all externally facing endpoints.
  - Always validate user permissions server-side before resource access.
  - Check roles using `User.Identity.IsInRole` in code when needed.
  - Implement proper direct object reference validation to prevent IDOR attacks.

- Authentication and Session Management
  - Use ASP.NET Core Identity with secure password policies and account lockout.
  - Set cookies with `HttpOnly = true` and `requireSSL = true` in production.
  - Reduce session timeout and disable sliding expiration for better security.
  - Throttle login, registration, and password reset methods against brute force attacks.

- Cryptographic Security
  - Never write custom cryptographic functions; use .NET's proven implementations.
  - Use strong hashing algorithms: SHA512 for general hashing, PBKDF2 for passwords.
  - Use AES-GCM for encryption with proper key management.
  - Use Windows Data Protection API (DPAPI) for secure local storage.
  - Enforce TLS 1.2+ for all network communications.

- Injection Prevention
  - Use parameterized SQL queries or Entity Framework exclusively.
  - Never concatenate user input into SQL commands or OS commands.
  - Use allowlist validation on all user input with methods like `IPAddress.TryParse`.
  - Escape LDAP special characters with backslash when needed.

- Security Misconfiguration
  - Disable debug and tracing in production using web.config transforms.
  - Force HTTPS redirects using `app.UseHttpsRedirection()` or Global.asax.
  - Remove server version headers and implement secure HTTP headers.
  - Never use default passwords or credentials.

- CSRF Protection
  - Use anti-forgery tokens with `@Html.AntiForgeryToken()` in forms.
  - Validate tokens with `[ValidateAntiForgeryToken]` on POST/PUT actions.
  - Set `ViewStateUserKey = Session.SessionID` for Web Forms CSRF protection.
  - Remove anti-forgery cookies on logout.

- Secure Headers Configuration
  - Set `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` headers.
  - Configure HSTS with `Strict-Transport-Security` header.
  - Remove `X-Powered-By` and version disclosure headers.

- Logging and Monitoring
  - Log authentication failures, access control violations with user context.
  - Use ILogger framework for centralized logging.
  - Never log sensitive data like passwords or tokens.
  - Include stack traces and error context in security logs.

- Serialization Security
  - Avoid `BinaryFormatter` which is dangerous for untrusted data.
  - Use `System.Text.Json`, `XmlSerializer`, or `DataContractSerializer` safely.
  - Never deserialize untrusted data without validation.
  - Implement digital signature validation for serialized objects.

CSRF Protection Example (from OWASP):

```csharp
protected override OnInit(EventArgs e) {
    base.OnInit(e);
    ViewStateUserKey = Session.SessionID;
}
```

Secure Headers Configuration (from OWASP):

```xml
<system.webServer>
  <httpProtocol>
    <customHeaders>
      <add name="Content-Security-Policy"
         value="default-src 'none'; style-src 'self'; img-src 'self'; font-src 'self'" />
      <add name="X-Content-Type-Options" value="NOSNIFF" />
      <add name="X-Frame-Options" value="DENY" />
      <add name="X-Permitted-Cross-Domain-Policies" value="master-only"/>
      <add name="X-XSS-Protection" value="0"/>
      <remove name="X-Powered-By"/>
    </customHeaders>
  </httpProtocol>
</system.webServer>
```

Summary:  
Secure .NET applications by implementing proper authorization controls, using secure authentication and session management, applying strong cryptography, preventing injection attacks, configuring security headers, implementing CSRF protection, maintaining secure configurations, logging security events properly, and handling serialization safely.