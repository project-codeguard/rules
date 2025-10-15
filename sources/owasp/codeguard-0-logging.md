---
description: Secure Application Logging
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## Application Logging Security Guidelines

Essential practices for implementing secure application logging for security monitoring, incident response, and compliance.

### Purpose and Use Cases

Application logging provides critical data for both security and operational purposes beyond infrastructure logging alone.

**Security Use Cases**:
- Anti-automation monitoring and identifying security incidents
- Monitoring policy violations and audit trails
- Compliance monitoring and data for investigations
- Contributing application-specific data for incident investigation
- Helping defend against vulnerability identification and exploitation

### Which Events to Log

Always log these security-relevant events:

**Input/Output Validation**:
- Input validation failures (protocol violations, unacceptable encodings, invalid parameters)
- Output validation failures (database record mismatches, invalid data encoding)

**Authentication and Authorization**:
- Authentication successes and failures
- Authorization (access control) failures
- Session management failures (cookie modifications, suspicious JWT validation failures)

**System Events**:
- Application errors and system events (syntax/runtime errors, connectivity problems)
- Application start-ups, shut-downs, and logging initialization
- Network connections and associated failures (backend TLS failures, certificate validation failures)

**High-Risk Operations**:
- User administration actions (user addition/deletion, privilege changes)
- Use of administrative privileges or default/shared accounts
- Access to sensitive data (payment cardholder data)
- Encryption activities (cryptographic key use or rotation)
- Data import/export and file uploads
- Deserialization failures

**Business Logic Events**:
- Legal opt-ins (permissions, terms of use, consent)
- Suspicious business logic activities (bypassing flow control, exceeding limitations)

### Event Attributes

Each log entry must record "when, where, who and what" with sufficient detail:

**When**: Log date/time in international format, event timestamp, interaction identifier
**Where**: Application identifier, address, service name, geolocation, code location
**Who**: Source address, user identity (if authenticated), user type classification
**What**: Event type, severity, security event flag, description, result status, reason

### Data to Exclude

Never log sensitive data directly - remove, mask, sanitize, hash, or encrypt:

- Application source code and session identification values
- Access tokens and authentication passwords
- Database connection strings and encryption keys
- Bank account or payment card holder data
- Sensitive personal data and PII
- Data of higher security classification than the logging system
- Commercially-sensitive information

### Event Collection Implementation

Implement application-wide log handler with security controls:

- Perform input validation on event data from other trust zones
- Perform sanitization on all event data to prevent log injection attacks (CR, LF, delimiter characters)
- Encode data correctly for the output format
- Apply SQL injection prevention if writing to databases
- Ensure logging failures don't prevent application operation or cause information leakage
- Synchronize time across all servers and devices

### Storage and Protection

**File System Storage**:
- Use separate partition from operating system and application files
- Apply strict permissions on directories and files
- Keep logs outside web-accessible locations
- Configure with plain text MIME type if web-accessible

**Database Storage**:
- Use separate database account only for writing log data
- Apply very restrictive database, table, function and command permissions

**Data Protection**:
- Use standard formats over secure protocols (CLFS, CEF over syslog)
- Build in tamper detection for record modification/deletion
- Store or copy log data to read-only media as soon as possible
- Record and monitor all access to logs
- Restrict and periodically review privileges to read log data

### Secure Transmission

When sending log data over untrusted networks:
- Use secure transmission protocols
- Consider whether origin of event data needs verification
- Perform due diligence checks before sending to third parties

### Verification and Testing

Include logging in security verification processes:
- Ensure logging works correctly and consistently
- Test mechanisms are not susceptible to injection attacks
- Ensure no unwanted side-effects when logging occurs
- Test effect of logging failures (database connectivity loss, filesystem issues)
- Verify access controls on event log data
- Ensure logging cannot cause denial of service through resource depletion

### Monitoring and Operation

- Incorporate application logging into centralized log management systems
- Enable alerting for serious events with immediate team notification
- Detect when logging has stopped or has been tampered with
- Share relevant event information with detection systems and intelligence gathering
- Maintain proper log retention periods per legal/regulatory requirements

### Protection Against Log Attacks

Logs may be targeted for attacks on:

**Confidentiality**: Unauthorized access to sensitive information stored in logs
**Integrity**: Tampering with log data or leveraging logs for exploitation
**Availability**: Flooding logs to exhaust resources or prevent further logging
**Accountability**: Preventing log writes or causing wrong identity logging to cover tracks

Implement appropriate controls to protect against these attack vectors while maintaining the logging system's security and reliability.