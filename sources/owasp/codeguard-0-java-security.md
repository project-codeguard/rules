---
description: Java Security Best Practices
languages:
- c
- java
- javascript
- typescript
- xml
- yaml
alwaysApply: false
---

## Java Security Guidelines

Key security practices for secure Java application development.

### SQL Injection Prevention

Use parameterized queries to prevent SQL injection:

```java
// Safe - PreparedStatement with parameters
String query = "select * from color where friendly_name = ?";
try (PreparedStatement pStatement = con.prepareStatement(query)) {
    pStatement.setString(1, userInput);
    try (ResultSet rSet = pStatement.executeQuery()) {
        // Process results
    }
}
```

### JPA Query Security

Use parameterized JPA queries:

```java
// Safe - Named parameters
String queryPrototype = "select c from Color c where c.friendlyName = :colorName";
Query queryObject = entityManager.createQuery(queryPrototype);
Color c = (Color) queryObject.setParameter("colorName", userInput).getSingleResult();
```

### XSS Prevention

Apply input validation and output encoding:

```java
// Input validation with allowlist
if (!Pattern.matches("[a-zA-Z0-9\\s\\-]{1,50}", userInput)) {
    return false;
}

// Output sanitization
PolicyFactory policy = new HtmlPolicyBuilder().allowElements("p", "strong").toFactory();
String safeOutput = policy.sanitize(outputToUser);
safeOutput = Encode.forHtml(safeOutput);
```

### Secure Logging

Use parameterized logging to prevent log injection:

```java
// Safe - parameterized logging
logger.warn("Login failed for user {}.", username);

// Avoid - string concatenation
// logger.warn("Login failed for user " + username);
```

### Cryptography Best Practices

Use trusted cryptographic libraries and secure algorithms:

```java
// Use AES-GCM with proper nonce management
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(128, nonce);
cipher.init(Cipher.ENCRYPT_MODE, secretKey, gcmParameterSpec);

// Generate secure random nonces
byte[] nonce = new byte[12];
SecureRandom.getInstanceStrong().nextBytes(nonce);
```

### Key Security Requirements

- Never hardcode cryptographic keys in source code
- Use Google Tink or similar trusted crypto libraries when possible
- Avoid writing custom cryptographic implementations
- Implement proper key rotation and management
- Keep all dependencies updated with security patches