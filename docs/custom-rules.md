# Custom Rules

Create custom rules to enforce your own policies, compliance requirements, or coding standards.

## Quick Start

1. **Create a source folder** under `sources/`:

        sources/
          core/             # Project CodeGuard rules
          owasp/            # OWASP supplementary rules
          my-rules/         # Your custom rules

2. **Copy the template** from `sources/templates/custom-rule-template.md.example` and customize it

3. **Build with your rules**:

        uv run python src/convert_to_ide_formats.py --source core my-rules

## Frontmatter Schema

| Field | Required | Description |
|:------|:---------|:------------|
| `description` | Yes | Brief description of the rule |
| `languages` | If `alwaysApply` is false | List of languages this rule applies to |
| `alwaysApply` | No | If `true`, rule applies to all files (omit `languages`) |
| `tags` | No | Filtering categories (see `src/tag_mappings.py`) |

## CLI Reference

### convert_to_ide_formats.py

Converts source rules to IDE-specific formats.

| Option | Description |
|--------|-------------|
| `--source` | Source folders under `sources/` to include. Default: `core` |
| `--output-dir`, `-o` | Output directory for generated bundles. Default: `dist` |
| `--tag` | Filter rules by tags (comma-separated, case-insensitive, AND logic) |

**Examples:**

```bash
# Default: convert core rules only
uv run python src/convert_to_ide_formats.py

# Include multiple sources
uv run python src/convert_to_ide_formats.py --source core owasp my-rules

# Custom output directory
uv run python src/convert_to_ide_formats.py --source core my-rules -o build

# Filter to only rules tagged with data-security
uv run python src/convert_to_ide_formats.py --tag data-security

# Multiple tags (AND logic - rules must have ALL tags)
uv run python src/convert_to_ide_formats.py --tag data-security,authentication
```

### validate_unified_rules.py

Validates rule files have correct frontmatter and structure before building.

```bash
# Validate all rules in a directory
uv run python src/validate_unified_rules.py sources/my-rules/

# Validate all sources
uv run python src/validate_unified_rules.py sources/
```

## Notes

- Filenames must be unique across all sources
- Use `.md` extension for all rule files
- Rules are converted to all supported IDE formats
- To add new tags, update `KNOWN_TAGS` in `src/tag_mappings.py`
