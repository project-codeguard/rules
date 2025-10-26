---
description: HTML5 Security Best Practices
languages:
- c
- go
- html
- java
- javascript
- php
- python
- ruby
- typescript
- xml
alwaysApply: false
---

## HTML5 Security Guidelines

This rule advises on secure HTML5 development practices to prevent vulnerabilities in modern web applications:

- Web Messaging Security
  - Always specify exact target origin in postMessage calls, never use "*" wildcard.
  - Verify event.origin strictly against trusted full domain names in message handlers.
  - Avoid partial domain matching that could allow subdomain takeover attacks.
  - Validate and sanitize all data received through postMessage before processing.
  - Never use eval() or Function() constructor on message data.
  - Use textContent instead of innerHTML when setting received message content.
  - Treat all cross-origin message data as untrusted input requiring validation.

- Cross-Origin Resource Sharing (CORS) Security
  - Restrict Access-Control-Allow-Origin to specific trusted origins, avoid "*" wildcard.
  - Validate URLs passed to XMLHttpRequest.open to prevent open redirects.
  - Implement proper CSRF protection even when using CORS (CORS doesn't prevent CSRF).
  - Reject mixed content requests (HTTP requests from HTTPS origins).
  - Don't rely solely on Origin header for access control as it can be spoofed outside browsers.
  - Use preflight requests for non-simple requests and validate Access-Control headers.

- WebSocket Security
  - Use only secure wss:// protocol, never unencrypted ws:// in production.
  - Implement application-level authentication and authorization for WebSocket connections.
  - Verify Origin header against allowlist during WebSocket handshake.
  - Validate and parse all WebSocket messages safely using JSON.parse() with error handling.
  - Implement connection limits and message size restrictions to prevent DoS attacks.
  - Use JWT or similar tokens for WebSocket authentication with proper validation.
  - Implement token invalidation and denylist mechanisms for revoked access.

- Client-Side Storage Security
  - Never store sensitive data (passwords, tokens, API keys, PII) in localStorage or sessionStorage.
  - Use sessionStorage instead of localStorage when persistence across browser sessions is not required.
  - Validate and sanitize all data retrieved from client-side storage before use.
  - Implement data encryption for sensitive information stored client-side when absolutely necessary.
  - Avoid hosting multiple applications on same origin to prevent storage access conflicts.

- DOM Manipulation and Link Security
  - Add rel="noopener noreferrer" attribute to all external links with target="_blank".
  - Set window.opener = null when using window.open() for external URLs.
  - Use iframe sandbox attribute with minimal permissions for untrusted content.
  - Implement X-Frame-Options header alongside iframe sandbox for defense-in-depth.
  - Avoid innerHTML with user-supplied content; use textContent, createElement, or trusted templating.
  - When innerHTML must be used, sanitize content with DOMPurify or similar libraries.

- Input Field Security and CSRF Protection
  - Use autocomplete="off" on sensitive input fields (passwords, credit cards, SSN).
  - Add spellcheck="false", autocorrect="off", autocapitalize="off" on credential inputs.
  - Implement CSRF tokens on all state-changing forms and AJAX requests.
  - Use secure cookie attributes: HttpOnly, Secure, SameSite=Strict for session cookies.
  - Validate CSRF tokens on server-side for all POST, PUT, DELETE requests.

- Secure Cookie Configuration
  - Set HttpOnly flag on session cookies to prevent JavaScript access.
  - Use Secure flag to ensure cookies are only sent over HTTPS connections.
  - Implement SameSite=Strict or SameSite=Lax to prevent CSRF attacks.
  - Use __Secure- or __Host- cookie prefixes for additional security.
  - Set appropriate cookie expiration and path restrictions.

- Web Workers and Service Workers Security
  - Validate all messages sent to and received from Web Workers.
  - Never create Web Workers from user-supplied URLs or content.
  - Implement proper error handling and timeout mechanisms for Worker communications.
  - Use Content Security Policy to restrict Worker script sources.
  - Validate Service Worker registration and update mechanisms.

- Geolocation and Device API Security
  - Require explicit user permission before accessing Geolocation API.
  - Validate geolocation data before sending to servers.
  - Implement proper error handling for geolocation failures.
  - Use HTTPS when transmitting location data to prevent interception.

- Offline Application Security
  - Require user consent before caching application data offline.
  - Validate integrity of cached resources to prevent cache poisoning.
  - Use HTTPS for all manifest files and cached resources.
  - Implement proper cache invalidation mechanisms for security updates.

Summary:  
Implement comprehensive HTML5 security controls through proper origin validation, secure storage practices, CSRF protection, secure cookie configuration, safe DOM manipulation, and robust authentication mechanisms to prevent XSS, CSRF, clickjacking, and data leakage vulnerabilities.