# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Formats Package

This package contains all IDE format implementations for rule conversion.

Available Formats:
- CursorFormat: Generates .mdc files for Cursor IDE
- WindsurfFormat: Generates .md files for Windsurf IDE
- CopilotFormat: Generates .instructions.md files for GitHub Copilot
- AgentSkillsFormat: Generates .md files for Agent Skills (OpenAI Codex, Claude Code, other AI coding tools)
- AntigravityFormat: Generates .md files for Google Antigravity

Usage:
    from formats import BaseFormat, ProcessedRule, CursorFormat, WindsurfFormat, CopilotFormat, ClaudeCodeFormat

    version = "1.0.0"
    formats = [
        CursorFormat(version),
        WindsurfFormat(version),
        CopilotFormat(version),
        AgentSkillsFormat(version),
        AntigravityFormat(version),
    ]
"""

from formats.base import BaseFormat, ProcessedRule
from formats.cursor import CursorFormat
from formats.windsurf import WindsurfFormat
from formats.copilot import CopilotFormat
from formats.agentskills import AgentSkillsFormat
from formats.antigravity import AntigravityFormat

__all__ = [
    "BaseFormat",
    "ProcessedRule",
    "CursorFormat",
    "WindsurfFormat",
    "CopilotFormat",
    "AgentSkillsFormat",
    "AntigravityFormat",
]
