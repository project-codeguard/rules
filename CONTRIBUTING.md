# Contributing

## How to contribute?

Project CodeGuard is an open-source initiative actively seeking contributions from the community. This document outlines how to get involved and the process we follow for proposing, reviewing, and merging changes.

In general, a Project CodeGuard Contributor is expected to:
- be knowledgeable in one or more areas related to the project
- contribute to developing and finalizing workstream deliverables
- be reliable in completing issues they take on
- show commitment over time with one or more PRs merged
- follow the project style and testing guidelines
- follow branch, PR, and code style conventions
- contribute in ways that substantially improve the quality of the project and the experience of people who use it

When contributing to any CodeGuard repository, please first discuss the change you wish to make via a GitHub issue. For small fixes, opening a PR directly with clear context is fine; for larger changes or new features, please open an issue first to align on scope and approach.

Please note that all of your interactions in the project are subject to our [Code of Conduct](CODE_OF_CONDUCT.md). This includes creation of issues or pull requests, commenting on issues or pull requests, and extends to all interactions in any real-time space.

Please be respectful of differing opinions when discussing potential contributions. We aim for a welcoming, collaborative environment for all contributors.

## Content Update Governance Process

CodeGuard uses a two-stage governance process for updates to the project’s rules, controls, and other structured content. This separates technical review from community governance, ensuring both content quality and project alignment.

### What Constitutes a Content Update

Content updates include changes to:
- Rules definitions, categories, and metadata
- Security control specifications and mappings
- Component or taxonomy elements and relationships
- Content-oriented documentation and guidance materials

### Two-Stage Process Overview

**Stage 1: Technical Review** – Content `feature` branches merge to the `develop` branch after standard PR review

**Stage 2: Community Review** – Bi-weekly governance review of the `develop` branch’s accumulated changes before release to `main`

```
feature-branch  →  develop    →    main
     ↑                 ↑             ↑
  Stage 1         Stage 2        Release
(Technical)       (Community)
```

### Non-Content Changes

The following types of changes are not covered by the two-stage content update process and continue to follow existing workflows:
- Bug fixes – technical corrections and error resolution
- Implementation changes – updates to code logic, algorithms, or system functionality
- Infrastructure updates – CI/CD, build processes, deployment configurations
- Documentation fixes – corrections to technical documentation, README updates, etc.
- Security patches – critical security-related fixes requiring immediate deployment
- Dependency updates – library upgrades and security patches for dependencies

These excluded change types may follow direct-to-`main` workflows as determined by repository maintainers and policies.

## Repository Structure

- **`sources/`** - Source rules (edit these: `core/` has 22 files, `owasp/` has 88)
- **`src/`** - Conversion and validation tools
- **`skills/`** - Claude Code plugin (generated, committed)
- **`dist/`** - Other IDE bundles (generated, not committed)

## First-time contributors

If you are new to the project and looking for an entry point, check the open issues. Issues tagged `good first issue` are meant to be small, well-scoped tasks suitable for first-time contributors. If you find one you’d like to work on, comment on the issue and/or assign yourself, and a maintainer can confirm assignment.

## Submitting a new issue

If you want to create a new issue that doesn't exist already, open a new one and include:
- a concise problem statement or feature request
- steps to reproduce (for bugs)
- expected vs. actual behavior
- environment details (versions, OS) if applicable
- proposed approach or alternatives (optional but helpful)

**If you discover a security bug, please do not report it through GitHub. Instead, please see security procedures in [SECURITY.md](SECURITY.md).**

## Submitting a new pull request and review process

The process for submitting pull requests depends on the type of change:

### For Content Updates (Two-Stage Process)

Follow these steps when submitting content updates:

1. Fork this repo into your GitHub account. If you have write access, you may create a branch directly.
2. Create a new branch, based on the `develop` branch, with a name that concisely describes what you’re working on.
3. Ensure that your changes pass validation and do not cause any existing tests to fail.
4. Submit a pull request against the `develop` branch.

#### Content Update PR Review

**Stage 1 Review**: Your PR to `develop` will be reviewed for technical criteria including content correctness, formatting and schema validation (where applicable), code hygiene, and commit message quality.

**Stage 2 Review**: On a regular cadence (typically bi-weekly), a PR will be created from `develop` to `main` containing all merged content changes from the cycle period. This undergoes community review by maintainers and contributors using lazy consensus and/or simple voting procedures as needed.

### For Non-Content Changes (Standard Process)

Follow these steps when submitting non-content changes (bug fixes, implementation changes, infrastructure updates, etc.):

1. Fork this repo into your GitHub account (or create a branch if you have write access).
2. Create a new branch, based on the `main` branch, with a name that concisely describes what you’re working on.
3. Ensure that your changes do not cause any existing tests to fail.
4. Submit a pull request against the `main` branch.

#### Non-Content PR Review
1. PRs will be reviewed by maintainers. Additional reviewers may be requested depending on scope.
2. Reviewer responses are typically due within 3 business days.

### General Review Guidelines

Maintainers aim to review pull requests and issues within 3 business days.

[Lazy consensus](https://openoffice.apache.org/docs/governance/lazyConsensus.html) is practiced for this project. Major changes in GitHub or to a project document on any official platform should be accompanied by an issue or discussion with a comment period of no less than seven (7) business days, mindful of major world holidays.

## Branch naming and commit messages

### Branch naming

- `main` – main development branch and authoritative source; updated after community approval for content changes
- `develop` – staging area for community review of content updates; feature branches for content changes target this branch
- `feature` – feature/this-is-a-new-feature-branch (target `develop` for content updates, `main` for non-content changes)
- `codebugfix` – codebugfix/description-of-the-bug (typically targets `main`)
- `languagefix` – languagefix/description-of-the-language-fix (typically targets `main`)
- `docs` – docs/description-of-the-documentation-change (typically targets `main`; documentation changes are exempt from the content update rule above)
- `release` – release/description-of-the-release – cut from `main` when ready

### Commit messages format

Write commit messages that clearly explain the change by continuing the sentence “This commit …”.

Examples of good commit messages:
- "This commit renames the examples folder to reference-implementations."
- "This commit bumps dependency versions to address security advisories."

## Release Process (Maintainers)

### Step 1: Update Version

```bash
# Edit pyproject.toml and update the version number
vi pyproject.toml  # Change version = "1.2.3"

# Regenerate all IDE bundles (auto-syncs version to JSON files)
uv run python src/convert_to_ide_formats.py

# Review changes
git diff

# Commit changes
git add -A
git commit -m "Bump version to 1.2.3"

# Push to main (via PR or direct)
git push origin main
```

**Note**: The conversion script automatically syncs the version from `pyproject.toml` to:
- `.claude-plugin/plugin.json` and `marketplace.json` (Claude Code plugin metadata)
- All generated IDE rule files (Cursor `.mdc`, Windsurf `.md`, Copilot `.instructions.md`, Claude Code `.md`)

This ensures version consistency across all artifacts.

### Step 2: Create Release (GitHub UI)

1. Go to: https://github.com/project-codeguard/rules/releases/new
2. **Tag**: Enter `vX.Y.Z` (must match version in pyproject.toml)
3. **Title**: `Project CodeGuard vX.Y.Z`
4. Click **"Generate release notes"** (auto-generates changelog)
5. Click **"Publish release"**

GitHub Actions will automatically:
- ✅ Validate versions match the tag
- ✅ Build IDE bundles (Cursor, Windsurf, Copilot)
- ✅ Upload ZIP artifacts to the release

## Testing Your Changes

```bash
# Validate rules (required if you modified rules)
python src/validate_unified_rules.py sources/

# Regenerate skills/ (required if you modified rules)
python src/convert_to_ide_formats.py
git add skills/  # skills/ is version-controlled

# Test with all sources (core + owasp)
python src/convert_to_ide_formats.py --source core owasp -o test-output/
# Check: test-output/.cursor/, test-output/.windsurf/, etc.

# Get help
python src/convert_to_ide_formats.py --help
```

## Feedback

Questions or comments about this project may be composed as GitHub issues or PR comments. If a broader discussion is needed, open or reference a GitHub Discussion (if enabled) or propose a short design doc in an issue.