---
description: Virtual Patching Security
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- typescript
- xml
alwaysApply: false
version: 0.1.0
severity: medium
---

## Virtual Patching Security

Implement temporary security controls to protect against known vulnerabilities while developing permanent code fixes through security policy enforcement layers.

### Virtual Patching Definition

A security policy enforcement layer which prevents and reports exploitation attempts of known vulnerabilities. Virtual patches analyze transactions and intercept attacks in transit so malicious traffic never reaches the web application, providing protection while actual source code remains unmodified.

### When Virtual Patching is Needed

Virtual patching addresses real-world scenarios where immediate code fixes are not feasible:

- Lack of resources: Developers allocated to other projects
- Third-party software: Code cannot be modified by users
- Outsourced development: Changes require new project authorization

Important: Code level fixes and virtual patching are NOT mutually exclusive. They are executed by different teams (developers vs. security operations) and can run in tandem.

### Virtual Patching Goals

- Minimize Time-to-Fix: Implement mitigation as soon as possible while code fixes are developed
- Attack Surface Reduction: Focus on minimizing attack vectors, even partial reduction (50% in 10 minutes vs 100% in 48 hours)

### Virtual Patching Tools

Available tools for implementing virtual patches:
- Intermediary devices such as WAF or IPS appliances
- Web server plugins such as ModSecurity
- Application layer filters such as ESAPI WAF

### Virtual Patching Methodology

Follow structured workflow for consistent, repeatable virtual patching:

1. Preparation
2. Identification  
3. Analysis
4. Virtual Patch Creation
5. Implementation/Testing
6. Recovery/Follow-Up

### Preparation Phase

Critical preparation items before incidents occur:

- Public/Vendor Vulnerability Monitoring: Subscribe to vendor alert mailing lists for commercial software
- Virtual Patching Pre-Authorization: Expedite governance processes since virtual patches don't modify source code
- Deploy Virtual Patching Tools in Advance: Install ModSecurity WAF or similar tools ready for activation
- Increase HTTP Audit Logging: Capture request URI, full headers, request/response bodies for incident analysis

### Analysis Phase

Recommended analysis steps:

1. Determine virtual patching applicability for vulnerability type
2. Utilize bug tracking system for vulnerability information management
3. Verify vulnerability identifier (CVE name/number)
4. Designate impact level for proper prioritization
5. Specify affected software versions
6. List configuration requirements to trigger vulnerability
7. Collect Proof of Concept (PoC) exploit code for analysis and testing

### Virtual Patch Creation Principles

Two main requirements for accurate virtual patches:
- No false positives: Never block legitimate traffic
- No false negatives: Never miss attacks, even with evasion attempts

### Positive Security (Allow List) Virtual Patches (Recommended)

Positive security model provides comprehensive input validation by specifying valid input characteristics and denying anything non-conformant.

Example ModSecurity virtual patch for SQL injection protection:

```text
##
## Verify we only receive 1 parameter called "reqID"
##
SecRule REQUEST_URI "@contains /wp-content/plugins/levelfourstorefront/scripts/administration/exportsubscribers.php" "chain,id:1,phase:2,t:none,t:Utf8toUnicode,t:urlDecodeUni,t:normalizePathWin,t:lowercase,block,msg:'Input Validation Error for \'reqID\' parameter - Duplicate Parameters Names Seen.',logdata:'%{matched_var}'"
  SecRule &ARGS:/reqID/ "!@eq 1"

##
## Verify reqID's payload only contains integers
##
SecRule REQUEST_URI "@contains /wp-content/plugins/levelfourstorefront/scripts/administration/exportsubscribers.php" "chain,id:2,phase:2,t:none,t:Utf8toUnicode,t:urlDecodeUni,t:normalizePathWin,t:lowercase,block,msg:'Input Validation Error for \'reqID\' parameter.',logdata:'%{args.reqid}'"
  SecRule ARGS:/reqID/ "!@rx ^[0-9]+$"
```

### Negative Security (Block List) Virtual Patches

Negative security model detects specific known attacks rather than allowing only valid traffic.

Example PoC attack payload:
```text
http://localhost/wordpress/wp-content/plugins/levelfourstorefront/scripts/administration/exportsubscribers.php?reqID=1' or 1='1
```

Example ModSecurity block list virtual patch:
```text
SecRule REQUEST_URI "@contains /wp-content/plugins/levelfourstorefront/scripts/administration/exportsubscribers.php" "chain,id:1,phase:2,t:none,t:Utf8toUnicode,t:urlDecodeUni,t:normalizePathWin,t:lowercase,block,msg:'Input Validation Error for \'reqID\' parameter.',logdata:'%{args.reqid}'"
  SecRule ARGS:/reqID/ "@pm '"
```

### Security Model Comparison

Positive vs Negative Security considerations:
- Negative security: Faster implementation but more evasion possibilities
- Positive security: Better protection but manual process, less scalable for large/dynamic sites
- Positive security recommended for specific vulnerability locations identified by alerts

### Avoid Exploit-Specific Patches

Resist creating patches that only block exact exploit payloads. Example poor approach for XSS:

```html
<script>
  alert('XSS Test')
</script>
```

Blocking only this exact payload provides minimal long-term protection value.

### Automated Virtual Patch Creation

Tools for automated patch creation from vulnerability reports:
- OWASP ModSecurity Core Rule Set (CRS) Scripts: Auto-convert XML output from tools like ZAP
- ThreadFix Virtual Patching: Convert vulnerability XML data into ModSecurity patches
- Direct WAF Importing: Commercial WAF products import DAST tool XML reports

### Implementation and Testing

Testing tools for virtual patch validation:
- Web browsers
- Command-line clients (Curl, Wget)
- Local proxy servers (ZAP)
- ModSecurity AuditViewer for log manipulation and re-injection

Testing steps:
- Implement patches initially in "Log Only" mode to prevent false positives
- Request retest from vulnerability identification team
- Return to analysis phase if evasions occur during retesting

### Recovery and Follow-Up

Post-implementation activities:
- Update ticket system with virtual patch details and rule IDs
- Conduct periodic re-assessments to determine when virtual patches can be removed
- Run virtual patch alert reports to demonstrate protection value
- Track time-to-fix metrics for different vulnerability types

### Developer Integration Guidelines

1. Prioritize permanent code fixes over virtual patches
2. Collaborate with security teams on virtual patch requirements and testing
3. Understand virtual patch limitations and temporary nature
4. Provide input on normal application behavior for positive security rules
5. Review virtual patch logs for attack patterns that inform secure coding practices
6. Plan code fixes to address root causes protected by virtual patches
7. Participate in virtual patch removal process once code fixes are deployed
8. Document application-specific requirements for virtual patch creation