---
description: Certificate and Public Key Pinning Security
languages:
- c
- java
- javascript
- kotlin
- matlab
- swift
- typescript
- xml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Certificate and Public Key Pinning Guidelines

Essential practices for implementing certificate and public key pinning to prevent Man-in-the-Middle attacks in hostile environments.

### Understanding the Problem

TLS channels can be vulnerable to MITM attacks when certificate-based trust is compromised through:
1. Attackers acquiring rogue certificates from trusted CAs for victim sites
2. Attackers injecting dangerous CAs into client trust stores

Pinning associates a host with its expected X509 certificate or public key, creating a pinset that advertised credentials must match.

### When NOT to Pin (Critical Decision Criteria)

Avoid pinning in these situations:
- You don't control both client and server sides of the connection
- You cannot update the pinset securely without app redeployment
- Certificate key pairs cannot be predicted before being put into service
- Application is not a native mobile application
- Updating pinset is disruptive to operations

The risk of outages almost always outweighs security benefits given modern certificate authority security advancements.

### When Pinning May Be Appropriate

Consider pinning only when:
- You control both endpoints and can manage certificate lifecycles
- You can implement secure pin update mechanisms
- Your threat model specifically requires protection against CA compromise
- You have tested thoroughly and planned for certificate rotation

### Implementation Approaches by Platform

#### Android
Use Android's Network Security Configuration feature with `<pin-set>` configuration settings. Alternatively, use established libraries like OkHTTP for programmatic pinning. Avoid implementing custom SSL validation from scratch.

#### iOS
Apple suggests pinning CA public keys via `Info.plist` under App Transport Security Settings. Use TrustKit library for easier implementation. Custom implementation requires SecTrustEvaluate logic following HTTPS Server Trust Evaluation guidelines.

#### .Net
Implement using ServicePointManager callbacks for certificate validation.

#### OpenSSL
Use verify_callback or post-connection validation via SSL_get_peer_certificate. Must call SSL_get_verify_result (verify X509_V_OK) and SSL_get_peer_certificate (verify non-NULL). Fail connection and tear down socket on validation errors.

#### Electron
Use electron-ssl-pinning library or ses.setCertificateVerifyProc for custom certificate validation.

### What to Pin

Pin selection strategy:
1. Leaf certificate pinning (recommended): Provides 100% certainty but requires backup pins for intermediate CAs to prevent app breakage during certificate rotation
2. Intermediate CA pinning: Reduces risk but trusts all certificates issued by that CA
3. Root CA pinning: Not recommended due to high risk from trusting all intermediate CAs

Pin type options:
- Whole certificate: Easiest to implement but requires frequent updates for certificate rotation
- Public key (subjectPublicKeyInfo): More flexible, allows certificate renewal with same key, provides access to key parameters and algorithm context
- Hash: Convenient and fixed-length but lacks contextual information

Prefer subjectPublicKeyInfo pinning for balance of flexibility and security context.

### Pin Management Best Practices

#### Pin Addition Timing
Add pins at development time (preloading) rather than Trust On First Use (TOFU). Preloading out-of-band prevents attackers from tainting pins.

#### Backup Strategy
Always include backup pins (intermediate CA or alternate certificates) to prevent application outages during certificate updates.

#### Update Mechanisms
Plan secure pin update methods that don't require app redeployment. Consider remote configuration with authenticated channels.

#### Failure Handling
Never allow users to bypass pin validation failures. Log failures client-side but terminate connections on pin mismatches.

### Corporate Environment Considerations

For organizations using interception proxies as part of Data Loss Prevention:
- Do not automatically allow-list interception proxies
- Add proxy public keys to pinset only after explicit risk acceptance approval
- Treat corporate proxies as "good bad actors" that still break end-to-end security

### Testing and Validation

Thoroughly test pinning implementations using OWASP Mobile Security Testing Guide network communication guidelines:
- Verify pin validation occurs correctly
- Test certificate rotation scenarios
- Validate failure handling paths
- Ensure backup pins function properly

### Operational Considerations

#### Certificate Lifecycle Management
- Coordinate with backend teams on certificate rotation schedules
- Plan pin updates in advance of certificate expiration
- Monitor certificate validity periods
- Implement alerts for approaching pin expiration

#### Risk Assessment
Understand that pinning creates operational risk of application outages if not managed properly. The security benefit must outweigh availability risks for your specific threat model.

### Common Implementation Errors to Avoid

- Custom TLS or pinning implementations instead of vetted libraries
- Pinning without backup strategies
- Allowing user bypass of pin failures
- Inadequate testing of certificate rotation scenarios
- Pinning root CAs without understanding the expanded trust implications

### Summary

Certificate and public key pinning can provide additional protection against sophisticated MITM attacks but introduces significant operational complexity and availability risks. Most applications should rely on standard certificate validation rather than implementing pinning. When pinning is necessary, use platform-native solutions or well-established libraries, implement comprehensive backup strategies, and thoroughly test all scenarios including certificate rotation.