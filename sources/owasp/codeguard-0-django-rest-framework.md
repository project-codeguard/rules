---
description: Django REST Framework Security Best Practices
languages:
- python
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Django REST Framework Security Guidelines

This rule advises on critical security practices when developing Django REST Framework APIs to protect against common risks:

- Authentication & Authorization  
  - Always set `DEFAULT_AUTHENTICATION_CLASSES` with appropriate authentication schemes for all non-public endpoints.  
  - When using SessionAuthentication, ensure CSRF protection is enabled and properly configured.
  - Never leave `DEFAULT_PERMISSION_CLASSES` as `AllowAny`; explicitly restrict access using proper permission classes.  
  - When overriding `get_object()`, always call `self.check_object_permissions(request, obj)` to enforce object-level access control.  
  - Avoid per-view overrides of authentication, permission, or throttle classes unless fully confident in their implications.

- Serializer Security  
  - In DRF Serializers, specify explicit `fields = [...]` allowlists; do not use `exclude`.
  - For Django ModelForms (when used outside DRF), always use `Meta.fields` allowlist instead of `Meta.exclude` or `"__all__"`.
  - DO NOT use `Meta.exclude` (denylist approach) or `ModelForms.Meta.fields = "__all__"`.

- Rate Limiting & Throttling  
  - Configure `DEFAULT_THROTTLE_CLASSES` to enable API rate limiting as a DoS defense layer.  
  - Prefer to enforce rate limiting at the gateway or WAF level; DRF throttling is a last-resort safeguard.

- Security Configuration  
  - Ensure `DEBUG` and `DEBUG_PROPAGATE_EXCEPTIONS` are set to `False` in production environments.  
  - Never hardcode secrets such as `SECRET_KEY`; inject them via environment variables or secrets managers.  
  - Disable all unused or dangerous HTTP methods (e.g., PUT, DELETE) at the API level.  
  - Validate, sanitize, and filter all incoming data rigorously.
  - Set secure HTTP headers: `SECURE_CONTENT_TYPE_NOSNIFF = True`, `X_FRAME_OPTIONS = 'DENY'`, `SECURE_BROWSER_XSS_FILTER = True`.
  - Implement Content Security Policy (CSP) using django-csp middleware to prevent XSS and clickjacking attacks.

- Prevent Injection Attacks  
  - Avoid raw SQL queries with user input; use ORM or parameterized queries exclusively.
  - DO NOT add user input to dangerous methods (`raw()`, `extra()`, `cursor.execute()`).
  - For YAML parsing, use safe loaders (`yaml.SafeLoader`); never parse YAML or pickle data from untrusted sources.
  - DO NOT use `eval()`, `exec()`, or similar dynamic code execution functions on user input.

- Secret Management  
  - Never hardcode secrets such as `SECRET_KEY`; inject them via environment variables or secrets managers.
  - DO NOT hardcode API keys, database passwords, or other sensitive credentials in source code.

- Input Validation  
  - Validate, sanitize, and filter all client-provided data rigorously.
  - Use Django's built-in form validation or DRF serializers with proper validation methods.

- Logging Security  
  - Log authentication failures, authorization denials, and validation errors with sufficient context.
  - DO NOT log sensitive data (passwords, tokens, PII) in application logs.
  - Include stack traces, error messages, and user context in security-relevant log entries.

Summary:  
Always enforce object-level permissions with `check_object_permissions()`, use explicit field allowlists in serializers, avoid dangerous functions with user input, never hardcode secrets, implement proper input validation, and ensure security-aware logging practices.