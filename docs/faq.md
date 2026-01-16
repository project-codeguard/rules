# Frequently Asked Questions

## Purpose Statement

This FAQ document provides clear, concise answers to help developers seamlessly integrate Project CodeGuard security rules into AI-assisted coding workflows. Our goal is to ensure AI-generated code adheres to secure development practices without disrupting productivity.

---

## Q: Where can I access the rules?

**A:** You can access the rules in the [Project CodeGuard GitHub repository](https://github.com/project-codeguard/rules). The latest stable release is available on the [releases page](https://github.com/project-codeguard/rules/releases).

---

## Q: How can I use the rules in Windsurf, Cursor, or GitHub Copilot?

**A:** Detailed installation instructions are available in our [Getting Started guide](getting-started.md). In summary:

1. Download the latest release from the [releases page](https://github.com/project-codeguard/rules/releases)
2. Extract the archive and copy the IDE-specific rules to your project:
   - **Cursor**: Copy `.cursor/` directory to your project root
   - **Windsurf**: Copy `.windsurf/` directory to your project root
   - **GitHub Copilot**: Copy `.github/instructions/` directory to your project root
3. Restart your IDE and start coding - the AI assistant will automatically follow the security rules

---
## Q: Will these rules consume a lot of the AI agent's **context window**?

**A:** The always‑on rules are lightweight and have minimal impact on the AI agent’s context window. Glob‑scoped rules only apply to their matching file types. Below are Cursor examples: left, no rules; right, three always‑on rules enabled.

<p align="center">
  <img src="../images/context-window-no-rules.png" alt="Cursor AI agent context window usage without Project CodeGuard rules" width="40%" style="display:inline-block; margin-right:2%;" />
  <img src="../images/context-window-with-rules.png" alt="Cursor AI agent context window usage with Project CodeGuard rules enabled" width="40%" style="display:inline-block;" />
</p>

<center>
  <sub>
    <b>Left:</b> Context window usage without any rules in place.<br>
    <b>Right:</b> Context window usage with three always-on rules enabled.
  </sub>
</center>


---
## Q: What are the OWASP supplementary rules?

**A:** The `sources/owasp/` folder contains supplementary rules based on OWASP cheat sheets. These rules supplement the core security rules and can be optionally included when building from source. By default, only core rules (22 files) are included in standard builds.

---

## Q: How can I use the rules in my own AI agent?

**A:** You can use the rules in your own AI agent by creating a custom ruleset. You can create a custom ruleset by creating a new file in the `.cursor/rules`, `.windsurf/rules`, `.github/instructions`, or `.agent/rules` directories and adding the rules you want to apply. You can also use the `project-codeguard/rules` repository as a template to create your own ruleset.

---

## Q: Why does the downloaded release folder appear empty?

**A:** After downloading and extracting the release, the folders may appear empty because the rule directories (`.cursor/`, `.windsurf/`, `.github/`, `.agent/`) start with a dot (`.`) and are hidden by default on most operating systems.

**To show hidden files:**

=== "macOS"
    
    In Finder, navigate to the extracted folder and press ++cmd+shift+period++ to toggle the visibility of hidden files. You should now see the `.cursor/`, `.windsurf/`, `.github/`, and `.agent/` directories.

=== "Windows"
    
    In File Explorer:
    
    1. Navigate to the extracted folder
    2. Click on the **View** tab in the ribbon
    3. Check the **Hidden items** checkbox

=== "Linux"
    
    In your file manager, press ++ctrl+h++ to toggle hidden files, or use `ls -la` in the terminal to view all files including hidden ones.

Once hidden files are visible, you can copy the appropriate directory (`.cursor/`, `.windsurf/`, `.github/`, or `.agent/`) to your project root.

---

## Q: Can I use this with Claude Code?

**A:** Yes! Install the Project CodeGuard Claude Code plugin (Agent Skill) and Claude will apply the security rules automatically while you code.

```bash
/plugin marketplace add project-codeguard/rules
/plugin install codeguard-security@project-codeguard
```

For team/repo defaults, add the plugin in `.claude/settings.json` so it’s enabled for all contributors. See the [Claude Code Plugin documentation](claude-code-skill-plugin.md) for details and troubleshooting.


## Q: How can I report a problem or enhancement to any of the rules?

**A:** You can report problems, successes, or suggest enhancements to any of the rules by:

1. **Creating a GitHub issue**: [Open an issue here](https://github.com/project-codeguard/rules/issues)
2. **Provide details**: Include which rule(s) are affected, the issue you encountered, and your suggested improvement
3. **Be specific**: If reporting a bug, include steps to reproduce and example code if possible

We welcome all feedback - whether it's a bug report, success story, or enhancement suggestion!

---

## Q: How can I contribute to these rules and this project?

**A:** You can contribute at any time by:

1. **Creating a pull request**: Submit code, documentation, or rule improvements directly
2. **Opening a GitHub issue**: Report bugs, suggest new rules, or propose enhancements
3. **Participating in discussions**: Share your experience and help other users
4. **Improving documentation**: Help make our docs clearer and more comprehensive

See [CONTRIBUTING.md](https://github.com/project-codeguard/rules/blob/main/CONTRIBUTING.md) for detailed guidelines on our contribution process.

---

## Q: Does Project CodeGuard replace my security scanners?

**A:** No, Project CodeGuard rules do not replace your security scanners. The primary purpose of CodeGuard is to help you avoid introducing new security vulnerabilities as you write code, by providing agentic rules and guidance directly in your IDE. If you perform a code review using these rules, Project CodeGuard will most likely identify many of the same vulnerabilities that security scanning tools would find. However, CodeGuard is not a comprehensive substitute for security scanners—automated security tools are designed to thoroughly analyze your entire codebase and catch a broader range of issues. For best results, use CodeGuard rules in combination with your existing security scanners to maximize your code’s security.

---

## Still have questions?

**Can't find your answer?** 

- [Open an issue](https://github.com/project-codeguard/rules/issues) with your question
- [Start a discussion](https://github.com/project-codeguard/rules/discussions) to chat with the community



