# Getting Started

Get up and running with Project CodeGuard in just a few steps.

## Prerequisites

Before you begin, familiarize yourself with how rules work in your IDE:

=== "Cursor"

    Cursor uses `.cursor/rules` for rule configuration.
    
    :material-book-open-page-variant: [Cursor Rules Documentation](https://docs.cursor.com/en/context/rules)

=== "Windsurf"

    Windsurf uses `.windsurf/rules` for rule configuration.
    
    :material-book-open-page-variant: [Windsurf Rules Documentation](https://docs.windsurf.com/windsurf/cascade/memories#rules)

=== "GitHub Copilot"

    GitHub Copilot uses `.github/instructions` for rule configuration.
    
    :material-book-open-page-variant: [GitHub Copilot Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)

## Installation

### Option 1: Download Pre-built Rules (Recommended)

1. **Download**: Visit the [Releases page](https://github.com/project-codeguard/rules/releases) and download the latest release archive
2. **Extract**: Unzip the downloaded file
3. **Install**: Copy the relevant IDE-specific rules to your project root:
    - For **Cursor**: Copy `.cursor/` directory
    - For **Windsurf**: Copy `.windsurf/` directory
    - For **GitHub Copilot**: Copy `.github/instructions/` directory

!!! tip "Repository Level Installation"
    Installing at the repository level ensures all team members benefit from the security rules automatically when they clone the repository.

!!! note "Hidden Files on macOS/Linux"
    On macOS/Linux, you may need to show hidden files:
    
    - **macOS Finder**: Press ++cmd+shift+period++ to toggle visibility
    - **Linux**: Use `ls -la` in terminal or enable "Show Hidden Files" in your file manager

### Option 2: Build from Source

If you want to customize or contribute to the rules, the source markdown lives under `sources/`:

```
sources/
├── core/        # Project CodeGuard rules
└── owasp/       # OWASP-derived rule pack
```

Convert everything and create IDE bundles locally:

```bash
# Clone the repository
git clone https://github.com/project-codeguard/rules.git
cd rules

# Install dependencies (requires Python 3.11+)
uv sync

# Convert unified rules to IDE-specific formats (sources/ → dist/rules/)
uv run python src/convert_to_ide_formats.py
# Add --source owasp (or any directory under sources/) to include extra packs

# Copy the generated rules to your project
cp -r ./dist/rules/.cursor/ /path/to/your/project/
cp -r ./dist/rules/.windsurf/ /path/to/your/project/
cp -r ./dist/rules/.github/ /path/to/your/project/
```

## Verify Installation

After installation, your project structure should include:

```
your-project/
├── .cursor/
│   └── rules/
├── .windsurf/
│   └── rules/
├── .github/
│   └── instructions/
└── ... (your project files)
```

## What's Included

The security rules cover essential areas:

### Core Security Rules

- **🔐 Cryptography**: Safe algorithms, secure key management, TLS configuration
- **🛡️ Input Validation**: SQL injection, XSS prevention, command injection defense
- **🔑 Authentication**: MFA, OAuth/OIDC, password security, session management
- **⚡ Authorization**: RBAC/ABAC, access control, privilege escalation prevention

### Platform-Specific Rules

- **📱 Mobile Apps**: iOS/Android security, secure storage, transport security
- **🌐 API Security**: REST/GraphQL/SOAP security, rate limiting, SSRF prevention
- **☁️ Cloud & Containers**: Docker/Kubernetes hardening, IaC security
- **🗄️ Data Storage**: Database security, encryption, backup protection

### DevOps & Supply Chain

- **📦 Dependencies**: Supply chain security, SBOM, vulnerability management
- **🔄 CI/CD**: Pipeline security, artifact signing, secrets management
- **📝 Logging**: Secure logging, monitoring, privacy-aware telemetry

## Testing the Integration

To verify the rules are working:

1. **Open your IDE** with the Project CodeGuard rules installed
2. **Start a new file** in a supported language (Python, JavaScript, Java, C/C++, etc.)
3. **Ask your AI assistant** to generate code that might have security implications:
   - "Create a function to hash a password"
   - "Write code to connect to a database"
   - "Generate an API endpoint with authentication"

4. **Observe the output** - The AI should automatically apply security best practices:
   - Using strong cryptographic algorithms (bcrypt/Argon2 for passwords)
   - Parameterized queries to prevent SQL injection
   - Proper authentication/authorization checks

## Next Steps

- **Review Rules**: Explore the security rules in your IDE's rules directory
- **Test Integration**: Generate some code and see the security guidance in action
- **Share Feedback**: Help us improve by [opening an issue](https://github.com/project-codeguard/rules/issues)
- **Contribute**: See [CONTRIBUTING.md](https://github.com/project-codeguard/rules/CONTRIBUTING.md) to contribute new rules or improvements

!!! success "You're Ready!"
    Project CodeGuard is now protecting your development workflow. The security rules will automatically guide AI assistants to generate more secure code.

## Troubleshooting

### Rules Not Working

If the AI assistant doesn't seem to follow the rules:

1. **Restart your IDE** to ensure rules are loaded
2. **Check file location** - Ensure rules are in the correct directory for your IDE
3. **Verify file format** - Rules should be markdown files
4. **Test with explicit request** - Ask the AI directly: "Follow the security rules when generating this code"

### Performance Impact

The rules have minimal performance impact, but if you experience issues:

- **Reduce rule count**: Start with core rules (cryptography, input validation, authentication)
- **Combine rules**: Merge related rules into fewer files
- **Report issues**: Let us know via [GitHub Issues](https://github.com/project-codeguard/rules/issues)

## Getting Help

- **Documentation**: You're reading it! Check the [FAQ](faq.md) for common questions
- **GitHub Issues**: [Report bugs or ask questions](https://github.com/project-codeguard/rules/issues)
- **Discussions**: [Join the community discussion](https://github.com/project-codeguard/rules/discussions)
