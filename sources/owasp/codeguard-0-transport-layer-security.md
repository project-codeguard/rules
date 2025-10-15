---
description: Transport Layer Security
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Transport Layer Security

Secure implementation of TLS to protect client-server communications with confidentiality, integrity, and authentication through proper protocol, cipher, and certificate configuration.


### TLS Security Benefits

When correctly implemented, TLS provides:
- Confidentiality: Protection against attackers reading traffic contents
- Integrity: Protection against traffic modification and replay attacks
- Authentication: Client confirmation of legitimate server connection

### Protocol Security

#### Use Strong TLS Protocols Only
General purpose web applications should default to TLS 1.3 with TLS 1.2 support if necessary.

Protocol requirements:
- Enable TLS 1.3 by default
- Support TLS 1.2 only if legacy client compatibility required
- Disable TLS 1.0, TLS 1.1, SSL v2, and SSL v3 completely
- Enable TLS_FALLBACK_SCSV extension to prevent downgrade attacks when fallback necessary
- Note: PCI DSS forbids legacy protocols such as TLS 1.0

#### Configure Strong Cipher Suites
Use only strong ciphers that provide adequate security levels.

Cipher requirements:
- Prefer GCM ciphers where possible
- Always disable null ciphers, anonymous ciphers, and EXPORT ciphers
- Use Mozilla Foundation secure configuration generator for balanced security and compatibility

#### Set Appropriate Diffie-Hellman Groups
Configure secure Diffie-Hellman parameters for key exchange.

TLS 1.3 groups: ffdhe2048, ffdhe3072, ffdhe4096, ffdhe6144, ffdhe8192

Configuration examples:

```text
# OpenSSL configuration
openssl_conf = openssl_init
[openssl_init]
ssl_conf = ssl_module
[ssl_module]
system_default = tls_system_default
[tls_system_default]
Groups = x25519:prime256v1:x448:ffdhe2048:ffdhe3072
```

```text
# Apache configuration
SSLOpenSSLConfCmd Groups x25519:secp256r1:ffdhe3072
```

```text
# NGINX configuration
ssl_ecdh_curve x25519:secp256r1:ffdhe3072;
```

#### Disable TLS Compression
Disable TLS compression to protect against CRIME attacks that could recover sensitive information like session cookies.

#### Keep Cryptographic Libraries Updated
Maintain current versions of SSL/TLS libraries to protect against vulnerabilities like Heartbleed.

### Certificate Management

#### Use Strong Keys and Protection
Generate certificates with minimum 2048-bit key size and protect private keys from unauthorized access using filesystem permissions and access controls.

#### Use Strong Cryptographic Hashing
Certificates should use SHA-256 for hashing algorithm rather than deprecated MD5 and SHA-1 algorithms.

#### Use Correct Domain Names
Certificate domain names must match server's FQDN in both commonName (CN) and subjectAlternativeName (SAN) attributes.

#### Consider Wildcard Certificate Risks
Wildcard certificates violate principle of least privilege. Use only when genuine need exists and never for systems at different trust levels.

#### Use Appropriate Certificate Authority
Choose trusted CAs for Internet-facing applications. Consider LetsEncrypt for free domain validated certificates.

### Application Implementation

#### Use TLS for All Pages
Implement TLS for entire application with HTTP 301 redirects and HSTS header support.

#### Prevent Mixed Content
Load all JavaScript, CSS, and resources over HTTPS to prevent session cookie sniffing and malicious code injection.

#### Use Secure Cookie Flag
Mark all cookies with "Secure" attribute to restrict transmission to encrypted HTTPS connections only.

#### Prevent Sensitive Data Caching
Use cache prevention headers:

```text
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
```

#### Implement HTTP Strict Transport Security
HSTS instructs browsers to always request site over HTTPS and prevents bypassing certificate warnings.

#### Consider Client Certificates and Mutual TLS
mTLS provides mutual authentication but involves significant administrative overhead. Recommended for high-value applications with technically sophisticated users.

#### Avoid Public Key Pinning in Browsers
HPKP deprecated and no longer supported by modern browsers. Consider pinning only in controlled environments.

### Testing and Validation

Test TLS configuration using tools like SSL Labs Server Test, testssl.sh, SSLyze, and other recommended online and offline testing tools.

### Implementation Guidelines

1. Default to TLS 1.3 with TLS 1.2 fallback only if necessary
2. Disable all legacy protocols (TLS 1.0/1.1, SSL v2/v3)
3. Configure strong cipher suites with GCM preference
4. Set appropriate Diffie-Hellman groups for key exchange
5. Disable TLS compression to prevent CRIME attacks
6. Use minimum 2048-bit certificate keys with SHA-256 hashing
7. Ensure correct domain names in certificate CN and SAN fields
8. Implement HTTPS for all pages with 301 redirects from HTTP
9. Prevent mixed content by loading all resources over HTTPS
10. Set Secure flag on all cookies
11. Prevent sensitive data caching with appropriate HTTP headers
12. Implement HSTS for browser enforcement
13. Consider mTLS for high-value applications
14. Avoid public key pinning in browsers
15. Regular testing of TLS configuration with recommended tools