---
description: NPM Security Best Practices
languages:
- javascript
alwaysApply: false
version: 0.1.0
severity: medium
---

## NPM Security Guidelines

Essential security practices for managing NPM packages and dependencies in JavaScript projects.

### Prevent Secret Leakage

Avoid publishing sensitive data to the npm registry:
- Use the `files` property in package.json as an allowlist to control what gets published
- Be cautious with `.gitignore` and `.npmignore` - if both exist, `.npmignore` takes precedence
- Run `npm publish --dry-run` to review the tarball contents before actual publishing
- NPM automatically revokes tokens detected in published packages, but prevention is better

### Enforce Deterministic Builds

Ensure consistent dependency installation across environments:
- Use `npm ci` instead of `npm install` in CI/CD and production builds
- Use `yarn install --frozen-lockfile` if using Yarn
- Never commit changes to package.json without updating the corresponding lockfile
- Lockfile inconsistencies can pull unintended package versions and compromise security

### Minimize Script Execution Risks

Reduce attack surface from package installation scripts:
- Add `--ignore-scripts` when installing packages: `npm install --ignore-scripts`
- Consider adding `ignore-scripts=true` to your `.npmrc` configuration
- Always vet third-party packages for credibility before installation
- Avoid immediate upgrades to new versions; allow time for community review
- Review changelog and release notes before upgrading dependencies

### Monitor Package Health

Regularly assess the state of your dependencies:
- Use `npm outdated` to identify packages that need updates
- Run `npm doctor` to verify healthy npm installation and environment
- Monitor for known vulnerabilities in dependencies using `npm audit`
- Scan for security vulnerabilities in third-party open source projects
- Set up monitoring for new CVEs that impact your project dependencies

### Use Private Registry Solutions

Consider using local npm proxies for enhanced control:
- Verdaccio provides a lightweight private registry solution
- Private registries offer package access control and authenticated users
- Proxy capabilities reduce duplicate downloads and save bandwidth
- Enable routing dependencies to different registries for security control
- Useful for testing environments and mono-repo projects

### Enable Account Security

Protect your npm publishing capabilities:
- Enable two-factor authentication with `npm profile enable-2fa auth-and-writes`
- Use auth-and-writes mode for comprehensive protection of profile, login, and package management
- Auth-only mode provides protection for login and profile changes only
- Use authentication apps like Google Authenticator for 2FA tokens

### Manage Access Tokens Securely

Control programmatic access to npm registry:
- Create tokens with minimal required permissions using `npm token create`
- Use read-only tokens when write access is not needed
- Restrict tokens to specific IP ranges with `--cidr` option
- Regularly audit tokens with `npm token list`
- Revoke unused or compromised tokens immediately with `npm token revoke`
- Never expose tokens in source code, logs, or environment variables

### Defend Against Typosquatting

Protect against malicious package substitution:
- Verify package names and metadata with `npm info <package>` before installation
- Be extra careful when copy-pasting installation commands from untrusted sources
- Check source code repositories and npm registry to confirm package legitimacy
- Default to being logged out of npm during daily development work
- Use `--ignore-scripts` when installing packages from unknown sources

### Follow Responsible Disclosure

Handle security vulnerabilities appropriately:
- Follow responsible disclosure programs when reporting vulnerabilities
- Coordinate with package maintainers before public disclosure
- Allow time for fixes and upgrade paths before publicizing security issues
- Use proper channels to report security concerns to package authors

### Package Naming Best Practices

Understand npm naming rules and security implications:
- Package names limited to 214 characters, lowercase only
- Cannot start with dot, underscore, or contain special characters like "~\'!()*"
- Be aware that typosquatting attacks target popular package names
- NPM uses spam detection mechanisms for new package publications
- Reserved names include node_modules and favicon.ico