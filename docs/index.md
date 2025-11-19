# Project CodeGuard: Security Rules for AI Coding Agents

[Project CodeGuard](https://github.com/project-codeguard/rules) is an open-source, model-agnostic security framework that embeds secure-by-default practices into AI coding agent workflows. It provides comprehensive security rules that guide AI assistants to generate more secure code automatically.

## Why Project CodeGuard?

AI coding agents are transforming software engineering, but this speed can introduce security vulnerabilities. Is your AI coding agent implementation introducing security vulnerabilities?

- Skipping input validation
- Hardcoding secrets and credentials
- Using weak cryptographic algorithms
- Relying on unsafe functions
- Missing authentication/authorization checks
- Missing any other security best practice

Project CodeGuard solves this by embedding security best practices directly into AI coding agent workflows. 

**Before, During, and After Code Generation.**

Project CodeGuard can be used **before**, **during** and **after** code generation. They can be used at the AI agent planning phase or for initial specification-driven engineering tasks. Project CodeGuard rules can also be used to prevent vulnerabilities from being introduced during code generation. They can also be used by automated code-review AI agents. 

For example, a rule focused on input validation could work at multiple stages: it might suggest secure input handling patterns during code generation, flag potentially unsafe user or AI agent input processing in real-time and then validate that proper sanitization and validation logic is present in the final code. Another rule targeting secret management could prevent hardcoded credentials from being generated, alert developers when sensitive data patterns are detected, and verify that secrets are properly externalized using secure configuration management. 

This multi-stage methodology ensures that security considerations are woven throughout the development process rather than being an afterthought, creating multiple layers of protection while maintaining the speed and productivity that make AI coding tools so valuable. 


## Security Coverage

Our rules cover essential security domains:

- **Cryptography**: Safe algorithms (including post-quantum cryptography), secure key management, certificate validation
- **Input Validation**: SQL injection prevention, XSS protection, command injection defense
- **Authentication**: MFA best practices, OAuth/OIDC, secure session management
- **Authorization**: RBAC/ABAC, access control, IDOR prevention
- **Supply Chain**: Dependency security, SBOM generation, vulnerability management
- **Cloud Security**: IaC hardening, container security, Kubernetes best practices
- **Platform Security**: Mobile apps, web services, API security
- **Data Protection**: Privacy, encryption at rest/transit, secure storage

## Quick Start

Get started in minutes:

1. **Download the rules** from our [releases page](https://github.com/project-codeguard/rules/releases)
2. **Copy to your project** - Place IDE-specific rules in your repository
3. **Start coding** - AI assistants will automatically follow security best practices

[Get Started →](getting-started.md){ .md-button .md-button--primary }
[View on GitHub :material-github:](https://github.com/project-codeguard/rules){ .md-button }

## How It Works

1. **Security rules** are written in a unified markdown format
2. **Conversion tools** translate rules to IDE-specific formats
3. **AI assistants** reference these rules when generating or reviewing code
4. **Secure code** is produced automatically without developer intervention

## Community

- **📋 Issues**: [Report bugs or request features](https://github.com/project-codeguard/rules/issues)
- **💬 Discussions**: [Join the conversation](https://github.com/project-codeguard/rules/discussions)
- **🤝 Contributing**: [Learn how to contribute](https://github.com/project-codeguard/rules/blob/main/CONTRIBUTING.md)

## Note

This is a strategic move by Cisco to raise the security posture of the entire ecosystem—not just Cisco itself. The health of the broader software community impacts everyone's products, and by sharing this information, we fortify the entire chain. The goal is to create a more secure environment for everyone.
