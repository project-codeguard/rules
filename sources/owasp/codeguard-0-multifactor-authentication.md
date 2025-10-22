---
description: Multifactor Authentication Implementation
languages:
- c
- go
- java
- javascript
- kotlin
- php
- python
- ruby
- swift
- typescript
alwaysApply: false
---

## Multifactor Authentication Guidelines

Essential practices for implementing secure multifactor authentication to protect against account compromise.

### Understanding MFA Factors

True MFA requires at least two factors from different categories. Multiple instances of the same factor (password + PIN) does not constitute MFA:

1. Something You Know: Passwords, PINs (avoid security questions - no longer acceptable per NIST SP 800-63)
2. Something You Have: Hardware tokens, software OTP, U2F tokens, certificates, smart cards 
3. Something You Are: Biometrics (fingerprints, facial recognition, iris scans)
4. Somewhere You Are: Source IP address, geolocation, geofencing
5. Something You Do: Behavioral profiling, keystroke dynamics (largely theoretical)

### When to Require MFA

Implement MFA for all critical authentication points:
- User login (primary requirement)
- Password changes or security question updates
- Email address changes associated with the account
- Disabling MFA
- Elevating user session to administrative session
- All API endpoints and mobile application authentication flows

### MFA Method Recommendations

#### Recommended (Most Secure)
- Passkeys/FIDO2: Combines possession and biometric/PIN factors, resistant to phishing
- Hardware U2F Tokens: Challenge-response authentication, phishing-resistant
- Hardware OTP Tokens: Separate physical devices, nearly impossible to compromise remotely
- Digital Certificates: Resistant to phishing, centrally manageable

#### Acceptable with Caution
- Software TOTP: Widely supported, cost-effective but vulnerable if device is compromised
- Smart Cards: Strong when combined with PIN but require PKI infrastructure

#### Avoid for Sensitive Applications
- SMS/Phone Calls: Susceptible to SIM swapping, should not protect PII or financial data
- Email Verification: Often same password as application, provides minimal additional security
- Security Questions: No longer acceptable per NIST SP 800-63

### Implementation Requirements

#### Risk-Based Authentication
Adjust MFA requirements based on context to improve user experience:
- Require MFA for new devices or unusual locations
- Use corporate IP ranges or geolocation as risk signals
- Consider time of access and device fingerprinting
- Implement behavioral profiling for continuous authentication

Common risk signals:
- Geolocation and IP reputation
- Device fingerprinting
- Unusual time of access
- Known compromised credentials

#### MFA Recovery Mechanisms
Implement secure recovery without creating bypass opportunities:
- Provide single-use recovery codes during MFA enrollment
- Require users to set up multiple MFA types
- Mail recovery codes to registered physical address
- Implement rigorous identity verification through support team
- Use trusted user vouching systems for corporate environments

#### Failed Authentication Handling
When password succeeds but MFA fails:
- Prompt user to try alternative MFA methods
- Allow secure MFA reset process
- Notify user of failed attempt with time, location, and device information
- Display notification on next successful login

#### Security Controls
- Rate limit authentication attempts to prevent brute force
- Implement account lockout after multiple failed MFA attempts
- Verify MFA state in all authenticated endpoints
- Avoid "remember this device" for highly sensitive applications
- Log and monitor all MFA-related events

### Factor-Specific Considerations

#### Hardware Tokens
Pros: Extremely difficult to compromise remotely, work without mobile devices
Cons: Expensive deployment, administrative overhead, can be stolen and used without PIN

#### Software TOTP
Pros: Cost-effective, easy deployment, widely supported standards
Cons: Vulnerable if device compromised, may be on same device as authentication

#### Biometrics
Pros: Hard to spoof, fast and convenient
Cons: Privacy concerns, expensive hardware, difficult to change if compromised

#### Location-Based
Pros: Transparent to users, minimal administrative overhead
Cons: No protection against compromised systems or insider threats

### Third-Party MFA Services

Consider using established MFA providers to reduce implementation complexity:
- Evaluate security practices and certifications of providers
- Understand implications if third-party service is compromised
- Ensure service meets compliance requirements for your industry

### Regulatory Compliance

Many industries require MFA implementation:
- Finance and healthcare sectors commonly mandate MFA
- GDPR compliance often requires MFA for sensitive data
- NIST SP 800-63 provides authoritative guidance on authentication factors
- Verify specific regulatory requirements for your application domain

### Testing and Monitoring

- Conduct penetration testing specifically targeting authentication flows
- Test MFA bypass scenarios and recovery mechanisms
- Monitor for unusual authentication patterns and failed attempts
- Regularly audit MFA implementation against current threats
- Ensure security features maintain usability to prevent user circumvention

Following these guidelines based on the OWASP Multifactor Authentication framework will significantly reduce the risk of account compromise while maintaining reasonable usability for legitimate users.