# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Agent Skills Format Implementation

Generates .md files for the Agent Skills standard (agentskills.io).
This format is used by OpenAI Codex, Claude Code, and other AI coding tools.
"""

from formats.base import BaseFormat, ProcessedRule


class AgentSkillsFormat(BaseFormat):
    """
    Agent Skills format implementation (.md files).

    Agent Skills (https://agentskills.io/) is an open standard for extending
    AI coding agents with task-specific capabilities. It uses standard markdown
    files with YAML frontmatter to define rules and instructions.

    This format is adopted by:
    - OpenAI Codex (skills)
    - Claude Code (plugins)
    - Other AI coding tools

    The original rule content is preserved and placed in the
    skills/software-security/rules/ directory for distribution.
    """

    def get_format_name(self) -> str:
        """Return Agent Skills format identifier."""
        return "agentskills"

    def get_file_extension(self) -> str:
        """Return Agent Skills format file extension."""
        return ".md"

    def get_output_subpath(self) -> str:
        """Return Agent Skills output subdirectory."""
        return "skills/software-security/rules"

    def generate(self, rule: ProcessedRule, globs: str) -> str:
        """
        Generate Agent Skills .md format.

        Agent Skills should preserve the original YAML frontmatter
        (description, languages, alwaysApply) so the rules remain complete
        and can be referenced properly by AI coding agents.

        Args:
            rule: The processed rule to format
            globs: Glob patterns (not used for Agent Skills format)

        Returns:
            Complete markdown with original YAML frontmatter preserved
        """
        # Build YAML frontmatter
        yaml_lines = []

        # Add description
        desc = self._format_yaml_field("description", rule.description)
        if desc:
            yaml_lines.append(desc)

        # Add languages if present
        if rule.languages:
            # Format as YAML list
            yaml_lines.append("languages:")
            for lang in rule.languages:
                yaml_lines.append(f"- {lang}")

        # Add alwaysApply
        yaml_lines.append(f"alwaysApply: {str(rule.always_apply).lower()}")

        return self._build_yaml_frontmatter(yaml_lines, rule.content)
