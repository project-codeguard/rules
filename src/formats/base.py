# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Base Format Class

Abstract base class for all IDE rule formats.
Defines the interface that all format implementations must follow.
"""

import yaml
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProcessedRule:
    """
    Represents a processed rule with required frontmatter.

    Attributes:
        description: Human-readable description of the rule
        languages: List of programming languages this rule applies to
        always_apply: Whether this rule should apply to all files
        content: The actual rule content in markdown format
        filename: Original filename of the rule
    """

    description: str
    languages: list[str]
    always_apply: bool
    content: str
    filename: str


class BaseFormat(ABC):
    """
    Abstract base class for IDE rule formats.

    This class defines the interface that all format implementations must follow.
    Each format is responsible for:
    - Providing its file extension (e.g., '.mdc', '.md')
    - Providing its output subdirectory path (e.g., '.cursor/rules')
    - Generating formatted content with proper frontmatter
    """

    def __init__(self, version: str):
        """
        Initialize format with version information.

        Args:
            version: Version string to include in generated files
        """
        self.version = version

    @abstractmethod
    def get_format_name(self) -> str:
        """
        Return the unique identifier for this format.

        Returns:
            Format name (e.g., 'cursor', 'windsurf', 'copilot')
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Return the file extension for this format.

        Returns:
            File extension including the dot (e.g., '.mdc', '.md')
        """
        pass

    @abstractmethod
    def get_output_subpath(self) -> str:
        """
        Return the subdirectory path for this format.

        Returns:
            Subdirectory path (e.g., '.cursor/rules', 'skills/software-security/rules')
        """
        pass

    @abstractmethod
    def generate(self, rule: ProcessedRule, globs: str) -> str:
        """
        Generate the formatted content for this IDE format.

        Args:
            rule: The processed rule to format
            globs: Glob patterns for file matching

        Returns:
            Fully formatted content with frontmatter and rule content
        """
        pass

    def _build_yaml_frontmatter(self, lines: list[str], content: str) -> str:
        """
        Helper to build complete file with YAML frontmatter.

        Args:
            lines: List of YAML lines to include in frontmatter
            content: The markdown content to append after frontmatter

        Returns:
            Complete formatted string with frontmatter and content
        """
        yaml_str = "\n".join(lines)
        return f"---\n{yaml_str}\n---\n\n{content}\n"

    def _format_yaml_field(self, field_name: str, value: str) -> str:
        """
        Format a field with proper YAML escaping for special characters.

        Args:
            field_name: Name of the YAML field
            value: Value to format

        Returns:
            Properly formatted YAML string, or empty string if value is empty
        """
        if value and value.strip():
            yaml_dump = yaml.safe_dump(
                {field_name: value},
                default_flow_style=False,
                allow_unicode=True,
            )
            return yaml_dump.strip()
        return ""
