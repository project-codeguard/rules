# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Claude Code Format Implementation

Generates .md files for Claude Code Skills/Plugins.
"""

from formats.base import BaseFormat, ProcessedRule


class ClaudeCodeFormat(BaseFormat):
    """
    Claude Code plugin format implementation (.md files).
    
    Claude Code Skills use standard markdown files without
    special frontmatter. The original rule content is preserved
    and placed in the skills/software-security/rules/ directory
    for plugin distribution.
    
    Unlike other IDE formats, Claude Code doesn't require special
    frontmatter transformations - it uses the rules as-is for
    plugin-based Skills.
    """

    def get_format_name(self) -> str:
        """Return Claude Code format identifier."""
        return "claudecode"

    def get_file_extension(self) -> str:
        """Return Claude Code format file extension."""
        return ".md"

    def get_output_subpath(self) -> str:
        """Return Claude Code output subdirectory."""
        return "skills/software-security/rules"

    def generate(self, rule: ProcessedRule, globs: str) -> str:
        """
        Generate Claude Code .md format.
        
        Claude Code Skills should preserve the original YAML frontmatter
        (description, languages, alwaysApply) so the rules remain complete
        and can be referenced properly.
        
        Args:
            rule: The processed rule to format
            globs: Glob patterns (not used for Claude Code format)
        
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

