# Project CodeGuard: Security Rules for AI Coding Agents

[Project CodeGuard](https://project-codeguard.org) is an open-source, model-agnostic security framework that embeds secure-by-default practices into AI coding agent workflows. It provides comprehensive security rules that guide AI assistants to generate more secure code automatically.

## Why Project CodeGuard?

AI coding agents are transforming software engineering, but this speed can introduce security vulnerabilities. Is your AI coding agent implementation introducing security vulnerabilities?

- ❌ Skipping input validation
- ❌ Hardcoding secrets and credentials
- ❌ Using weak cryptographic algorithms
- ❌ Relying on unsafe functions
- ❌ Missing authentication/authorization checks
- ❌ Missing any other security best practice

Project CodeGuard solves this by embedding security best practices directly into AI coding agent workflows. 

**During and After Code Generation.**

These rules can be used for: 
- preventing vulnerabilities from being introduced during code generation
- automated code review by AI agents


## Security Coverage

Our rules cover essential security domains:

- **🔐 Cryptography**: Safe algorithms (including post-quantum cryptography), secure key management, certificate validation
- **🛡️ Input Validation**: SQL injection prevention, XSS protection, command injection defense
- **🔑 Authentication**: MFA best practices, OAuth/OIDC, secure session management
- **⚡ Authorization**: RBAC/ABAC, access control, IDOR prevention
- **📦 Supply Chain**: Dependency security, SBOM generation, vulnerability management
- **☁️ Cloud Security**: IaC hardening, container security, Kubernetes best practices
- **📱 Platform Security**: Mobile apps, web services, API security
- **🔍 Data Protection**: Privacy, encryption at rest/transit, secure storage

## Quick Start

Get started in minutes:

1. **Download the rules** from our [releases page](https://github.com/project-codeguard/rules/releases)
2. **Copy to your project** - Place AI agent and IDE specific rules in your repository
3. **Start coding** - AI assistants will automatically follow security best practices

- Additional details in the [Get Started →](getting-started.md)


## How It Works

1. **Security rules** are written in a unified markdown format
2. **Conversion tools** translate rules to IDE and AI agent formats
3. **AI assistants** reference these rules when generating or reviewing code
4. **Secure code** is produced automatically without developer intervention

## Repository Layout

```
sources/
├── core/        # Project CodeGuard rule set
└── owasp/       # OWASP-derived rule pack

dist/rules/      # Generated IDE bundles (created by the converter)
src/             # Conversion and validation tools
```

Run `uv run python src/convert_to_ide_formats.py` to build the IDE bundles
before packaging a release. The default run converts the core pack; append
`--source owasp` (or any directory under `sources/`) to include additional packs.

## Maintainer Release Checklist

1. Bump `[project].version` in `pyproject.toml` to the new `major.minor.patch` on a feature branch.
2. Open a pull request into `dev`; once approved, merge the version bump into `dev`.
3. Create a short-lived release branch from `dev`, run final checks, and merge that branch into `main`.
4. Tag the merge commit on `main` (`git tag vX.Y.Z && git push origin vX.Y.Z`) and publish a GitHub Release from that tag. The `Build IDE Bundles` workflow runs automatically, attaches `dist/ide-rules.zip` to the release, and uploads the same file as a workflow artifact.

## Community

- **📋 Issues**: [Report bugs or request features](https://github.com/project-codeguard/rules/issues)
- **💬 Discussions**: [Join the conversation](https://github.com/project-codeguard/rules/discussions)
- **🤝 Contributing**: [Learn how to contribute](https://github.com/project-codeguard/rules/blob/main/CONTRIBUTING.md)

Copyright © 2025 Cisco Systems, Inc. Licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
