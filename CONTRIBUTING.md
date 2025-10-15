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

## First-time contributors

If you are new to the project and looking for an entry point, check the open issues. Issues tagged `good first issue` are meant to be small, well-scoped tasks suitable for first-time contributors. If you find one you’d like to work on, comment on the issue and/or assign yourself, and a maintainer can confirm assignment.

## Submitting a new issue

If you want to create a new issue that doesn’t exist already, open a new one and include:
- a concise problem statement or feature request
- steps to reproduce (for bugs)
- expected vs. actual behavior
- environment details (versions, OS) if applicable
- proposed approach or alternatives (optional but helpful)

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
- `codebugfix` – codebugfix/name-of-the-bug (typically targets `main`)
- `languagefix` – languagefix/fix-details (typically targets `main`)
- `release` – release/1.0.0 – cut from `main` when ready

### Rebasing note

**For content updates**: After completing work on a feature branch, rebase on `develop` before opening a PR. After PR approval, rebase again to ensure the latest `develop` changes are included before merging.

**For non-content changes**: After completing work on a feature branch, rebase on `main` before opening a PR. After PR approval, rebase again to ensure the latest `main` changes are included before merging.

### Commit messages format

Write commit messages that clearly explain the change by continuing the sentence “This commit …”.

Examples of good commit messages:
- "This commit renames the examples folder to reference-implementations."
- "This commit bumps dependency versions to address security advisories."

## Release Process

For maintainers creating a new release:

1. Bump `[project].version` in `pyproject.toml` to the new `major.minor.patch` on a feature branch.
2. Open a pull request into `develop`; once approved, merge the version bump into `develop`.
3. Create a short-lived release branch from `develop`, run final checks, and merge that branch into `main`.
4. Tag the merge commit on `main` (`git tag vX.Y.Z && git push origin vX.Y.Z`) and publish a GitHub Release from that tag.
5. The `Build IDE Bundles` workflow runs automatically, attaches `dist/ide-rules.zip` to the release, and uploads the same file as a workflow artifact.

## Feedback

Questions or comments about this project may be composed as GitHub issues or PR comments. If a broader discussion is needed, open or reference a GitHub Discussion (if enabled) or propose a short design doc in an issue.