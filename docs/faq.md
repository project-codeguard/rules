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

**A:** No. The always-on rules are designed to be lightweight and efficient, and should not consume a lot of the AI agent's context window. The "glob" rules are designed to be applied only to the related file types specified in the rule.

---
## Q: What are the OWASP supplementary rules?

**A:** The `sources/owasp/` folder contains supplementary rules based on OWASP cheat sheets. These rules supplement the core security rules and can be optionally included when building from source. By default, only core rules (22 files) are included in standard builds.

---

## Q: How can I use the rules in my own AI agent?

**A:** You can use the rules in your own AI agent by creating a custom ruleset. You can create a custom ruleset by creating a new file in the `.cursor/rules`, `.windsurf/rules`, or `.github/instructions` directories and adding the rules you want to apply. You can also use the `project-codeguard/rules` repository as a template to create your own ruleset.

---

## Q: Why does the downloaded release folder appear empty?

**A:** After downloading and extracting the release, the folders may appear empty because the rule directories (`.cursor/`, `.windsurf/`, `.github/`) start with a dot (`.`) and are hidden by default on most operating systems.

**To show hidden files:**

=== "macOS"
    
    In Finder, navigate to the extracted folder and press ++cmd+shift+period++ to toggle the visibility of hidden files. You should now see the `.cursor/`, `.windsurf/`, and `.github/` directories.

=== "Windows"
    
    In File Explorer:
    
    1. Navigate to the extracted folder
    2. Click on the **View** tab in the ribbon
    3. Check the **Hidden items** checkbox

=== "Linux"
    
    In your file manager, press ++ctrl+h++ to toggle hidden files, or use `ls -la` in the terminal to view all files including hidden ones.

Once hidden files are visible, you can copy the appropriate directory (`.cursor/`, `.windsurf/`, or `.github/`) to your project root.

---

## Q: Can I use this with Claude Code?

**A:** Yes! Claude Code automatically reads and follows instructions from a `CLAUDE.md` file in your project root. To use Project CodeGuard rules with Claude Code you can point to the Project CodeGuard rules in your `CLAUDE.md` file.

When Claude Code operates in your project, it treats the Project CodeGuard security rules in `CLAUDE.md` as authoritative system instructions.


## Q: How can I report a problem or enhancement to any of the rules?

**A:** You can report problems, successes, or suggest enhancements to any of the rules by:

1. **Creating a GitHub issue**: [Open an issue here](https://github.com/project-codeguard/rules/issues)
2. **Provide details**: Include which rule(s) are affected, the issue you encountered, and your suggested improvement
3. **Be specific**: If reporting a bug, include steps to reproduce and example code if possible

We welcome all feedback - whether it's a bug report, success story, or enhancement suggestion!

---

## Q: Why do I get the following error message in GitHub for some of the rules?

```
Error in user YAML: (<unknown>): did not find expected alphabetic 
or numeric character while scanning an alias at line x column x
```

**A:** You can safely ignore this error. GitHub attempts to parse YAML headers combined with markdown content, which can cause this warning. It does not affect rule functionality - the rules will work correctly in your IDE regardless of this GitHub display issue.

---

## Q: How can I contribute to these rules and this project?

**A:** You can contribute at any time by:

1. **Creating a pull request**: Submit code, documentation, or rule improvements directly
2. **Opening a GitHub issue**: Report bugs, suggest new rules, or propose enhancements
3. **Participating in discussions**: Share your experience and help other users
4. **Improving documentation**: Help make our docs clearer and more comprehensive

See [CONTRIBUTING.md](https://github.com/project-codeguard/rules/blob/main/CONTRIBUTING.md) for detailed guidelines on our contribution process.

---

## Still have questions?

**Can't find your answer?** 

- [Open an issue](https://github.com/project-codeguard/rules/issues) with your question
- [Start a discussion](https://github.com/project-codeguard/rules/discussions) to chat with the community



