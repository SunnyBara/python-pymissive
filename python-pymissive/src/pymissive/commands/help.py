"""Help utility - read and display command docs from docs/commands/ or _docs/."""

from __future__ import annotations

import sys
from pathlib import Path


def _get_commands_dir() -> Path:
    """Return commands package directory."""
    return Path(__file__).resolve().parent


def get_docs_path(command_name: str) -> Path:
    """Return path to command doc. Checks package _docs/ then project docs/commands/."""
    cmd_dir = _get_commands_dir()
    # Package-installed: pymissive/commands/_docs/{command}.md
    pkg_doc = cmd_dir / "_docs" / f"{command_name}.md"
    if pkg_doc.exists():
        return pkg_doc
    # Dev: python-pymissive/docs/commands/{command}.md
    for parent in [cmd_dir.parent.parent, cmd_dir.parent, Path.cwd()]:
        doc = parent / "docs" / "commands" / f"{command_name}.md"
        if doc.exists():
            return doc
    return pkg_doc


def get_readme_path() -> Path:
    """Return path to README.md."""
    base = _get_commands_dir().parent
    for parent in [base.parent.parent, base.parent, Path.cwd()]:
        readme = parent / "README.md"
        if readme.exists():
            return readme
    return base.parent / "README.md"


def print_command_help(command_name: str) -> bool:
    """Print command doc from docs/commands/{name}.md. Returns True if displayed."""
    path = get_docs_path(command_name).resolve()
    if not path.exists():
        print(f"No documentation found for {command_name}", file=sys.stderr)
        return False
    try:
        content = path.read_text(encoding="utf-8")
        print(content)
        return True
    except OSError as e:
        print(f"Cannot read doc: {e}", file=sys.stderr)
        return False


def print_readme() -> bool:
    """Print README.md. Returns True if displayed."""
    path = get_readme_path().resolve()
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
        print(content)
        return True
    except OSError:
        return False
