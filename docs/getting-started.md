# Getting Started

Get up and running with Project CodeGuard in just a few steps.

## Project CodeGuard Introduction Video
[This video](https://www.youtube.com/watch?v=O03MDxUWjsE) introduces Project CodeGuard and includes several demos on how to use it during code generation and code review with Claude Code, Codex, and other coding agents.

<div style="position: relative; width: 100%; padding-bottom: 56.25%; margin: 2em 0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);">
  <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" src="https://www.youtube.com/embed/O03MDxUWjsE" title="Project CodeGuard Introduction Video and Demos" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

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

=== "Antigravity"
    Antigravity uses `.agent/rules` for rule configuration.

    :material-book-open-page-variant: [Antigravity Instructions](https://codelabs.developers.google.com/getting-started-google-antigravity#8)

## Installation

### Option 1: Download Pre-built Rules (Recommended)

1. **Download**: Visit the [Releases page](https://github.com/project-codeguard/rules/releases) and download the IDE-specific ZIP file:
    - `ide-rules-all.zip` - All IDE formats (recommended for teams using multiple tools)
    - `ide-rules-cursor.zip` - Cursor only
    - `ide-rules-windsurf.zip` - Windsurf only
    - `ide-rules-copilot.zip` - GitHub Copilot only
    - `ide-rules-antigravity.zip` - Antigravity only
2. **Extract**: Unzip the downloaded file
3. **Install**: Copy the relevant IDE-specific rules to your project root:
    - For **Cursor**: Copy `.cursor/` directory to your project
    - For **Windsurf**: Copy `.windsurf/` directory to your project
    - For **GitHub Copilot**: Copy `.github/` directory to your project
    - For **Antigravity**: Copy `.agent/` directory to your project


!!! tip "Repository Level Installation"
    Installing at the repository level ensures all team members benefit from the security rules automatically when they clone the repository.

!!! note "Hidden Files on macOS/Linux"
    On macOS/Linux, you may need to show hidden files:
    
    - **macOS Finder**: Press ++cmd+shift+period++ to toggle visibility
    - **Linux**: Use `ls -la` in terminal or enable "Show Hidden Files" in your file manager

### Claude Code Plugin

Claude Code uses a plugin system instead of manual file installation:

```bash
# Add the Project CodeGuard marketplace
/plugin marketplace add project-codeguard/rules

# Install the security plugin
/plugin install codeguard-security@project-codeguard
```

The plugin will be automatically loaded and apply security rules to your code. See the [Claude Code Plugin documentation](claude-code-skill-plugin.md) for more details.

### OpenAI Codex Skills

OpenAI Codex uses [agent skills](https://agentskills.io/) to extend capabilities with task-specific instructions. 

!!! warning "Prerequisites"
    Make sure you're running the latest version of Codex before installing skills.

To install Project CodeGuard as a Codex skill, open Codex and use the built-in skill installer:

```
$skill-installer install from https://github.com/project-codeguard/rules/tree/main/skills/software-security
```

Alternatively, you can manually clone the skill to your project:

```bash
# Clone to your project's .codex/skills directory
mkdir -p .codex/skills
cd .codex/skills
git clone https://github.com/project-codeguard/rules.git temp
mv temp/skills/software-security ./
rm -rf temp

# Restart Codex to load the new skill
```

Once installed, you can invoke the skill explicitly in your prompts using `$software-security` or Codex will automatically use it when you're trying to write, review, or modify code.

!!! info "Codex Skills Documentation"
    For more information about Codex skills, skill locations, and configuration, see the [OpenAI Codex Skills documentation](https://developers.openai.com/codex/skills/).

### Option 2: Build from Source

If you want to customize or contribute to the rules:

```bash
# Clone the repository
git clone https://github.com/project-codeguard/rules.git
cd rules

# Install dependencies (requires Python 3.11+)
uv sync

# Validate rules
uv run python src/validate_unified_rules.py sources/

# Convert rules (default: core rules only)
uv run python src/convert_to_ide_formats.py

# Or include all rules (core + owasp supplementary)
uv run python src/convert_to_ide_formats.py --source core owasp

# Copy the generated rules to your project
cp -r dist/.cursor/ /path/to/your/project/
cp -r dist/.windsurf/ /path/to/your/project/
cp -r dist/.github/ /path/to/your/project/
cp -r dist/.agent/ /path/to/your/project/
```

## Verify Installation

After installation, your project structure should include:

```
your-project/
├── .agent/
│   └── rules/
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
- **Contribute**: See [CONTRIBUTING.md](https://github.com/project-codeguard/rules/blob/main/CONTRIBUTING.md) to contribute new rules or improvements

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

