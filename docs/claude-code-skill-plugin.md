# CodeGuard Claude Code Plugin

## Overview

This document explains how Project CodeGuard is packaged as a Claude Code plugin (Agent Skill) and how to use it effectively in your AI-assisted coding workflows.

Project CodeGuard is an **open-source, model-agnostic security framework** that embeds secure-by-default practices into AI coding workflows. The plugin makes it easy to integrate these security rules with Claude Code.

## What is an Agent Skill?

Agent Skills are model-invoked capabilities that Claude autonomously uses based on task context. The CodeGuard security skill provides comprehensive security guidance that Claude applies automatically when writing, reviewing, or modifying code.

## Installation

### Prerequisites

- Claude Code installed
- Basic familiarity with Claude Code's plugin system

### Installation Steps

1. **Add the Project CodeGuard marketplace:**
   ```bash
   /plugin marketplace add project-codeguard/rules
   ```

2. **Install the security plugin:**
   ```bash
   /plugin install codeguard-security@project-codeguard
   ```

3. **Restart Claude Code** (if prompted)

4. **Verify installation:**
   The skill is automatically loaded. Start coding and Claude will apply security rules automatically.

## How It Works

The CodeGuard skill integrates **22 security rule files** covering all major security domains across languages, frameworks, and technology stacks. The skill follows a simple but powerful workflow:

### Skill Activation

The skill activates automatically when:
- Writing new code in any language
- Reviewing or modifying existing code
- Implementing security-sensitive features (authentication, cryptography, data handling)
- Working with user input, databases, APIs, or external services
- Configuring cloud infrastructure, CI/CD pipelines, or containers
- Handling sensitive data, credentials, or cryptographic operations

### Security Workflow

When generating or reviewing code, Claude follows this 3-step workflow:

**1. Initial Security Check**
- Will this handle credentials? → Apply `codeguard-1-hardcoded-credentials`
- What language is being used? → Identify applicable language-specific rules
- What security domains are involved? → Load relevant rule files

**2. Code Generation**
- Apply secure-by-default patterns from relevant CodeGuard rules
- Add security-relevant comments explaining choices

**3. Security Review**
- Review against implementation checklists in each rule
- Verify no hardcoded credentials or secrets
- Validate that all applicable rules have been followed
- Explain which security rules were applied
- Highlight security features implemented

### Rule Categories

**Always-Apply Rules** (3 critical rules checked on every code operation):
- `codeguard-1-hardcoded-credentials` - Never hardcode secrets or credentials
- `codeguard-1-crypto-algorithms` - Use modern cryptographic algorithms
- `codeguard-1-digital-certificates` - Validate certificate security

**Context-Specific Rules** (19 rules applied based on technology and features):
- Input validation, authentication, authorization, APIs, data storage, privacy, logging, cryptography, file handling, serialization, supply chain, DevOps, cloud, Kubernetes, IaC, frameworks, mobile security, and memory safety (C/C++)

## Usage Examples

### Example 1: Writing Database Code

```python
# Claude will automatically use parameterized queries
def get_user(email):
    # Secure pattern following codeguard-0-input-validation-injection
    query = "SELECT * FROM users WHERE email = ?"
    return cursor.execute(query, (email,))
```

### Example 2: Handling API Keys

```javascript
// Claude will prevent hardcoded credentials
// and suggest environment variables
const apiKey = process.env.STRIPE_API_KEY;
if (!apiKey) {
  throw new Error("STRIPE_API_KEY not configured");
}
```

### Example 3: Password Hashing

```python
# Claude will suggest modern password hashing
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)
```

### Example 4: File Upload Security

```javascript
// Claude will enforce file validation
const multer = require('multer');
const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    // Validate file type by content, not just extension
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only images allowed'));
    }
  }
});
```

## Team Deployment

For organizations, deploy CodeGuard to all developers automatically:

1. Add to your project's `.claude/settings.json`:
   ```json
   {
     "marketplaces": [{"source": "project-codeguard/rules"}],
     "plugins": [
       {
         "name": "codeguard-security",
         "marketplace": "project-codeguard",
         "enabled": true
       }
     ]
   }
   ```

2. Team members trust the repository folder

3. CodeGuard installs automatically for everyone

## All Security Rules

The plugin includes 22 comprehensive security rules organized into two categories:

### Always-Apply Rules (3 rules)

These critical rules are checked on **every** code operation:

| Rule | Description |
|------|-------------|
| `codeguard-1-hardcoded-credentials` | Prevent secrets, passwords, API keys, tokens in source code |
| `codeguard-1-crypto-algorithms` | Ban weak algorithms (MD5, SHA-1, DES); use modern alternatives |
| `codeguard-1-digital-certificates` | Validate certificate expiration, key strength, signature algorithms |

### Context-Specific Rules (19 rules)

These rules apply based on the programming language, framework, or feature being implemented. Claude automatically selects relevant rules based on context:

| Security Domain | Rules |
|-----------------|-------|
| **Input & Injection** | `codeguard-0-input-validation-injection` |
| **Authentication** | `codeguard-0-authentication-mfa` |
| **Authorization** | `codeguard-0-authorization-access-control` |
| **Sessions** | `codeguard-0-session-management-and-cookies` |
| **APIs & Web** | `codeguard-0-api-web-services`, `codeguard-0-client-side-web-security` |
| **Data & Privacy** | `codeguard-0-data-storage`, `codeguard-0-privacy-data-protection`, `codeguard-0-logging` |
| **Cryptography** | `codeguard-0-additional-cryptography` |
| **Files & Serialization** | `codeguard-0-file-handling-and-uploads`, `codeguard-0-xml-and-serialization` |
| **Infrastructure** | `codeguard-0-supply-chain-security`, `codeguard-0-devops-ci-cd-containers`, `codeguard-0-cloud-orchestration-kubernetes`, `codeguard-0-iac-security` |
| **Platforms** | `codeguard-0-framework-and-languages`, `codeguard-0-mobile-apps` |
| **Memory Safety (C/C++)** | `codeguard-0-safe-c-functions` |

> **Note:** Each rule file contains detailed guidance, checklists, and examples. Claude references these automatically based on the code context.

## Updating

To update to the latest security rules:

```bash
/plugin update codeguard-security@project-codeguard
```

## Customization

### Disabling the Plugin

If needed, temporarily disable:

```bash
/plugin disable codeguard-security@project-codeguard
```

Re-enable:

```bash
/plugin enable codeguard-security@project-codeguard
```

### Using Specific Rule Files

All rule files are available in the `skills/software-security/rules/` directory within the plugin. You can reference specific rules in prompts:

```
Claude, please review this authentication code against the 
codeguard-0-authentication-mfa.md guidelines
```

### Creating Custom Workflows

You can create custom security review workflows:

```
Claude, perform the following security checks on this code:
1. Check for hardcoded credentials
2. Validate input sanitization
3. Verify authentication implementation
4. Review authorization logic
Use the relevant CodeGuard rules for each check.
```

## Troubleshooting

### Plugin Not Loading

1. Verify installation: `/plugin` → "Manage Plugins"
2. Check that `codeguard-security` is listed and enabled
3. Restart Claude Code

### Rules Not Being Applied

1. Confirm the plugin is enabled
2. Try explicitly mentioning security in your prompt
3. Check that you're working with supported languages

### Checking Plugin Version

```bash
/plugin list
```

Look for `codeguard-security@project-codeguard` and note the version number.

## Best Practices

### During Development

1. **Trust the automation**: Let Claude apply security rules automatically
2. **Learn from suggestions**: When Claude suggests secure alternatives, understand why
3. **Ask for explanations**: Request Claude to explain security recommendations
4. **Use proactive security**: Ask Claude for security guidance before implementing features

### During Code Review

1. **Explicit security review**: Ask Claude to perform comprehensive security analysis
2. **Reference specific rules**: Mention rule names for focused review (e.g., "Review against codeguard-0-authentication-mfa")
3. **Check always-apply rules**: Ensure credentials, crypto algorithms, certificates, and C functions are handled securely
4. **Validate workflow**: Confirm that Claude followed the 3-step security workflow

### For Teams

1. **Standardize installation**: Use `.claude/settings.json` for consistent setup across the team
2. **Version control**: Track which plugin version your team uses
3. **Update regularly**: Keep rules current with latest security guidance
4. **Share learnings**: Document security patterns specific to your stack
5. **Train developers**: Ensure team members understand how to work with AI-assisted security

## Building the Plugin

If you're contributing to Project CodeGuard or need to rebuild the plugin:

```bash
cd /path/to/project-codeguard/rules

# Regenerate the Claude Code plugin (always uses core rules only)
uv run python src/convert_to_ide_formats.py
```

This command:
- Converts unified rules from `sources/` to IDE-specific formats
- Generates `skills/` directory with the 22 core security rules (Claude Code plugin)
- Creates `dist/` with IDE-specific formats (Cursor, Windsurf, Copilot, Antigravity)

**Note:** The Claude Code plugin (`skills/`) always contains only the 22 curated core rules. To build bundles with OWASP supplementary rules for other IDEs, use `--source core owasp`, but this only affects `dist/`, not `skills/`.

## Advanced Usage

### Language-Specific Security Reviews

Request focused reviews for specific languages:

```
Claude, perform a security review of this Python code with emphasis on:
- SQL injection prevention
- Input validation
- Authentication best practices
```

### Feature-Specific Guidance

Get proactive security guidance when building features:

```
Claude, I'm about to implement a file upload feature. 
What security considerations should I keep in mind 
according to CodeGuard rules?
```

### Security-First Development

Use CodeGuard from the planning phase:

```
Claude, help me design a secure authentication system for a web app.
Use CodeGuard rules to guide the architecture.
```

## Plugin Architecture

### File Structure

```
project-codeguard/rules/
├── .claude-plugin/
│   ├── plugin.json                  # Plugin metadata
│   └── marketplace.json             # Marketplace catalog
│
├── sources/                         # Source rules (version controlled)
│   ├── core/                        # Core security rules
│   └── owasp/                       # OWASP supplementary rules
│
├── skills/                          # Claude Code plugin (version controlled)
│   └── software-security/
│       ├── SKILL.md                 # Generated skill file
│       └── rules/                   # Generated rule files
│
├── dist/                            # Release artifacts (not in git)
│   ├── .cursor/                     # Cursor IDE format
│   ├── .windsurf/                   # Windsurf IDE format
│   └── .github/                     # Copilot format
│
└── src/
    └── convert_to_ide_formats.py    # Conversion script
```

### How Claude Uses the Skill

When you write or review code, Claude follows this workflow:

1. **Reads SKILL.md** - Understands when to activate the skill and what workflow to follow
2. **Initial Security Check** - Identifies which rules apply based on:
   - Whether credentials are involved (always-apply rule)
   - The programming language in use
   - The security domains involved (auth, crypto, APIs, etc.)
3. **Applies Security Rules** - References relevant rule files to:
   - Use secure-by-default patterns
   - Follow implementation checklists
   - Apply language-specific guidance
4. **Generates Secure Code** - Produces code that:
   - Never hardcodes credentials
   - Uses modern cryptographic algorithms
   - Implements input validation
   - Follows security best practices
5. **Provides Explanations** - Documents which security rules were applied and highlights security features implemented

## Contributing

Found an issue with the plugin or want to improve it?

1. **Report issues**: [GitHub Issues](https://github.com/project-codeguard/rules/issues)
2. **Suggest rules**: [GitHub Discussions](https://github.com/project-codeguard/rules/discussions)
3. **Contribute**: [Contributing Guide](https://github.com/project-codeguard/rules/blob/main/CONTRIBUTING.md)

## Version History

### Version 1.0.1
- Changed `codeguard-1-safe-c-functions` from always-apply to `codeguard-0-safe-c-functions` context-specific rule (C/C++ only)
- Updated rule counts: 3 always-apply rules, 19 context-specific rules
- Fixed GitHub Copilot instructions to use `description` field instead of `title`

### Version 1.0.0
- Initial release
- 22 comprehensive security rules
- 4 always-apply rules
- 18 context-specific rules
- Support for all major programming languages
- Complete technology stack coverage

## Resources

- **Project Website**: [https://project-codeguard.org](https://project-codeguard.org)
- **GitHub Repository**: [https://github.com/project-codeguard/rules](https://github.com/project-codeguard/rules)
- **Documentation**: [https://project-codeguard.org/getting-started/](https://project-codeguard.org/getting-started/)
- **Issue Tracker**: [https://github.com/project-codeguard/rules/issues](https://github.com/project-codeguard/rules/issues)

## License

- **Rules**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Tools**: Apache License 2.0

## Support

Need help? We're here for you:

1. **Documentation**: Start with [Getting Started Guide](https://project-codeguard.org/getting-started/)
2. **Community**: Join [GitHub Discussions](https://github.com/project-codeguard/rules/discussions)
3. **Issues**: Report bugs via [GitHub Issues](https://github.com/project-codeguard/rules/issues)


