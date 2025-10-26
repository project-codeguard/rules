---
description: Input Validation Security Best Practices
languages:
- c
- go
- java
- javascript
- php
- python
- ruby
- sql
- typescript
- xml
alwaysApply: false
---

## Input Validation Security Guidelines

This rule provides clear, actionable guidance for implementing robust input validation security functionality in applications.

### Introduction

Input validation ensures only properly formed data enters the workflow, preventing malformed data from persisting in the database and triggering malfunction of downstream components. Input validation should happen as early as possible in the data flow.

Data from all potentially untrusted sources should be subject to input validation, including Internet-facing web clients and backend feeds from suppliers, partners, vendors or regulators.

Input Validation should not be used as the primary method of preventing XSS, SQL Injection and other attacks but can significantly contribute to reducing their impact if implemented properly.

### Input Validation Strategies

- Syntactic validation: enforce correct syntax of structured fields (e.g. SSN, date, currency symbol)
- Semantic validation: enforce correctness of values in specific business context (e.g. start date before end date, price within expected range)

### Implementing Input Validation

- Data type validators available in web application frameworks (Django Validators, Apache Commons Validators)
- Validation against JSON Schema and XML Schema (XSD)
- Type conversion with strict exception handling (Integer.parseInt() in Java, int() in Python)
- Range checks for numerical parameters and length checks for strings
- Array of allowed values for small sets of string parameters
- Regular expressions covering the whole input string (^...$) avoiding "any character" wildcards

### Allowlist vs Denylist

Allowlist validation defines exactly what IS authorized; everything else is not authorized. For structured data (dates, SSNs, zip codes, emails), define strong validation patterns using regular expressions. For fixed options (dropdowns, radio buttons), input must match exactly one offered value.

### Validating Free-form Unicode Text

- Normalization: Ensure canonical encoding across all text
- Character category allowlisting: Use Unicode categories like "decimal digits" or "letters"
- Individual character allowlisting: Allow specific characters like apostrophe for names

### Regular Expressions (Regex)

Be aware of RegEx Denial of Service (ReDoS) attacks. Input validation should:
- Be applied to all input data
- Define allowed character sets
- Define minimum and maximum length (e.g. {1,25})

### Allow List Regular Expression Examples

U.S. Zip Code: `^\d{5}(-\d{4})?$`

Java Example:
```java
private static final Pattern zipPattern = Pattern.compile("^\d{5}(-\d{4})?$");

public void doPost(HttpServletRequest request, HttpServletResponse response) {
  try {
      String zipCode = request.getParameter("zip");
      if (!zipPattern.matcher(zipCode).matches()) {
          throw new YourValidationException("Improper zipcode format.");
      }
  } catch(YourValidationException e) {
      response.sendError(response.SC_BAD_REQUEST, e.getMessage());
  }
}
```

### Client-side vs Server-side Validation

Input validation must be implemented on the server-side before data processing, as client-side validation can be circumvented by attackers.

### File Upload Validation

Upload Verification:
- Validate filename uses expected extension type
- Enforce maximum file size limits
- Check ZIP files before extraction (target path, compression level, estimated size)

Upload Storage:
- Use server-generated random filenames
- Analyze uploaded files for malicious content
- Server defines file paths, not client

Beware of dangerous file types:
- crossdomain.xml / clientaccesspolicy.xml
- .htaccess and .htpasswd
- Web executable scripts: aspx, asp, css, swf, jsp, js, php, cgi

Image Upload:
- Use image rewriting libraries to verify and strip content
- Set extension based on detected content type
- Ensure content type is within defined image types

### Email Address Validation

Syntactic Validation:
- Contains two parts separated by @
- No dangerous characters (backticks, quotes, null bytes)
- Domain contains only letters, numbers, hyphens, periods
- Length limits: local part ≤ 63 chars, total ≤ 254 chars

Semantic Validation:
- Send verification email with secure token
- Token requirements: ≥32 chars, cryptographically random, single-use, time-limited