---
description: Standardized Security Event Logging Vocabulary
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
version: 0.1.0
severity: medium
---

## Security Event Logging Vocabulary Guidelines

Standardized vocabulary for logging security events to improve monitoring, alerting, and incident response.

### Standard Event Format

NOTE: All dates should be logged in ISO 8601 format WITH UTC offset to ensure maximum portability

```json
{
    "datetime": "2021-01-01T01:01:01-0700",
    "appid": "foobar.netportal_auth",
    "event": "AUTHN_login_success:joebob1",
    "level": "INFO",
    "description": "User joebob1 login successfully",
    "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "source_ip": "165.225.50.94",
    "host_ip": "10.12.7.9",
    "hostname": "portalauth.foobar.com",
    "protocol": "https",
    "port": "440",
    "request_uri": "/api/v2/auth/",
    "request_method": "POST",
    "region": "AWS-US-WEST-2",
    "geo": "USA"
}
```

### Authentication Events [AUTHN]

authn_login_success[:userid] - Successful login (Level: INFO)
authn_login_successafterfail[:userid,retries] - Successful login after previous failures (Level: INFO)
authn_login_fail[:userid] - Failed login attempt (Level: WARN)
authn_login_fail_max[:userid,maxlimit] - Maximum failures reached (Level: WARN)
authn_login_lock[:userid,reason] - Account locked (reasons: maxretries, suspicious, customer, other) (Level: WARN)
authn_password_change[:userid] - Password successfully changed (Level: INFO)
authn_password_change_fail[:userid] - Password change failed (Level: CRITICAL)
authn_impossible_travel[:userid,region1,region2] - User in distant locations simultaneously (Level: CRITICAL)
authn_token_created[:userid,entitlements] - Service token created (Level: INFO)
authn_token_revoked[:userid,tokenid] - Token revoked (Level: INFO)
authn_token_reuse[:userid,tokenid] - Revoked token reuse attempt (Level: CRITICAL)
authn_token_delete[:appid] - Token deleted (Level: WARN)

### Authorization Events [AUTHZ]

authz_fail[:userid,resource] - Unauthorized access attempt (Level: CRITICAL)
authz_change[:userid,from,to] - User entitlements changed (Level: WARN)
authz_admin[:userid,event] - All privileged user activity (Level: WARN)

### Encryption/Decryption Events [CRYPT]

crypt_decrypt_fail[userid] - Decryption failure (Level: WARN)
crypt_encrypt_fail[userid] - Encryption failure (Level: WARN)

### Excessive Use Events [EXCESS]

excess_rate_limit_exceeded[userid,max] - Rate limit exceeded (Level: WARN)

### File Upload Events [UPLOAD]

upload_complete[userid,filename,type] - File upload completed (Level: INFO)
upload_stored[filename,from,to] - File stored with new name/location (Level: INFO)
upload_validation[filename,(virusscan|imagemagick|...):(FAILED|incomplete|passed)] - File validation results (Level: INFO|CRITICAL)
upload_delete[userid,fileid] - File deleted (Level: INFO)

### Input Validation Events [INPUT]

input_validation_fail:[(fieldone,fieldtwo...),userid] - Server-side validation failure (Level: WARN)

### Malicious Behavior Events [MALICIOUS]

malicious_excess_404:[userid|IP,useragent] - Excessive 404s indicating force-browsing (Level: WARN)
malicious_extraneous:[userid|IP,inputname,useragent] - Unexpected input data submitted (Level: CRITICAL)
malicious_attack_tool:[userid|IP,toolname,useragent] - Known attack tools detected (Level: CRITICAL)
malicious_cors:[userid|IP,useragent,referer] - Illegal cross-origin request (Level: CRITICAL)
malicious_direct_reference:[userid|IP,useragent] - Direct object reference attempt (Level: CRITICAL)

### Privilege Changes Events [PRIVILEGE]

privilege_permissions_changed:[userid,file|object,fromlevel,tolevel] - Object permissions changed (Level: WARN)

### Sensitive Data Events [DATA]

sensitive_create:[userid,file|object] - Sensitive data created (Level: WARN)
sensitive_read:[userid,file|object] - Sensitive data accessed (Level: WARN)
sensitive_update:[userid,file|object] - Sensitive data modified (Level: WARN)
sensitive_delete:[userid,file|object] - Sensitive data marked for deletion (Level: WARN)

### Sequence Errors Events [SEQUENCE]

sequence_fail:[userid] - Business logic flow bypassed (Level: CRITICAL)

### Session Management Events [SESSION]

session_created:[userid] - New authenticated session (Level: INFO)
session_renewed:[userid] - Session extended after expiry warning (Level: INFO)
session_expired:[userid,reason] - Session expired (reasons: logout, timeout, revoked) (Level: INFO)
session_use_after_expire:[userid] - Expired session use attempt (Level: CRITICAL)

### System Events [SYS]

sys_startup:[userid] - System started (Level: WARN)
sys_shutdown:[userid] - System shut down (Level: WARN)
sys_restart:[userid] - System restarted (Level: WARN)
sys_crash[:reason] - System crash (Level: WARN)
sys_monitor_disabled:[userid,monitor] - Security monitoring disabled (Level: WARN)
sys_monitor_enabled:[userid,monitor] - Security monitoring enabled (Level: WARN)

### User Management Events [USER]

user_created:[userid,newuserid,attributes[one,two,three]] - New user created (Level: WARN)
user_updated:[userid,onuserid,attributes[one,two,three]] - User account updated (Level: WARN)
user_archived:[userid,onuserid] - User account archived (Level: WARN)
user_deleted:[userid,onuserid] - User account deleted (Level: WARN)

### Data Exclusions

Never log sensitive information: private or secret information, source code, keys, certificates, authentication passwords, session identification values, access tokens, sensitive personal data, PII, database connection strings, encryption keys, bank account or payment card data, commercially-sensitive information.

### Implementation Requirements

- Use ISO 8601 format with UTC offset for all timestamps
- Include application identifier (appid) for correlation  
- Apply consistent severity levels (INFO, WARN, CRITICAL)
- Include relevant context (IP addresses, user agents, request details)
- Consider data privacy regulations when logging user information
- Fields logged after event type should be considered optional based on business needs and data stewardship responsibilities