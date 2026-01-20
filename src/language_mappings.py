# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# SPDX-License-Identifier: Apache-2.0

"""
Shared language mappings for all rule tools.
Single source of truth for language-to-extension mappings.
"""

# Master mapping of languages to file extensions
LANGUAGE_TO_EXTENSIONS = {
    "apex": [".cls", ".trigger"],
    "python": [".py", ".pyx", ".pyi"],
    "javascript": [".js", ".jsx", ".mjs"],
    "typescript": [".ts", ".tsx"],
    "java": [".java"],
    "c": [".c", ".h"],
    "cpp": [".cpp", ".hpp", ".cc", ".cxx"],
    "c++": [".cpp", ".hpp", ".cc", ".cxx"],  # Alias
    "go": [".go"],
    "rust": [".rs"],
    "ruby": [".rb"],
    "php": [".php"],
    "swift": [".swift"],
    "kotlin": [".kt", ".kts"],
    "scala": [".scala"],
    "r": [".r", ".R"],
    "matlab": [".m"],
    "julia": [".jl"],
    "dart": [".dart"],
    "lua": [".lua"],
    "perl": [".pl", ".pm"],
    "shell": [".sh", ".bash"],
    "powershell": [".ps1"],
    "fsharp": [".fs", ".fsx"],
    "clojure": [".clj", ".cljs"],
    "elixir": [".ex", ".exs"],
    "erlang": [".erl", ".hrl"],
    "ocaml": [".ml", ".mli"],
    "nim": [".nim"],
    "vlang": [".v"],
    "zig": [".zig"],
    "d": [".d"],
    "solidity": [".sol"],
    "vyper": [".vy"],
    "cairo": [".cairo"],
    "sway": [".sway"],
    "handlebars": [".hbs"],
    "liquid": [".liquid"],
    "markdown": [".md"],
    "mdx": [".mdx"],
    "latex": [".tex"],
    "yaml": [".yml", ".yaml"],
    "docker": ["Dockerfile*", "docker-compose*", ".dockerfile"],
    "xml": [".xml", ".xsd", ".xslt", ".wsdl"],
    "vue": [".vue"],
    "svelte": [".svelte"],
    "astro": [".astro"],
    "elm": [".elm"],
    "purescript": [".purs"],
    "idris": [".idr"],
    "agda": [".agda"],
    "lean": [".lean"],
    "coq": [".coq"],
    "verilog": [".v"],
    "vhdl": [".vhd", ".vhdl"],
    "cuda": [".cu", ".cuh"],
    "opencl": [".cl"],
    "glsl": [".glsl", ".vert", ".frag"],
    "hlsl": [".hlsl"],
    "wgsl": [".wgsl"],
    "html": [".html", ".htm"],
    "sql": [".sql", ".ddl", ".dml"],
}

# Reverse mapping: extension to language (for conversion from globs)
EXTENSION_TO_LANGUAGE = {}
for lang, exts in LANGUAGE_TO_EXTENSIONS.items():
    for ext in exts:
        # First language wins for duplicate extensions
        if ext not in EXTENSION_TO_LANGUAGE:
            EXTENSION_TO_LANGUAGE[ext] = lang


def languages_to_globs(languages: list[str]) -> str:
    """
    Convert list of languages to glob patterns.
    
    Args:
        languages: List of programming language names (e.g., ['python', 'javascript'])
    
    Returns:
        Comma-separated glob patterns (e.g., '**/*.py,**/*.js')
        Empty string if no languages provided
    """
    if not languages:
        return ""

    extensions = []
    for lang in languages:
        if lang in LANGUAGE_TO_EXTENSIONS:
            for ext in LANGUAGE_TO_EXTENSIONS[lang]:
                if "*" in ext:
                    extensions.append(ext)
                else:
                    extensions.append(f"**/*{ext}")

    return ",".join(sorted(set(extensions)))


def globs_to_languages(globs: str) -> list[str]:
    """
    Convert glob patterns to list of languages.
    
    Args:
        globs: Comma-separated glob patterns (e.g., '**/*.py,**/*.js')
    
    Returns:
        Sorted list of language names that match the glob patterns
        Empty list if no patterns or universal glob provided
    """
    if not globs or globs in ["**", "*", "**/*"]:
        return []

    languages = set()
    patterns = globs.split(",")

    for pattern in patterns:
        pattern = pattern.strip().lower()

        # Check for file extensions and patterns
        for ext, lang in EXTENSION_TO_LANGUAGE.items():
            if ext.lower() in pattern:
                languages.add(lang)
                break  # One match per pattern is enough

    return sorted(languages)
