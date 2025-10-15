---
description: Django Security Best Practices
languages:
- c
- python
alwaysApply: false
version: 0.1.0
severity: medium
---

## Django Security Guidelines

This rule advises on critical Django security practices to prevent common web vulnerabilities:

- General Security Configuration
  - Never set `DEBUG = True` in production environments.
  - Keep Django and dependencies up-to-date regularly.
  - Use rate limiting packages like `django_ratelimit` or `django-axes` for brute-force protection.

- Authentication System
  - Include `django.contrib.auth`, `django.contrib.contenttypes`, and `django.contrib.sessions` in `INSTALLED_APPS`.
  - Use `@login_required` decorator to protect views requiring authentication.
  - Configure `AUTH_PASSWORD_VALIDATORS` with appropriate validators for password policies.
  - Use `make_password()` and `check_password()` functions for password hashing and verification.

- Secret Key Management
  - Generate `SECRET_KEY` with at least 50 characters containing letters, digits, and symbols.
  - Use `get_random_secret_key()` function for key generation.
  - Store `SECRET_KEY` in environment variables, never hardcode in source.
  - Rotate keys regularly and immediately upon exposure.

- Security Middleware Configuration
  - Include `django.middleware.security.SecurityMiddleware` in `MIDDLEWARE` settings.
  - Include `django.middleware.clickjacking.XFrameOptionsMiddleware` in `MIDDLEWARE` settings.
  - Set `SECURE_CONTENT_TYPE_NOSNIFF = True` for MIME type protection.
  - Configure `SECURE_HSTS_SECONDS` with positive integer for HTTPS enforcement.
  - Set `X_FRAME_OPTIONS = 'DENY'` or `'SAMEORIGIN'` for clickjacking protection.

- Cookie Security
  - Set `SESSION_COOKIE_SECURE = True` to send session cookies over HTTPS only.
  - Set `CSRF_COOKIE_SECURE = True` to send CSRF cookies over HTTPS only.
  - Use `secure=True` parameter when setting custom cookies with `HttpResponse.set_cookie()`.

- CSRF Protection
  - Include `django.middleware.csrf.CsrfViewMiddleware` in `MIDDLEWARE` settings.
  - Use `{% csrf_token %}` template tag in all forms.
  - Extract CSRF token properly for AJAX calls.

- XSS Protection
  - Use Django's built-in template system with automatic HTML escaping.
  - Avoid `safe` filter and `mark_safe` function unless input is from trusted sources.
  - Use `json_script` template filter for passing data to JavaScript.

- HTTPS Configuration
  - Set `SECURE_SSL_REDIRECT = True` to redirect HTTP requests to HTTPS.
  - Configure `SECURE_PROXY_SSL_HEADER` when behind proxy or load balancer.

- Admin Panel Security
  - Change default admin URL from `/admin/` to custom path in `urls.py`.

Code Examples (from OWASP):

```python
# Authentication setup
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
]

@login_required
def my_view(request):
    # Your view logic

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
]

# Secret key from environment
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Cookie security
response.set_cookie('my_cookie', 'cookie_value', secure=True)
```

```html
<!-- CSRF in forms -->
<form method="post">
    {% csrf_token %}
    <!-- Your form fields here -->
</form>
```

Summary:  
Configure Django securely by disabling debug mode in production, using proper authentication settings, securing secret keys, enabling security middleware, setting secure cookie attributes, implementing CSRF protection, preventing XSS, enforcing HTTPS, and securing admin access.