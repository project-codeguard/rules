---
description: Injection Prevention Best Practices
languages:
- c
- go
- java
- javascript
- php
- powershell
- python
- ruby
- shell
- sql
- typescript
alwaysApply: false
version: 0.1.0
severity: medium
---

## Injection Prevention Guidelines

This rule provides clear, actionable guidance for preventing injection flaws across multiple languages and injection types. Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query.

### Introduction

Injection attacks, especially SQL Injection, are unfortunately very common. Injection flaws occur when an application sends untrusted data to an interpreter. Injection flaws are very prevalent, particularly in legacy code, often found in SQL queries, LDAP queries, XPath queries, OS commands, program arguments, etc.

### SQL Injection Prevention

Defense Option 1: Prepared Statements (with Parameterized Queries)

Safe Java Prepared Statement Example:
```java
// This should REALLY be validated too
String custname = request.getParameter("customerName"); 
String query = "SELECT account_balance FROM user_data WHERE user_name = ?";
PreparedStatement pstmt = connection.prepareStatement( query );
pstmt.setString( 1, custname); 
ResultSet results = pstmt.executeQuery( );
```

Defense Option 2: Stored Procedures

Safe Java Stored Procedure Example:
```java
// This should REALLY be validated
String custname = request.getParameter("customerName");
try {
 CallableStatement cs = connection.prepareCall("{call sp_getAccountBalance(?)}");
 cs.setString(1, custname);
 ResultSet results = cs.executeQuery();
 // Result set handling...
} catch (SQLException se) {
 // Logging and error handling...
}
```

Defense Option 3: Allow-List Input Validation

Defense Option 4: Escaping All User-Supplied Input

### LDAP Injection Prevention

Escape all variables using the right LDAP encoding function

Safe Java for LDAP escaping Example:
```java
public String escapeDN (String name) {
 //From RFC 2253 and the / character for JNDI
 final char[] META_CHARS = {'+', '"', '<', '>', ';', '/'};
 String escapedStr = new String(name);
 //Backslash is both a Java and an LDAP escape character,
 //so escape it first
 escapedStr = escapedStr.replaceAll("\\\\\\\\","\\\\\\\\");
 //Positional characters - see RFC 2253
 escapedStr = escapedStr.replaceAll("\^#","\\\\\\\\#");
 escapedStr = escapedStr.replaceAll("\^ | $","\\\\\\\\ ");
 for (int i=0 ; i < META_CHARS.length ; i++) {
        escapedStr = escapedStr.replaceAll("\\\\" +
                     META_CHARS[i],"\\\\\\\\" + META_CHARS[i]);
 }
 return escapedStr;
}
```

```java
public String escapeSearchFilter (String filter) {
 //From RFC 2254
 String escapedStr = new String(filter);
 escapedStr = escapedStr.replaceAll("\\\\\\\\","\\\\\\\\5c");
 escapedStr = escapedStr.replaceAll("\\\\\*","\\\\\\\\2a");
 escapedStr = escapedStr.replaceAll("\\\\(","\\\\\\\\28");
 escapedStr = escapedStr.replaceAll("\\\\)","\\\\\\\\29");
 escapedStr = escapedStr.replaceAll("\\\\" +
               Character.toString('\u0000'), "\\\\\\\\00");
 return escapedStr;
}
```

### Operating System Commands

If it is considered unavoidable the call to a system command incorporated with user-supplied input, the following two layers of defense should be used:

1. Parameterization - If available, use structured mechanisms that automatically enforce the separation between data and command
2. Input validation - the values for commands and the relevant arguments should be both validated:
   - Commands must be validated against a list of allowed commands
   - Arguments should be validated using positive or allowlist input validation
   - Allow-list Regular Expression - explicitly define a list of good characters allowed and maximum length. Ensure that metacharacters like `& | ; $ > < \` \ !` and whitespaces are not part of the Regular Expression

Example regular expression: `^[a-z0-9]{3,10}$`

Incorrect Usage:
```java
ProcessBuilder b = new ProcessBuilder("C:\DoStuff.exe -arg1 -arg2");
```

Correct Usage:
```java
ProcessBuilder pb = new ProcessBuilder("TrustedCmd", "TrustedArg1", "TrustedArg2");
Map<String, String> env = pb.environment();
pb.directory(new File("TrustedDir"));
Process p = pb.start();
```

### Injection Prevention Rules

Rule #1 (Perform proper input validation)
- Perform proper input validation. Positive or allowlist input validation with appropriate canonicalization is recommended, but is not a complete defense as many applications require special characters in their input.

Rule #2 (Use a safe API)
- The preferred option is to use a safe API which avoids the use of the interpreter entirely or provides a parameterized interface. Be careful of APIs, such as stored procedures, that are parameterized, but can still introduce injection under the hood.

Rule #3 (Contextually escape user data)
- If a parameterized API is not available, you should carefully escape special characters using the specific escape syntax for that interpreter.