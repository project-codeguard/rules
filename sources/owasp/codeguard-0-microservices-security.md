---
description: Microservices Security Best Practices
languages:
- c
- go
- java
- javascript
- python
- ruby
- typescript
- yaml
alwaysApply: false
---

## Microservices Security Guidelines

Essential security practices for implementing authentication, authorization, and logging in microservices-based systems.

### Edge-Level Authorization

API gateways can centralize authorization enforcement for downstream microservices, but have limitations:
- Pushing all authorization decisions to the gateway becomes hard to manage in complex ecosystems
- The API gateway may become a single point of decision violating "defense in depth"
- Operation teams typically own gateways, slowing development velocity

**Recommendation**: Implement authorization at both edge level (coarse-grained) and service level (fine-grained).

### Service-Level Authorization Patterns

**NIST Components**:
- Policy Administration Point (PAP): User interface for creating and managing access control rules
- Policy Decision Point (PDP): Computes access decisions by evaluating access control policy
- Policy Enforcement Point (PEP): Enforces policy decisions for protected objects
- Policy Information Point (PIP): Retrieval source of attributes for policy evaluation

#### Centralized Pattern with Embedded Policy Decision Point

**Recommended approach**: Access control rules defined centrally but stored and evaluated at microservice level.

1. Access control rules defined using PAP and delivered to embedded PDP with required attributes
2. When subject invokes microservice endpoint, microservice code invokes the PDP 
3. PDP generates access control policy decision by evaluating input against rules and attributes
4. Microservice enforces authorization based on PDP decision

**Implementation**: PDP implemented as microservice built-in library or sidecar in service mesh architecture.

### Authorization Implementation Recommendations

1. Use special language to express policy instead of hardcoding in source code
2. Implement as platform-level solution managed by dedicated security team
3. Use widely-adopted solutions rather than custom implementations
4. Implement "defense in depth" principle:
   - Gateway/proxy level: coarse-grained authorization
   - Microservice level: fine-grained decisions using shared authorization components
   - Business code level: business-specific access control rules
5. Implement formal procedures for access control policy development, approval, and rollout

### External Entity Identity Propagation

**Problem**: Internal services need caller context for fine-grained authorization decisions.

**Anti-pattern**: Reusing external access tokens internally (insecure due to token leakage risk).

#### Recommended Pattern: Signed Data Structure by Trusted Issuer

After edge authentication, generate data structure representing external entity identity (user ID, roles, permissions), signed or encrypted by trusted issuer and propagated to internal microservices.

**Implementation Recommendations**:
1. Decouple external access tokens from internal representation
2. Use single data structure to represent and propagate external entity identity
3. Sign internal entity representation structure (symmetric or asymmetric encryption)
4. Make internal structure extensible for additional claims
5. Never expose internal entity representation structure outside trusted boundary

### Service-to-Service Authentication

#### Mutual Transport Layer Security (mTLS)

Each microservice carries public/private key pair for authentication via mTLS. Provides:
- Legitimate service identification
- Confidentiality and integrity of transmitted data

**Challenges**: Key provisioning, trust bootstrap, certificate revocation, key rotation.

#### Token-Based Authentication

Token contains caller ID (microservice ID) and permissions (scopes). Process:
1. Caller microservice obtains signed token from security token service using service ID and password
2. Token attached to outgoing requests via HTTP headers
3. Called microservice extracts and validates token online or offline

**Online validation**: Network call to centralized service (detects revoked tokens, high latency, for critical requests)
**Offline validation**: Uses downloaded public key (may not detect revoked tokens, low latency, for non-critical requests)

### Logging Architecture

**Principles**:
- Each microservice writes log messages to local file using standard output
- Logging agent periodically pulls log messages and publishes to message broker
- Central logging service subscribes to message broker messages

**Key Requirements**:

1. **Local File Logging**: Microservices write to local files, not directly to central logging system
2. **Dedicated Logging Agent**: Decoupled component deployed on same host as microservice
3. **Asynchronous Pattern**: Message broker implements asynchronous connection between logging agent and central service
4. **Mutual Authentication**: Logging agent and message broker use mutual authentication (TLS)
5. **Access Control**: Message broker enforces access control policy with least privileges
6. **Data Sanitization**: Filter/sanitize log messages to exclude sensitive data (PII, passwords, API keys)
7. **Correlation ID**: Generate unique correlation ID for every call chain to group log messages
8. **Health Monitoring**: Logging agent provides health and status data
9. **Structured Format**: Publish log messages in structured format (JSON, CSV)
10. **Context Data**: Append platform context (hostname, container name) and runtime context (class name, filename)

### Security Architecture Documentation

Essential documentation to support threat modeling, attack surface analysis, and least privilege enforcement:

#### Service and Infrastructure Inventory
- Document all application services and infrastructure components with unique IDs, business functions, API definitions including security schemes (scopes, API keys), source repositories, and team ownership
- Include authentication, authorization, logging, monitoring, and discovery services
- Document data storages (databases, caches) and message queues with software types

#### Data Classification and Flow Mapping
- Identify and classify all data assets by protection level (PII, confidential, public)
- Map service-to-storage relationships with access types (read, read/write)
- Document service-to-service communications (synchronous HTTP/gRPC, asynchronous messaging) with data exchanged
- Track which assets are stored in which systems (golden source vs cache)

#### Architecture Visualization
- Create graphical representations using service call graphs or data flow diagrams
- Use tools like DOT language to visualize component relationships and trust boundaries
- Maintain current architecture diagrams showing all connections and data flows

#### Security Applications
This documentation enables:
- Attack surface enumeration from API definitions for focused security testing
- Data leakage analysis by tracking sensitive data movement across service boundaries  
- Least privilege implementation by defining minimal permissions based on documented interactions
- Trust boundary validation and justification of all service communications
- Centralized security control verification to avoid duplicate or missing protections

### Security Best Practices Summary

- Implement defense-in-depth authorization at multiple layers
- Use centralized policy management with embedded decision points
- Propagate signed internal identity tokens, never external tokens
- Choose mTLS for service authentication when possible, token-based for flexibility
- Implement resilient, secure logging with proper data sanitization
- Maintain comprehensive architecture documentation for threat modeling and security analysis
- Apply formal governance procedures for all security policy changes