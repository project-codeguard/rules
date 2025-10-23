# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Validate Unified Rules Format

Validates that unified rules have correct YAML frontmatter and structure.
"""

import sys
from pathlib import Path

from language_mappings import LANGUAGE_TO_EXTENSIONS
from utils import parse_frontmatter_and_content


def validate_rule(file_path: Path) -> dict[str, list[str]]:
    """Validate a single unified rule file."""
    errors = []
    warnings = []

    try:
        # Read and parse file
        content = file_path.read_text(encoding="utf-8")
        frontmatter, markdown_content = parse_frontmatter_and_content(content)

        if frontmatter is None:
            errors.append("Missing or invalid YAML frontmatter")
            return {"errors": errors, "warnings": warnings}

        # Check required fields
        if "description" not in frontmatter:
            errors.append("Missing required field: description")
        elif not str(frontmatter["description"]).strip():
            errors.append("description cannot be empty")

        # Validate languages and alwaysApply logic
        has_languages = "languages" in frontmatter and frontmatter["languages"]
        always_apply = frontmatter.get("alwaysApply", False)

        if always_apply and has_languages:
            errors.append("Rules with alwaysApply=true should not have languages")
        elif not always_apply and not has_languages:
            errors.append("Rules must have either languages or alwaysApply=true")

        # Validate language names if present
        if has_languages and isinstance(frontmatter["languages"], list):
            unknown = [
                lang
                for lang in frontmatter["languages"]
                if lang.lower() not in LANGUAGE_TO_EXTENSIONS
            ]
            if unknown:
                warnings.append(f"Unknown languages: {', '.join(unknown)}")

        # Check content exists
        if not markdown_content.strip():
            errors.append("Rule content cannot be empty")

    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return {"errors": errors, "warnings": warnings}


def main():
    """Validate all rules in the sources directory."""
    rules_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "sources")

    if not rules_dir.exists():
        print(f"❌ Directory {rules_dir} does not exist")
        sys.exit(1)

    # Find all .md files recursively (excluding README and templates)
    md_files = [
        f for f in rules_dir.rglob("*.md") 
        if f.name.lower() != "readme.md" and not f.name.endswith(".template")
    ]

    if not md_files:
        print(f"❌ No rule files found in {rules_dir}")
        sys.exit(1)

    print(f"🔍 Validating {len(md_files)} rules in {rules_dir} (recursive)\n")

    passed = 0
    failed = 0
    total_warnings = 0

    for md_file in sorted(md_files):
        result = validate_rule(md_file)
        errors = result["errors"]
        warnings = result["warnings"]

        if errors:
            failed += 1
            print(f"❌ {md_file.name}")
            for error in errors:
                print(f"   - {error}")
        else:
            passed += 1
            if warnings:
                print(f"✅ {md_file.name}")
                for warning in warnings:
                    print(f"   ⚠️  {warning}")
                    total_warnings += 1
            else:
                print(f"✅ {md_file.name}")

    # Summary
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    if total_warnings:
        print(f"   Warnings: {total_warnings}")

    if failed > 0:
        print("\n❌ Validation failed")
        sys.exit(1)
    else:
        print("\n✅ All rules valid!")


if __name__ == "__main__":
    main()
