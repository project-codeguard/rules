# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Copilot Format Implementation

Generates .instructions.md files for GitHub Copilot with YAML frontmatter.
"""

from formats.base import BaseFormat, ProcessedRule


class CopilotFormat(BaseFormat):
    """
    GitHub Copilot format implementation (.instructions.md files).

    Copilot uses .instructions.md files with YAML frontmatter containing:
    - applyTo: File matching patterns
    - title: Rule title/description
    - version: Rule version
    """

    def get_format_name(self) -> str:
        """Return Copilot format identifier."""
        return "copilot"

    def get_file_extension(self) -> str:
        """Return Copilot format file extension."""
        return ".instructions.md"

    def get_output_subpath(self) -> str:
        """Return Copilot output subdirectory."""
        return ".github/instructions"

    def generate(self, rule: ProcessedRule, globs: str) -> str:
        """
        Generate Copilot .instructions.md format with YAML frontmatter.

        Args:
            rule: The processed rule to format
            globs: Glob patterns for file matching

        Returns:
            Formatted .instructions.md content
        """
        yaml_lines = []

        # Add applyTo (Copilot's equivalent of globs)
        yaml_lines.append(f"applyTo: '{globs}'")

        # Add description
        description = self._format_yaml_field("description", rule.description)
        if description:
            yaml_lines.append(description)

        # Add version
        yaml_lines.append(f"version: {self.version}")

        return self._build_yaml_frontmatter(yaml_lines, rule.content)
