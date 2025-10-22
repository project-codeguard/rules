---
description: Zero Trust Architecture Implementation - Security principles for designing
  systems with no implicit trust
languages:
- c
- go
- java
- javascript
- kotlin
- php
- python
- ruby
- scala
- shell
- swift
- typescript
- yaml
alwaysApply: false
---

## Implementing Zero Trust Architecture

Implementing Zero Trust Architecture (ZTA) principles in your applications is essential for modern security.

Zero Trust is built on the principle of "never trust, always verify" and assumes that threats exist both outside and inside the network. Key concepts include:

- No implicit trust based on network location or asset ownership
- Continuous verification of identity and device health
- Least privilege access to resources and data
- Microsegmentation of networks and applications
- Continuous monitoring and analytics for threat detection

### Authentication & Authorization

- Implement Strong Authentication using FIDO2/WebAuthn

- Implement Context-Aware Authorization
Implement authorization that considers multiple factors:

```java
// Java example of context-aware authorization
public class ZeroTrustAuthorizationService {
    public boolean authorizeAccess(User user, Resource resource, AccessContext context) {
        // 1. Verify user identity
        if (!identityService.verifyIdentity(user)) {
            logFailedAttempt("Identity verification failed", user, resource, context);
            return false;
        }

        // 2. Check device health and compliance
        if (!deviceService.isCompliant(context.getDeviceId())) {
            logFailedAttempt("Device not compliant", user, resource, context);
            return false;
        }

        // 3. Evaluate risk score based on multiple factors
        int riskScore = riskEngine.calculateScore(user, resource, context);
        if (riskScore > ACCEPTABLE_THRESHOLD) {
            logFailedAttempt("Risk score too high", user, resource, context);
            return false;
        }

        // 4. Check if user has required permissions
        if (!permissionService.hasPermission(user, resource, context.getRequestedAction())) {
            logFailedAttempt("Insufficient permissions", user, resource, context);
            return false;
        }

        // 5. Log successful access
        auditLogger.logAccess(user, resource, context);
        return true;
    }
}
```

- Implement Short-Lived Access Tokens

Implement token-based authentication with short lifetimes:

```python
# Python example using JWT with short expiration
import jwt
from datetime import datetime, timedelta

def generate_access_token(user_id, device_id, permissions):
    # Set token to expire in 15 minutes
    expiration = datetime.utcnow() + timedelta(minutes=15)

    payload = {
        'sub': user_id,
        'device_id': device_id,
        'permissions': permissions,
        'exp': expiration,
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4())  # Unique token ID
    }

    # Sign with appropriate algorithm and key
    token = jwt.encode(payload, SECRET_KEY, algorithm='ES256')

    # Store token metadata for potential revocation
    store_token_metadata(user_id, payload['jti'], device_id, expiration)

    return token
```

### Secure Communication

- Implement TLS 1.3 for all communications

- Implement API security measures:

```typescript
// TypeScript example of API security middleware
import express from 'express';
import rateLimit from 'express-rate-limit';
import helmet from 'helmet';

const app = express();

// Set security headers
app.use(helmet());

// Rate limiting
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', apiLimiter);

// API authentication middleware
app.use('/api/', (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  try {
    // Verify token and extract user info
    const user = verifyAndDecodeToken(token);

    // Check if token has been revoked
    if (isTokenRevoked(token)) {
      return res.status(401).json({ error: 'Token revoked' });
    }

    // Add user info to request for downstream handlers
    req.user = user;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
});

// Payload validation middleware
app.use(express.json({
  verify: (req, res, buf) => {
    try {
      // Check if JSON is valid and meets schema requirements
      validateSchema(buf.toString(), req.path);
    } catch (e) {
      throw new Error('Invalid JSON payload');
    }
  },
  limit: '100kb' // Limit payload size
}));
```

### Monitoring and Logging

- Implement Comprehensive Logging

```csharp
// C# example of detailed security logging
public class SecurityLogger
{
    private readonly ILogger _logger;

    public SecurityLogger(ILogger logger)
    {
        _logger = logger;
    }

    public void LogAccessAttempt(string userId, string resourceId, bool success, AccessContext context)
    {
        var logEvent = new SecurityEvent
        {
            EventType = success ? "access_granted" : "access_denied",
            Timestamp = DateTime.UtcNow,
            UserId = userId,
            ResourceId = resourceId,
            IpAddress = context.IpAddress,
            DeviceId = context.DeviceId,
            DeviceHealth = context.DeviceHealthStatus,
            Location = context.GeoLocation,
            RequestedPermissions = context.RequestedPermissions,
            RiskScore = context.RiskScore
        };

        // Log with appropriate level
        if (success)
        {
            _logger.LogInformation("Access granted: {Event}", JsonSerializer.Serialize(logEvent));
        }
        else
        {
            _logger.LogWarning("Access denied: {Event}", JsonSerializer.Serialize(logEvent));
        }
    }
}
```

### Implement fine-grained network and application segmentation


```yaml
# Kubernetes Network Policy example for microsegmentation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-backend-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 443
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector:
        matchLabels:
          name: monitoring
      podSelector:
        matchLabels:
          app: telemetry
    ports:
    - protocol: TCP
      port: 9090
```