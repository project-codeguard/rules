# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Antigravity Format Implementation

Generates .md rule files for Google Antigravity with YAML frontmatter.
"""

from formats.base import BaseFormat, ProcessedRule


class AntigravityFormat(BaseFormat):
    """
    Google Antigravity format implementation (.md workflow files).

    Antigravity uses .md files with YAML frontmatter containing:
    - description: Rule description (required by Antigravity spec)
    
    Workflows are stored in .agent/workflows/ and can be triggered
    on-demand with /workflow-name in the Antigravity interface.
    """

    def get_format_name(self) -> str:
        """Return Antigravity format identifier."""
        return "antigravity"

    def get_file_extension(self) -> str:
        """Return Antigravity format file extension."""
        return ".md"

    def get_output_subpath(self) -> str:
        """Return Antigravity output subdirectory."""
        return ".agent/rules"

    def generate(self, rule: ProcessedRule, globs: str) -> str:
        """
        Generate Antigravity .md format with YAML frontmatter.

        Args:
            rule: The processed rule to format
            globs: Glob patterns for file matching (not used by Antigravity)

        Returns:
            Formatted .md content with minimal frontmatter
        
        Note:
            Antigravity workflows use simple markdown with description-only
            frontmatter. Language/glob information is not needed as workflows
            are triggered manually by the user.
        """
        yaml_lines = []

        # Add description (required by Antigravity spec)
        desc = self._format_yaml_field("description", rule.description)
        if desc:
            yaml_lines.append(desc)
        
        # Optional: Add tags for categorization (if Antigravity supports it)
        if rule.tags:
            yaml_lines.append("tags:")
            for tag in rule.tags:
                yaml_lines.append(f"- {tag}")

        return self._build_yaml_frontmatter(yaml_lines, rule.content)