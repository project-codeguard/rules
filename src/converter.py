# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Rule Converter

Converts unified markdown rules to multiple IDE formats.
Handles parsing, validation, and format generation.
"""
from dataclasses import dataclass
from pathlib import Path

from language_mappings import languages_to_globs
from utils import parse_frontmatter_and_content
from formats import (
    BaseFormat,
    ProcessedRule,
)


@dataclass
class FormatOutput:
    """
    Represents the output for a single format.

    Attributes:
        content: The fully formatted content with frontmatter
        extension: File extension including dot (e.g., '.mdc')
        subpath: Subdirectory path (e.g., '.cursor/rules', 'skills/software-security/rules')
    """

    content: str
    extension: str
    subpath: str


@dataclass
class ConversionResult:
    """
    Represents the complete result of converting a rule file.

    Attributes:
        filename: Original filename (e.g., 'my-rule.md')
        basename: Filename without extension (e.g., 'my-rule')
        outputs: Dictionary mapping format names to their outputs
        languages: List of programming languages the rule applies to, empty list if always applies
    Example:
        result = ConversionResult(
            filename="my-rule.md",
            basename="my-rule",
            outputs={
                "cursor": FormatOutput(
                    content="---\\n...\\n---\\n\\nContent",
                    extension=".mdc",
                    subpath=".cursor/rules"
                )
            },
            languages=["python", "javascript"]
        )
    """

    filename: str
    basename: str
    outputs: dict[str, FormatOutput]
    languages: list[str]


class RuleConverter:
    """
    Converts markdown rules to multiple IDE formats.

    Uses the BaseFormat abstraction to support multiple IDE formats in an extensible way.
    New formats can be added by creating a new BaseFormat subclass and passing it to the converter.

    Main Methods:
        - parse_rule(): Parse markdown file with YAML frontmatter
        - generate_globs(): Convert languages to glob patterns
        - convert(): Convert a rule file to all registered formats (returns ConversionResult)

    Example:
        # Create converter
        from converter import RuleConverter, ConversionResult, FormatOutput
        from formats import CursorFormat, WindsurfFormat
        from utils import get_version_from_pyproject

        version = get_version_from_pyproject()
        converter = RuleConverter(formats=[
            CursorFormat(version),
            WindsurfFormat(version)
        ])

        # Convert a file
        try:
            result = converter.convert("rule.md")
            # result is ConversionResult dataclass

            for format_name, output in result.outputs.items():
                # output is FormatOutput dataclass
                print(f"{format_name}: {output.extension}")
                save_file(output.content, output.subpath)
        except ValueError as e:
            print(f"Invalid rule: {e}")
    """

    def __init__(self, formats: list[BaseFormat]):
        """
        Initialize the converter with version info and supported formats.

        Args:
            formats: List of BaseFormat instances to use for conversion.
        """
        self.formats = formats

    def parse_rule(self, content: str, filename: str) -> ProcessedRule:
        """
        Parse a markdown file with required frontmatter.

        Args:
            content: Full file content with YAML frontmatter
            filename: Name of the file being parsed

        Returns:
            ProcessedRule with validated frontmatter and content

        Raises:
            ValueError: If frontmatter is missing or invalid
        """
        # Parse frontmatter and content using shared utility
        frontmatter, markdown_content = parse_frontmatter_and_content(content)

        if not frontmatter:
            raise ValueError(f"Missing or invalid frontmatter in {filename}")

        # Validate required description field
        if "description" not in frontmatter or not frontmatter["description"].strip():
            raise ValueError(f"Missing required 'description' field in {filename}")

        always_apply = frontmatter.get("alwaysApply", False)

        # Validate languages field based on alwaysApply setting
        if always_apply:
            # If alwaysApply is true, languages should not be specified or should be empty
            if "languages" in frontmatter and frontmatter["languages"]:
                raise ValueError(
                    f"When 'alwaysApply' is true, 'languages' should not be specified or should be empty in {filename}"
                )
            languages = []  # No languages when always applying
        else:
            # If alwaysApply is false, languages is required
            if "languages" not in frontmatter:
                raise ValueError(
                    f"Missing required 'languages' field in {filename} (required when alwaysApply is false)"
                )

            languages = frontmatter["languages"]
            if not isinstance(languages, list) or not languages:
                raise ValueError(
                    f"'languages' must be a non-empty list in {filename} when alwaysApply is false"
                )

        # Adding rule_id to the beginning of the content
        rule_id = Path(filename).stem
        markdown_content = f"rule_id: {rule_id}\n\n{markdown_content}"

        return ProcessedRule(
            description=frontmatter["description"],
            languages=[lang.lower() for lang in languages],
            always_apply=always_apply,
            content=markdown_content,
            filename=filename,
        )

    def generate_globs(self, languages: list[str]) -> str:
        """
        Generate comma-separated glob patterns for languages.

        Args:
            languages: List of programming languages

        Returns:
            Comma-separated glob patterns, or "**/*" for all files
        """
        # Use shared function from language_mappings
        globs = languages_to_globs(languages)
        return globs if globs else "**/*"

    def convert(self, filepath: str) -> ConversionResult:
        """
        Convert a rule file to all registered formats.

        This method handles the entire conversion pipeline:
        - Reading the file
        - Parsing and validating
        - Generating all format outputs

        Args:
            filepath: Path to the rule file to convert (str or Path)

        Returns:
            ConversionResult with filename, basename, and format outputs

        Raises:
            FileNotFoundError: If the rule file doesn't exist
            ValueError: If the rule has invalid frontmatter or structure
            Exception: For other unexpected errors during conversion

        Example:
            try:
                result = converter.convert("rules/my-rule.md")
                for format_name, output in result.outputs.items():
                    path = f"{output.subpath}/{result.basename}{output.extension}"
                    write_file(path, output.content)
            except (FileNotFoundError, ValueError) as e:
                print(f"Error: {e}")
        """
        filepath = Path(filepath)
        filename = filepath.name
        basename = filepath.stem

        # Read the rule file (may raise FileNotFoundError)
        content = filepath.read_text(encoding="utf-8")

        # Parse and validate (may raise ValueError)
        rule = self.parse_rule(content, filename)

        # Generate globs once for all formats
        globs = self.generate_globs(rule.languages)

        # Generate output for each format
        outputs = {}
        for format_handler in self.formats:
            format_name = format_handler.get_format_name()
            outputs[format_name] = FormatOutput(
                content=format_handler.generate(rule, globs),
                extension=format_handler.get_file_extension(),
                subpath=format_handler.get_output_subpath(),
            )

        return ConversionResult(
            filename=filename,
            basename=basename,
            outputs=outputs,
            languages=rule.languages,
        )
