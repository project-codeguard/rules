---
description: LDAP Injection Prevention
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
- yaml
alwaysApply: false
---

## LDAP Injection Prevention Guidelines

Essential practices for preventing LDAP injection vulnerabilities in applications that use directory services.

### Understanding LDAP Injection

LDAP injection occurs when untrusted user input is improperly incorporated into LDAP queries, potentially allowing attackers to bypass authentication, access unauthorized data, or modify directory information.

Two main components vulnerable to injection:
- **Distinguished Names (DNs)**: Unique identifiers like `cn=Richard Feynman, ou=Physics Department, dc=Caltech, dc=edu`
- **Search Filters**: Query criteria using boolean logic in Polish notation

### Primary Defense: Proper Escaping

#### Distinguished Name Escaping

Characters that must be escaped in DNs: `\ # + < > , ; " =` and leading or trailing spaces.

Characters allowed in DNs (no escaping needed): `* ( ) . & - _ [ ] ` ~ | @ $ % ^ ? : { } ! '`

#### Search Filter Escaping

Characters that must be escaped in search filters: `* ( ) \ NUL`

### Safe Java Example

The original OWASP document provides this allowlist validation approach:

```java
// String userSN = "Sherlock Holmes"; // Valid
// String userPassword = "secret2"; // Valid
// ... beginning of LDAPInjection.searchRecord()...
sc.setSearchScope(SearchControls.SUBTREE_SCOPE);
String base = "dc=example,dc=com";

if (!userSN.matches("[\\w\\s]*") || !userPassword.matches("[\\w]*")) {
 throw new IllegalArgumentException("Invalid input");
}

String filter = "(&(sn = " + userSN + ")(userPassword=" + userPassword + "))";
// ... remainder of LDAPInjection.searchRecord()... 
```

### Safe .NET Encoding

Use .NET AntiXSS (now the Encoder class) LDAP encoding functions:
- `Encoder.LdapFilterEncode(string)` - encodes according to RFC4515
- `Encoder.LdapDistinguishedNameEncode(string)` - encodes according to RFC2253
- `LdapDistinguishedNameEncode(string, bool, bool)` - with optional initial/final character escaping

### Framework-Based Protection

Use frameworks that automatically protect from LDAP injection:
- **Java**: OWASP ESAPI with `encodeForLDAP(String)` and `encodeForDN(String)`
- **.NET**: LINQ to LDAP (for .NET Framework 4.5 or lower) provides automatic LDAP encoding

### Additional Defenses

#### Least Privilege
- Minimize privileges assigned to LDAP binding accounts
- Use read-only accounts where possible
- Avoid administrative accounts for application connections

#### Bind Authentication
- Configure LDAP with bind authentication to add verification and authorization checks
- Prevent anonymous connections and unauthenticated binds

#### Allow-List Input Validation
- Validate input against known-safe characters before LDAP query construction
- Normalize user input before validation
- Store sensitive data in sanitized form

### Key Security Requirements

- Always escape untrusted data before incorporating into LDAP queries
- Use context-appropriate escaping (DN vs search filter)
- Implement comprehensive input validation with allowlists
- Use established security libraries rather than custom escaping
- Apply principle of least privilege to LDAP connections
- Enable proper authentication mechanisms to prevent bypass attacks