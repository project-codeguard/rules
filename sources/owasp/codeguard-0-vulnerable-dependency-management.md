---
description: Vulnerable Dependency Management
languages:
- c
- go
- javascript
- r
- xml
alwaysApply: false
---

## Vulnerable Dependency Management

Detect and mitigate security vulnerabilities in third-party dependencies through automated scanning, proper testing, and systematic remediation approaches.

### Automated Detection

Integrate vulnerability scanning from project inception using tools that cover multiple vulnerability sources:
- CVE databases (NIST National Vulnerability Database)
- Full disclosure sources (mailing lists, Exploit-DB)
- Provider-specific vulnerability feeds

Recommended tools:
- OWASP Dependency Check (Java, .NET, experimental support for Python, Ruby, PHP, Node.js, C/C++)
- NPM Audit (Node.js, JavaScript)
- OWASP Dependency Track (organization-wide management)

### Remediation Cases

Case 1 - Patched version available:
1. Update dependency version in testing environment
2. Run automated tests to verify functionality
3. If tests pass: deploy to production
4. If tests fail: update application code for API changes or report incompatibility to provider

Case 2 - Patch delayed, provider provides workaround:
1. Apply provider workaround if available
2. If provider lists impacted functions, add protective wrappers
3. Validate workaround in testing environment

Example protective wrapper for RCE vulnerability:
```java
public void callFunctionWithRCEIssue(String externalInput){
    //Apply input validation on the external input using regex
    if(Pattern.matches("[a-zA-Z0-9]{1,50}", externalInput)){
        //Call the flawed function using safe input
        functionWithRCEIssue(externalInput);
    }else{
        //Log the detection of exploitation
        SecurityLogger.warn("Exploitation of the RCE issue XXXXX detected !");
        //Raise an exception leading to a generic error send to the client...
    }
}
```

Case 3 - No patch available:
1. Analyze CVE description to understand vulnerability type (SQL injection, XSS, XXE, etc.)
2. Identify all application code calling the vulnerable dependency
3. Implement compensating controls based on vulnerability type
4. Create unit tests to verify protection effectiveness
5. For open source dependencies: consider creating and contributing patches

Case 4 - Previously unknown vulnerability discovered:
1. Notify provider with vulnerability details
2. If provider cooperates: follow Case 2 approach
3. If provider unresponsive: follow Case 3 approach

### Dependencies Analysis

Transitive dependencies: Act on direct dependencies when possible, as modifying transitive dependencies requires understanding complex dependency chains and can impact application stability.

Use dependency management tools to identify:
- Direct vs transitive dependency relationships
- All code paths using vulnerable components
- Impact scope of potential vulnerabilities

### Testing and Validation

Maintain comprehensive automated tests covering:
- Features using impacted dependencies
- Security controls added as mitigations
- Regression detection during updates

Run tests before and after dependency updates to ensure:
- Application functionality remains intact
- Security mitigations are effective
- No new vulnerabilities are introduced

### Risk Management

Document all vulnerability decisions including:
- Technical analysis and CVSS scoring
- Chosen mitigation approach and rationale
- Testing results and validation steps
- Risk acceptance decisions with business justification

Escalate risk acceptance decisions to Chief Risk Officer after thorough technical analysis.

### Continuous Monitoring

Implement continuous dependency scanning in CI/CD pipelines:
- Scan on every build
- Fail builds for high-severity vulnerabilities
- Generate reports for security team review
- Track remediation progress and compliance

Choose tools supporting false-positive flagging and multiple reliable input sources to handle different vulnerability disclosure methods.

### Prevention Guidelines

- Start dependency scanning from project inception
- Prefer fixing vulnerabilities at source (application or dependency) over external controls
- Keep dependencies updated regularly
- Monitor dependencies for maintenance status and community activity
- Consider dependency complexity and transitive dependency count when selecting libraries