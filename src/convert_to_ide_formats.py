# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Convert Unified Rules to IDE Formats

Transforms the unified markdown sources into IDE-specific bundles (Cursor,
Windsurf, Copilot, Claude Code). This script is the main entry point for producing
distributable rule packs from the sources/ directory.
"""

import re
import shutil
from pathlib import Path
from collections import defaultdict

from converter import RuleConverter
from formats import CursorFormat, WindsurfFormat, CopilotFormat, ClaudeCodeFormat
from utils import get_version_from_pyproject
from validate_versions import set_plugin_version, set_marketplace_version

# Project root is always one level up from src/
PROJECT_ROOT = Path(__file__).parent.parent


def sync_plugin_metadata(version: str) -> None:
    """
    Sync version from pyproject.toml to Claude Code plugin metadata files.

    Args:
        version: Version string from pyproject.toml
    """
    set_plugin_version(version, PROJECT_ROOT)
    set_marketplace_version(version, PROJECT_ROOT)
    print(f"✅ Synced plugin metadata to {version}")


def update_skill_md(language_to_rules: dict[str, list[str]], skill_path: str) -> None:
    """
    Update SKILL.md with language-to-rules mapping table.

    Args:
        language_to_rules: Dictionary mapping languages to rule files
        skill_path: Path to SKILL.md file
    """
    # Generate markdown table
    table_lines = [
        "| Language | Rule Files to Apply |",
        "|----------|---------------------|",
    ]

    for language in sorted(language_to_rules.keys()):
        rules = sorted(language_to_rules[language])
        rules_str = ", ".join(rules)
        table_lines.append(f"| {language} | {rules_str} |")

    table = "\n".join(table_lines)

    # Markers for the language mappings section
    start_marker = "<!-- LANGUAGE_MAPPINGS_START -->"
    end_marker = "<!-- LANGUAGE_MAPPINGS_END -->"

    # Read SKILL.md
    skill_file = Path(skill_path)
    content = skill_file.read_text(encoding="utf-8")

    if start_marker not in content or end_marker not in content:
        raise RuntimeError(
            "Invalid template: Language mappings section not found in codeguard-SKILLS.md.template"
        )

    # Replace entire section including markers with just the table
    start_idx = content.index(start_marker)
    end_idx = content.index(end_marker) + len(end_marker)
    new_section = f"\n\n{table}\n\n"
    updated_content = content[:start_idx] + new_section + content[end_idx:]

    # Write back to SKILL.md
    skill_file.write_text(updated_content, encoding="utf-8")
    print(f"Updated SKILL.md with language mappings")


def convert_rules(input_path: str, output_dir: str = "dist", include_claudecode: bool = True, version: str = None) -> dict[str, list[str]]:
    """
    Convert rule file(s) to all supported IDE formats using RuleConverter.

    Args:
        input_path: Path to a single .md file or folder containing .md files
        output_dir: Output directory (default: 'dist/')
        include_claudecode: Whether to generate Claude Code plugin (default: True, only for core rules)
        version: Version string to use (default: read from pyproject.toml)

    Returns:
        Dictionary with 'success' and 'errors' lists:
        {
            "success": ["rule1.md", "rule2.md"],
            "errors": ["rule3.md: error message"]
        }

    Example:
        results = convert_rules("sources/core", "dist", include_claudecode=True)
        print(f"Converted {len(results['success'])} rules")
    """
    if version is None:
        version = get_version_from_pyproject()

    # Specify formats to generate
    all_formats = [
        CursorFormat(version),
        WindsurfFormat(version),
        CopilotFormat(version),
    ]
    
    # Only include Claude Code for core rules (committed plugin)
    if include_claudecode:
        all_formats.append(ClaudeCodeFormat(version))

    converter = RuleConverter(formats=all_formats)
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"{input_path} does not exist")

    # Determine files to process
    if path.is_file():
        if path.suffix != ".md":
            raise ValueError(f"{input_path} is not a .md file")
        md_files = [path]
    else:
        # Use rglob to recursively find all .md files in subdirectories
        md_files = sorted(list(path.rglob("*.md")))
        if not md_files:
            raise ValueError(f"No .md files found in {input_path}")
    
    print(f"Converting {len(md_files)} files from: {path}")

    # Setup output directory
    output_base = Path(output_dir)

    results = {"success": [], "errors": []}
    language_to_rules = defaultdict(list)

    # Process each file
    for md_file in md_files:
        try:
            # Convert the file (raises exceptions on error)
            result = converter.convert(md_file)

            # Write each format
            output_files = []
            for format_name, output in result.outputs.items():
                # Construct output path
                # Claude Code goes to project root ./skills/
                # Other formats go to dist/ (or specified output_dir)
                if format_name == "claudecode":
                    base_dir = PROJECT_ROOT
                else:
                    base_dir = output_base
                
                output_file = (
                    base_dir
                    / output.subpath
                    / f"{result.basename}{output.extension}"
                )

                # Create directory if it doesn't exist and write file
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(output.content, encoding="utf-8")
                output_files.append(output_file.name)

            print(f"Success: {result.filename} → {', '.join(output_files)}")
            results["success"].append(result.filename)

            # Update language mappings for SKILL.md
            for language in result.languages:
                language_to_rules[language].append(result.filename)

        except FileNotFoundError as e:
            error_msg = f"{md_file.name}: File not found - {e}"
            print(f"Error: {error_msg}")
            results["errors"].append(error_msg)

        except ValueError as e:
            error_msg = f"{md_file.name}: Validation error - {e}"
            print(f"Error: {error_msg}")
            results["errors"].append(error_msg)

        except Exception as e:
            error_msg = f"{md_file.name}: Unexpected error - {e}"
            print(f"Error: {error_msg}")
            results["errors"].append(error_msg)

    # Summary
    print(
        f"\nResults: {len(results['success'])} success, {len(results['errors'])} errors"
    )

    # Generate SKILL.md with language mappings (only if Claude Code is included)
    if include_claudecode and language_to_rules:
        template_path = PROJECT_ROOT / "sources" / "core" / "codeguard-SKILLS.md.template"
        
        if not template_path.exists():
            raise FileNotFoundError(
                f"SKILL.md template not found at {template_path}. "
                "This file is required for Claude Code plugin generation."
            )
        
        output_skill_dir = PROJECT_ROOT / "skills" / "software-security"
        output_skill_dir.mkdir(parents=True, exist_ok=True)
        output_skill_path = output_skill_dir / "SKILL.md"
        
        # Read template and inject current version from pyproject.toml
        template_content = template_path.read_text(encoding="utf-8")
        # Replace the hardcoded version with actual version
        template_content = re.sub(
            r'codeguard-version:\s*"[^"]*"',
            f'codeguard-version: "{version}"',
            template_content
        )
        output_skill_path.write_text(template_content, encoding="utf-8")
        
        update_skill_md(language_to_rules, str(output_skill_path))

    return results


def _resolve_source_paths(args) -> list[Path]:
    """
    Resolve source paths from CLI arguments.
    Priority: --source flags > default (core)
    """
    # If --source flags provided, resolve under sources/
    if args.source:
        return [Path("sources") / src for src in args.source]
    
    # Default: core rules only
    return [Path("sources/core")]


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    
    parser = ArgumentParser(
        description="Convert unified rule markdown into IDE-specific bundles."
    )
    parser.add_argument(
        "--source",
        nargs="+",
        help="Named sources under ./sources to convert (e.g., --source core owasp). Default: core",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="dist",
        help="Output directory for generated bundles (default: dist).",
    )
    
    cli_args = parser.parse_args()
    source_paths = _resolve_source_paths(cli_args)

    # Validate all source paths exist
    missing = [p for p in source_paths if not p.exists()]
    if missing:
        print(f"❌ Source path(s) not found: {', '.join(str(p) for p in missing)}")
        sys.exit(1)

    # Check for duplicate filenames across sources if multiple sources
    if len(source_paths) > 1:
        filename_to_sources = defaultdict(list)
        for source_path in source_paths:
            for md_file in source_path.rglob("*.md"):
                filename_to_sources[md_file.name].append(source_path.name)
        
        duplicates = {name: srcs for name, srcs in filename_to_sources.items() if len(srcs) > 1}
        if duplicates:
            print(f"❌ Found {len(duplicates)} duplicate filename(s) across sources:")
            for filename, sources in duplicates.items():
                print(f"   - {filename} in: {', '.join(sources)}")
            print("\nPlease rename files to have unique names across all sources.")
            sys.exit(1)
    
    # Get version once and sync to metadata files
    version = get_version_from_pyproject()
    sync_plugin_metadata(version)

    # Check if core is in the sources for Claude Code plugin generation
    has_core = Path("sources/core") in source_paths
    if has_core:
        # Validate template exists early
        template_path = PROJECT_ROOT / "sources" / "core" / "codeguard-SKILLS.md.template"
        if not template_path.exists():
            print(f"❌ SKILL.md template not found at {template_path}")
            print("This file is required for Claude Code plugin generation.")
            sys.exit(1)

    # Clean output directories once before processing
    output_path = Path(cli_args.output_dir)
    if output_path.exists():
        shutil.rmtree(output_path)
        print(f"✅ Cleaned {cli_args.output_dir}/ directory")

    if has_core:
        skills_rules_dir = PROJECT_ROOT / "skills" / "software-security" / "rules"
        if skills_rules_dir.exists():
            shutil.rmtree(skills_rules_dir)
            print(f"✅ Cleaned skills/ directory")
    
    # Print processing summary
    if len(source_paths) > 1:
        sources_list = ', '.join(p.name for p in source_paths)
        print(f"\nConverting {len(source_paths)} sources: {sources_list}")
        if has_core:
            print("(Claude Code plugin will include only core rules)")
        print()
    
    # Convert all sources
    aggregated = {"success": [], "errors": []}
    for source_path in source_paths:
        is_core = source_path == Path("sources/core")
        
        print(f"Processing: {source_path}")
        results = convert_rules(
            str(source_path), 
            cli_args.output_dir, 
            include_claudecode=is_core,
            version=version
        )
        
        aggregated["success"].extend(results["success"])
        aggregated["errors"].extend(results["errors"])
        print("")
    
    if aggregated["errors"]:
        print("❌ Some conversions failed")
        sys.exit(1)
    
    print("✅ All conversions successful")
