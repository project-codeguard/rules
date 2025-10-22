---
description: Threat Modeling Security
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
- swift
- typescript
alwaysApply: false
---

## Threat Modeling Security

Structured process to identify, analyze, and mitigate security threats early in the development lifecycle through systematic security analysis.

### Threat Modeling Process

The threat modeling process answers four key questions:
1. What are we working on?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good enough job?

### System Modeling (What are we working on?)

Create visual representations of your system to understand attack surfaces and security boundaries.

Data Flow Diagrams (DFDs):
- Model system interactions with data and external entities
- Identify trust boundaries, data flows, data stores, and processes
- Use tools like OWASP Threat Dragon, Microsoft Threat Modeling Tool, or draw.io
- Create multiple DFDs for complex systems (high-level overview plus detailed sub-systems)
- Store DFDs in accessible format for updates and reference

Key elements to capture:
- External entities interacting with the system
- Data flows between components
- Data storage locations
- Process boundaries and trust zones
- Authentication and authorization points

Alternative approaches:
- Brainstorming sessions for domain discovery
- Collaborative definition of key terms and concepts
- Quick identification of business processes and dependencies

### Threat Identification (What can go wrong?)

Use STRIDE methodology to systematically identify threats within your system context.

STRIDE Categories:

| Threat Category | Violates | Examples |
|-----------------|----------|----------|
| Spoofing | Authenticity | Attacker steals authentication token to impersonate user |
| Tampering | Integrity | Attacker abuses application to perform unintended database updates |
| Repudiation | Non-repudiability | Attacker manipulates logs to cover their actions |
| Information Disclosure | Confidentiality | Attacker extracts data from database containing user account info |
| Denial of Service | Availability | Attacker locks legitimate user out by failed authentication attempts |
| Elevation of Privileges | Authorization | Attacker tampers with JWT to change their role |

Threat identification techniques:
- Systematic review of each STRIDE category for system components
- Brainstorming sessions with development and security teams
- Integration with tactical approaches like kill chains or MITRE ATT&CK
- Use of threat modeling tools for structured analysis

Threat prioritization:
- Assess likelihood and impact of identified threats
- Consider cost and effort required for mitigation
- Focus on threats with highest risk-to-effort ratio

### Response and Mitigations (What are we going to do about it?)

Define responses for each identified threat using these strategies:

Response Options:
- Mitigate: Reduce likelihood that threat will materialize
- Eliminate: Remove feature or component causing the threat
- Transfer: Shift responsibility to another entity
- Accept: Acknowledge risk but take no action due to business constraints

Mitigation requirements:
- Develop actionable mitigation strategies that can be implemented
- Document mitigations as testable requirements
- Reference standards like OWASP ASVS and MITRE CWE for guidance
- Apply mitigations at category or individual threat level
- Ensure mitigations are built into the system, not theoretical

### Review and Validation (Did we do a good enough job?)

Validate threat model completeness and effectiveness through stakeholder review.

Review criteria:
- Does the model accurately reflect the actual system?
- Have all applicable threats been identified?
- Has a response strategy been defined for each threat?
- Do mitigation strategies reduce risk to acceptable levels?
- Is the threat model formally documented and accessible?
- Can mitigations be tested and measured for effectiveness?

Review participants:
- Development teams
- Security teams
- Architecture teams
- Product stakeholders
- Operations teams

### Integration with Development Process

Integrate threat modeling seamlessly into SDLC:
- Perform initial threat modeling during design phase
- Update threat models when system architecture changes
- Include threat modeling in feature development workflows
- Treat as standard development step, not optional add-on
- Maintain and refine models alongside system evolution

Development team considerations:
- Provide security training for developers
- Include security experts in threat modeling sessions
- Use tools that simplify and automate threat identification
- Promote security culture within development organization
- Establish cross-team collaboration and communication

Tools and techniques:
- OWASP Threat Dragon for collaborative threat modeling
- Microsoft Threat Modeling Tool for structured analysis
- OWASP pytm for threat-modeling-as-code approach
- draw.io with threat modeling libraries for diagramming
- STRIDE, PASTA, LINDDUN, OCTAVE, and VAST methodologies

### Implementation Guidelines

1. Start threat modeling early in design phase and integrate into SDLC
2. Create comprehensive Data Flow Diagrams showing trust boundaries and data flows
3. Apply STRIDE methodology systematically to identify threats
4. Prioritize threats based on likelihood, impact, and mitigation cost
5. Develop actionable, testable mitigation requirements
6. Involve security experts and cross-functional stakeholders in reviews
7. Document threat models and store artifacts accessibly
8. Update threat models when system architecture or features change
9. Use appropriate tools to support and streamline the process
10. Foster security awareness and collaboration across development teams