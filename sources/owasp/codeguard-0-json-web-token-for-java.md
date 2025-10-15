---
description: JSON Web Token Security for Java
languages:
- c
- java
- javascript
- typescript
- xml
- yaml
alwaysApply: false
version: 0.1.0
severity: medium
---

## JSON Web Token Security for Java

Key security practices for implementing JWT in Java applications.

### Algorithm Security

Always specify the expected algorithm explicitly:

```java
// Prevent 'none' algorithm attack
JWTVerifier verifier = JWT.require(Algorithm.HMAC256(keyHMAC)).build();
DecodedJWT decodedToken = verifier.verify(token);
```

### Token Sidejacking Prevention

Code to create the token after successful authentication.

``` java
// HMAC key - Block serialization and storage as String in JVM memory
private transient byte[] keyHMAC = ...;
// Random data generator
private SecureRandom secureRandom = new SecureRandom();

...

//Generate a random string that will constitute the fingerprint for this user
byte[] randomFgp = new byte[50];
secureRandom.nextBytes(randomFgp);
String userFingerprint = DatatypeConverter.printHexBinary(randomFgp);

//Add the fingerprint in a hardened cookie - Add cookie manually because
//SameSite attribute is not supported by javax.servlet.http.Cookie class
String fingerprintCookie = "__Secure-Fgp=" + userFingerprint
                           + "; SameSite=Strict; HttpOnly; Secure";
response.addHeader("Set-Cookie", fingerprintCookie);

//Compute a SHA256 hash of the fingerprint in order to store the
//fingerprint hash (instead of the raw value) in the token
//to prevent an XSS to be able to read the fingerprint and
//set the expected cookie itself
MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] userFingerprintDigest = digest.digest(userFingerprint.getBytes("utf-8"));
String userFingerprintHash = DatatypeConverter.printHexBinary(userFingerprintDigest);

//Create the token with a validity of 15 minutes and client context (fingerprint) information
Calendar c = Calendar.getInstance();
Date now = c.getTime();
c.add(Calendar.MINUTE, 15);
Date expirationDate = c.getTime();
Map<String, Object> headerClaims = new HashMap<>();
headerClaims.put("typ", "JWT");
String token = JWT.create().withSubject(login)
   .withExpiresAt(expirationDate)
   .withIssuer(this.issuerID)
   .withIssuedAt(now)
   .withNotBefore(now)
   .withClaim("userFingerprint", userFingerprintHash)
   .withHeader(headerClaims)
   .sign(Algorithm.HMAC256(this.keyHMAC));
```

Code to validate the token.

``` java
// HMAC key - Block serialization and storage as String in JVM memory
private transient byte[] keyHMAC = ...;

...

//Retrieve the user fingerprint from the dedicated cookie
String userFingerprint = null;
if (request.getCookies() != null && request.getCookies().length > 0) {
 List<Cookie> cookies = Arrays.stream(request.getCookies()).collect(Collectors.toList());
 Optional<Cookie> cookie = cookies.stream().filter(c -> "__Secure-Fgp"
                                            .equals(c.getName())).findFirst();
 if (cookie.isPresent()) {
   userFingerprint = cookie.get().getValue();
 }
}

//Compute a SHA256 hash of the received fingerprint in cookie in order to compare
//it to the fingerprint hash stored in the token
MessageDigest digest = MessageDigest.getInstance("SHA-256");
byte[] userFingerprintDigest = digest.digest(userFingerprint.getBytes("utf-8"));
String userFingerprintHash = DatatypeConverter.printHexBinary(userFingerprintDigest);

//Create a verification context for the token
JWTVerifier verifier = JWT.require(Algorithm.HMAC256(keyHMAC))
                              .withIssuer(issuerID)
                              .withClaim("userFingerprint", userFingerprintHash)
                              .build();

//Verify the token, if the verification fail then an exception is thrown
DecodedJWT decodedToken = verifier.verify(token);
```


### Token Revocation

Implement token blacklist for logout functionality:


Code in charge of adding a token to the denylist and checking if a token is revoked.

``` java
/**
* Handle the revocation of the token (logout).
* Use a DB in order to allow multiple instances to check for revoked token
* and allow cleanup at centralized DB level.
*/
public class TokenRevoker {

 /** DB Connection */
 @Resource("jdbc/storeDS")
 private DataSource storeDS;

 /**
  * Verify if a digest encoded in HEX of the ciphered token is present
  * in the revocation table
  *
  * @param jwtInHex Token encoded in HEX
  * @return Presence flag
  * @throws Exception If any issue occur during communication with DB
  */
 public boolean isTokenRevoked(String jwtInHex) throws Exception {
     boolean tokenIsPresent = false;
     if (jwtInHex != null && !jwtInHex.trim().isEmpty()) {
         //Decode the ciphered token
         byte[] cipheredToken = DatatypeConverter.parseHexBinary(jwtInHex);

         //Compute a SHA256 of the ciphered token
         MessageDigest digest = MessageDigest.getInstance("SHA-256");
         byte[] cipheredTokenDigest = digest.digest(cipheredToken);
         String jwtTokenDigestInHex = DatatypeConverter.printHexBinary(cipheredTokenDigest);

         //Search token digest in HEX in DB
         try (Connection con = this.storeDS.getConnection()) {
             String query = "select jwt_token_digest from revoked_token where jwt_token_digest = ?";
             try (PreparedStatement pStatement = con.prepareStatement(query)) {
                 pStatement.setString(1, jwtTokenDigestInHex);
                 try (ResultSet rSet = pStatement.executeQuery()) {
                     tokenIsPresent = rSet.next();
                 }
             }
         }
     }

     return tokenIsPresent;
 }


### Secure Client Storage

Store tokens in sessionStorage with fingerprint binding:

```javascript
// Store in sessionStorage, not localStorage
sessionStorage.setItem("token", data.token);

// Send as Bearer token
xhr.setRequestHeader("Authorization", "bearer " + token);
```

### Strong Secrets

Use strong HMAC secrets or RSA keys:
- HMAC secrets: minimum 64 characters, cryptographically random
- Prefer RSA or ECDSA over HMAC for better security
- Never hardcode secrets in source code