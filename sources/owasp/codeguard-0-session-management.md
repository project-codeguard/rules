---
description: Session Management Security
languages:
- c
- go
- java
- javascript
- kotlin
- php
- python
- ruby
- scala
- swift
- typescript
alwaysApply: false
---

## Session Management Security

Implement secure session handling to prevent session hijacking, fixation, and unauthorized access through proper ID generation, cookie security, and lifecycle management.

### Session ID Properties

#### Secure Generation
- Use cryptographically secure pseudorandom number generator (CSPRNG) for session IDs
- Ensure minimum 64 bits of entropy (16 hexadecimal characters minimum)
- Generate completely random, opaque session IDs with no meaningful content
- Change default session ID names (PHPSESSID, JSESSIONID) to generic names like "id"

#### Session ID Content
- Session IDs must be meaningless identifiers on client side
- Never include sensitive information or PII in session ID values
- Store all session data (user details, permissions, state) server-side only
- Encrypt session storage if it contains sensitive information

### Cookie Security Configuration

#### Essential Cookie Attributes
- Secure: Only transmit over HTTPS connections
- HttpOnly: Prevent JavaScript access to protect against XSS
- SameSite: Use Strict or Lax to mitigate CSRF attacks
- Domain/Path: Scope cookies narrowly to minimize exposure

#### Cookie Persistence
- Use non-persistent session cookies (no Expires or Max-Age attributes)
- Session should disappear when browser instance closes
- Avoid persistent cookies for session management

Example secure cookie configuration:
```
Set-Cookie: id=<session-id>; Secure; HttpOnly; SameSite=Strict; Path=/app
```

### Transport Layer Security

- Enforce HTTPS for entire web session, not just authentication
- Never mix HTTP and HTTPS within same user session
- Implement HTTP Strict Transport Security (HSTS)
- Set or regenerate cookies only after HTTPS redirect occurs

### Session Lifecycle Management

#### Session ID Generation and Verification
- Use strict session management - only accept server-generated session IDs
- Reject any session ID not previously created by the application
- Treat session IDs as untrusted user input requiring validation
- Detect and alert on unknown session IDs as suspicious activity

#### Session ID Regeneration
- Regenerate session ID after any privilege level change
- Mandatory regeneration during authentication process
- Regenerate on password changes, permission changes, role changes
- Use different session ID names for pre/post authentication states
- Invalidate previous session IDs when generating new ones

Framework examples for regeneration:
- J2EE: `request.getSession(true)` & `HttpSession.invalidate()`
- ASP.NET: `Session.Abandon()` & `Response.Cookies.Add(new...)`
- PHP: `session_start()` & `session_regenerate_id(true)`

### Session Expiration

#### Automatic Expiration
- Implement idle timeout (2-5 minutes for high-value, 15-30 minutes for low-risk)
- Implement absolute timeout (4-8 hours based on application usage)
- Enforce timeouts server-side, never rely solely on client-side controls
- Optionally implement renewal timeout to periodically regenerate session IDs

#### Manual Expiration
- Provide visible, accessible logout button on every page
- Fully invalidate sessions server-side on logout
- Clear session cookies client-side with empty value and past expiration

Server-side invalidation examples:
- J2EE: `HttpSession.invalidate()`
- ASP.NET: `Session.Abandon()`
- PHP: `session_destroy()/unset()`

### Web Content Caching Protection

- Use Cache-Control: no-store for responses containing session IDs
- Apply restrictive cache directives for all sensitive content
- Prevent session ID caching in browser history or proxy servers
- Include cache control headers on all pages displaying sensitive data

### Attack Detection and Monitoring

#### Session Attack Detection
- Monitor for session ID brute force attempts from single IP addresses
- Detect session ID anomalies and manipulation attempts
- Log session lifecycle events (creation, renewal, destruction)
- Bind sessions to client properties (IP, User-Agent) for anomaly detection

#### Logging Best Practices
- Log session events using salted hash of session ID (not actual ID)
- Include timestamps, IP addresses, User-Agent, and operation details
- Monitor for simultaneous sessions and enforce business policies
- Protect administrative session management interfaces

### Client-Side Storage Security

#### Avoid Insecure Storage
- Never store session tokens in localStorage or sessionStorage
- Avoid any JavaScript-accessible session storage due to XSS risk
- If JavaScript access required, use Web Workers to isolate secrets
- Prefer HttpOnly cookies for session token exchange

#### Web Workers Alternative
- Use Web Workers for browser storage when persistence not required
- Keep secrets within Web Worker context, never transmit to main window
- Provides similar security guarantees as HttpOnly cookies

### Framework and Implementation

#### Built-in Session Management
- Prefer established framework session mechanisms over custom solutions
- Keep frameworks updated to latest versions with security fixes
- Review and harden default framework configurations
- Ensure secure session storage repository protection

#### Multiple Cookie Considerations
- Verify all cookies for sessions using multiple cookies
- Enforce relationships between pre/post authentication cookies
- Avoid same cookie names for different paths or domains
- Prevent cross-subdomain cookie exposure

### Reauthentication Requirements

Require reauthentication for high-risk events:
- Password changes
- Login from new/suspicious IP addresses or devices
- Account recovery completion
- Privilege escalation events

### Additional Security Measures

#### Client-Side Defenses (Defense-in-Depth)
- Implement login timeouts to force session ID renewal
- Force logout on browser window close events
- Disable cross-tab session sharing where feasible
- Automatic client logout with countdown warnings

#### WAF Protection
- Use Web Application Firewalls to enforce cookie security attributes
- Implement WAF-based session fixation protection
- Apply sticky session enforcement via WAF rules
- Use WAF for session expiration management when code changes limited

### Essential Implementation Checklist

1. Generate session IDs using CSPRNG with minimum 64 bits entropy
2. Configure cookies with Secure, HttpOnly, SameSite attributes
3. Enforce HTTPS site-wide with HSTS headers
4. Regenerate session IDs on all privilege changes
5. Implement both idle and absolute session timeouts
6. Provide complete logout functionality with server-side invalidation
7. Apply no-store cache directives for sensitive content
8. Monitor session attacks and log security events
9. Use framework built-in session management
10. Require reauthentication for sensitive operations