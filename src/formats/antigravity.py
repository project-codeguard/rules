# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Antigravity Format Implementation

Generates .md rule files for Antigravity with YAML frontmatter.
"""

from formats.base import BaseFormat, ProcessedRule


class AntigravityFormat(BaseFormat):
    """
    Antigravity format implementation (.md rule files).

    Antigravity uses .md files with YAML frontmatter containing:
    - trigger: 'always_on' or 'glob' (activation type)
    - globs: (if trigger is 'glob') File matching patterns
    - description: Rule description
    - version: Rule version
    
    Rules use activation types (Always On or Glob) to determine when
    they apply, similar to Windsurf's implementation.
    See: https://antigravity.google/docs/rules-workflows
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
            globs: Glob patterns for file matching

        Returns:
            Formatted .md content with trigger, globs, description, and version
        
        Note:
            Antigravity rules use activation types:
            - 'always_on': Rule applies to all files (when alwaysApply is true)
            - 'glob': Rule applies to files matching glob patterns (language-specific)
        """
        yaml_lines = []

        # Use trigger: always_on for rules that should always apply
        if rule.always_apply:
            yaml_lines.append("trigger: always_on")
        else:
            yaml_lines.append("trigger: glob")
            yaml_lines.append(f"globs: {globs}")

        # Add description (required by Antigravity spec)
        desc = self._format_yaml_field("description", rule.description)
        if desc:
            yaml_lines.append(desc)

        # Add version
        yaml_lines.append(f"version: {self.version}")

        return self._build_yaml_frontmatter(yaml_lines, rule.content)
