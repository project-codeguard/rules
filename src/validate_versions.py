#!/usr/bin/env python3
# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Version Validation Script

Validates that all version strings match across:
- pyproject.toml
- .claude-plugin/plugin.json
- .claude-plugin/marketplace.json
"""

import json
import re
import sys
import tomllib
from pathlib import Path
from typing import NamedTuple


class VersionCheck(NamedTuple):
    """Result of a version check."""

    file: str
    expected: str
    found: str
    matches: bool


def get_pyproject_version(root: Path) -> str:
    """Get version from pyproject.toml."""
    pyproject_path = root / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


def get_plugin_version(root: Path) -> str:
    """Get version from plugin.json."""
    plugin_path = root / ".claude-plugin" / "plugin.json"
    with open(plugin_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["version"]


def set_plugin_version(version: str, root: Path) -> None:
    """Set version in plugin.json."""
    plugin_path = root / ".claude-plugin" / "plugin.json"
    with open(plugin_path, encoding="utf-8") as f:
        data = json.load(f)
    data["version"] = version
    with open(plugin_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def get_marketplace_version(root: Path) -> str:
    """Get version from marketplace.json."""
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    with open(marketplace_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["plugins"][0]["version"]


def set_marketplace_version(version: str, root: Path) -> None:
    """Set version in marketplace.json."""
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    with open(marketplace_path, encoding="utf-8") as f:
        data = json.load(f)
    for plugin in data.get("plugins", []):
        plugin["version"] = version
    with open(marketplace_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def _read_front_matter_value(path: Path, key: str) -> str:
    """Read a YAML front-matter value from a markdown file."""
    content = path.read_text(encoding="utf-8")
    front_matter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not front_matter_match:
        raise ValueError(f"Missing front matter in {path}")
    front_matter = front_matter_match.group(1)
    value_match = re.search(
        rf'^{re.escape(key)}:\s*"([^"]+)"\s*$',
        front_matter,
        re.MULTILINE,
    )
    if not value_match:
        raise ValueError(f"Missing {key} in front matter for {path}")
    return value_match.group(1)


def get_skill_codeguard_version(root: Path) -> str:
    """Get codeguard-version from skills/software-security/SKILL.md."""
    skill_path = root / "skills" / "software-security" / "SKILL.md"
    return _read_front_matter_value(skill_path, "codeguard-version")


def validate_versions(expected_version: str, root: Path = None) -> list[VersionCheck]:
    """
    Validate all versions match the expected version.

    Args:
        expected_version: The version to validate against (e.g., from git tag)
        root: Project root directory (defaults to parent of this script)

    Returns:
        List of VersionCheck results
    """
    if root is None:
        root = Path(__file__).parent.parent

    checks = [
        VersionCheck(
            "pyproject.toml", expected_version, get_pyproject_version(root), False
        ),
        VersionCheck("plugin.json", expected_version, get_plugin_version(root), False),
        VersionCheck(
            "marketplace.json", expected_version, get_marketplace_version(root), False
        ),
        VersionCheck(
            "SKILL.md",
            expected_version,
            get_skill_codeguard_version(root),
            False,
        ),
    ]

    # Update matches field
    return [
        VersionCheck(c.file, c.expected, c.found, c.expected == c.found) for c in checks
    ]


def main() -> int:
    """Main entry point for CLI."""
    if len(sys.argv) != 2:
        print("Usage: validate_versions.py <expected_version>")
        print("Example: validate_versions.py 1.0.0")
        return 1

    expected_version = sys.argv[1]
    results = validate_versions(expected_version)

    # Print results
    all_match = True
    for check in results:
        if check.matches:
            print(f"✅ {check.file}: {check.found}")
        else:
            print(f"❌ {check.file}: expected {check.expected}, found {check.found}")
            all_match = False

    if all_match:
        print(f"\n✅ All versions match: {expected_version}")
        return 0
    else:
        print(f"\n❌ Version mismatch detected!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
