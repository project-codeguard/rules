---
description: MCP (Model Context Protocol) Security based on CoSAI MCP Security guidelines
languages:
- python
- javascript
- typescript
- go
- rust
- java
alwaysApply: false
---

rule_id: codeguard-0-mcp-security

# MCP (Model Context Protocol) Security Guidelines

NEVER deploy MCP servers or clients without implementing proper security controls.

### Workload Identity and Authentication
- Use SPIFFE/SPIRE for cryptographic workload identities
  - SPIFFE (Secure Production Identity Framework For Everyone) provides a standard for service identity
  - SPIRE (SPIFFE Runtime Environment) issues and rotates short-lived cryptographic identities (SVIDs)

### Input and Data Sanitization
- Validate ALL inputs using allowlists at every trust boundary
- Sanitize file paths through canonicalization
- Use parameterized queries for database operations
- Apply context-aware output encoding (SQL, shell, HTML)
- Sanitize tool outputs: return only minimum fields, redact all PII and sensitive data
- Treat ALL inputs, tool schemas, metadata, prompts, and resource content as untrusted input
- Deploy prompt injection detection systems
- Use strict JSON schemas to maintain boundaries between instructions and data

### Sandboxing and Isolation
- Design MCP servers to execute with least privilege
- MCP servers interacting with host environment (files, commands, network) MUST implement sandboxing controls
- LLM-generated code MUST NOT run with full user privileges
- Implement additional sandboxing layers: gVisor, Kata Containers, SELinux sandboxes

### Cryptographic Verification of Resources
- Provide cryptographic signatures and SBOMs for all server code
- Implement signature verification in your MCP client before loading servers
- Use TLS for ALL data in transit
- Implement remote attestation capabilities to verify servers are running expected code

### Transport Layer Security

#### stdio Transport (Local Servers)
- STRONGLY RECOMMENDED for local MCP to eliminate DNS rebinding risks
- Direct pipe-based stream communication
- Implement sandbox to prevent privilege escalation

#### HTTP Streaming Transport (Remote Servers)
Required security controls to implement:
- Payload Limits (prevent large payload and recursive payload DoS)
- Rate limiting for tool calls and transport requests
- Client-Server Authentication/Authorization
- Mutual TLS Authentication
- TLS Encryption
- CORS Protection
- CSRF Protection
- Integrity Checks (prevent replay, spoofing, poisoned responses)

### Secure Tool and UX Design
- Create single-purpose tools with explicit boundaries; avoid "do anything" tools
- Do not rely on the LLM for validation or authorization decisions
- Use two-stage commit for high-impact actions: draft/preview first, explicit commit with confirmation second
- Provide rollback/undo paths (draft IDs, snapshots, reversible actions) and time-bound commits when possible

### Human-in-the-Loop
- Implement confirmation prompts for risky operations in your MCP server
- Use elicitation on MCP server side to request user confirmation of risky actions
- Security-relevant messages MUST clearly indicate implications
- Do NOT rely solely on human approval (users can become fatigued)

### Logging and Observability
- Implement logging in your MCP servers and clients
- Log: tools that were used, parameters, originating prompt
- Use OpenTelemetry for end-to-end linkability of actions
- Maintain immutable records of actions and authorizations

---

## Deployment Pattern Security

### All-Local (stdio or http)
- Security depends entirely on host system posture
- Use `stdio` transport to avoid DNS rebinding risks
- Use sandboxing to limit privilege escalation attacks
- Appropriate for development and personal use

### Single-Tenant Remote (http)
- Authentication between client and server is REQUIRED
- Use secure credential storage (OS keychains, secret managers)
- Communication MUST be authenticated and encrypted
- Enterprise clients should enforce authenticated server discovery with explicit allowlists

### Multi-Tenant Remote (http)
- Require robust tenant isolation, identity, and access control
- Implement strong multi-tenancy controls (per-tenant encryption, role-based access control)
- Prefer MCP servers hosted directly by service provider
- Provide remote attestation when possible
