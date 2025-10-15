"""
Convert Unified Rules to IDE Formats

Transforms the unified markdown sources into IDE-specific bundles (Cursor,
Windsurf, Copilot). This script is the main entry point for producing
distributable rule packs.
"""

from argparse import ArgumentParser
from pathlib import Path
import shutil
import sys

from converter import RuleConverter
from formats import CopilotFormat, CursorFormat, WindsurfFormat
from utils import get_version_from_pyproject


def convert_rules(input_path: str, output_dir: str = "dist") -> dict[str, list[str]]:
    """
    Convert rule file(s) to all supported IDE formats using RuleConverter.

    Args:
        input_path: Path to a single .md file or folder containing .md files
        output_dir: Output directory (default: 'dist')

    Returns:
        Dictionary with 'success' and 'errors' lists:
        {
            "success": ["rule1.md", "rule2.md"],
            "errors": ["rule3.md: error message"]
        }

    Example:
        results = convert_rules("sources/", "dist")
        print(f"Converted {len(results['success'])} rules")
    """
    version = get_version_from_pyproject()

    # Specify all formats that should be generated here
    all_formats = [
        CursorFormat(version),
        WindsurfFormat(version),
        CopilotFormat(version),
    ]

    converter = RuleConverter(formats=all_formats)
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"{input_path} does not exist")

    # Determine files to process
    if path.is_file():
        if path.suffix != ".md":
            raise ValueError(f"{input_path} is not a .md file")
        files_to_process = [path]
        print(f"Converting file: {path.name}")
    else:
        files_to_process = sorted(path.rglob("*.md"))
        if not files_to_process:
            raise ValueError(f"No .md files found in {input_path}")
        print(f"Converting {len(files_to_process)} files from subtree: {path}")

    # Setup output directory
    output_base = Path(output_dir)
    generated_rules_dir = output_base / "rules"

    results = {"success": [], "errors": []}

    # Process each file
    for md_file in files_to_process:
        try:
            # Convert the file (raises exceptions on error)
            result = converter.convert(md_file)

            # Write each format
            output_files = []
            for format_name, output in result.outputs.items():
                # Construct output path
                output_file = (
                    generated_rules_dir
                    / output.subpath
                    / f"{result.basename}{output.extension}"
                )

                # Create directory if it doesn't exist and write file
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(output.content, encoding="utf-8")
                output_files.append(output_file.name)

            print(f"Success: {result.filename} → {', '.join(output_files)}")
            results["success"].append(result.filename)

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

    return results


def _resolve_source_paths(args) -> list[Path]:
    """
    Determine which source paths to convert based on CLI arguments.

    Priority:
        1. Explicit positional paths (can be files or directories)
        2. Named sources via --source (resolved relative to ./sources)
        3. Default to ./sources/core
    """
    if args.inputs:
        return [Path(path) for path in args.inputs]

    if args.sources:
        base = Path("sources")
        return [(base / source_name) for source_name in args.sources]

    return [Path("sources/core")]


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Convert unified rule markdown into IDE-specific bundles."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Optional explicit file or directory paths to convert (overrides --source).",
    )
    parser.add_argument(
        "--source",
        dest="sources",
        action="append",
        help="Named source under ./sources to convert (e.g., --source core --source owasp).",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="dist",
        help="Output directory for generated bundles (default: dist).",
    )

    cli_args = parser.parse_args()
    source_paths = _resolve_source_paths(cli_args)

    generated_root = Path(cli_args.output_dir) / "rules"
    if generated_root.exists():
        print(f"Removing existing generated bundles at {generated_root}")
        shutil.rmtree(generated_root)

    print("Converting sources:")
    for path in source_paths:
        print(f"  • {path}")

    aggregated = {"success": [], "errors": []}
    for source_path in source_paths:
        results = convert_rules(str(source_path), cli_args.output_dir)
        aggregated["success"].extend(results["success"])
        aggregated["errors"].extend(results["errors"])

    if aggregated["errors"]:
        print("\nOne or more conversions failed.")
        sys.exit(1)
