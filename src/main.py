#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path

# Add the src directory to PYTHONPATH so alfred_results can be imported.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from alfred_results import ScriptFilterPayload
from alfred_results.result_item import ResultItem


def version_tuple(v: str) -> tuple[int, ...]:
    """Convert a version string into a tuple of integers for comparison.

    Args:
        v: A dot-separated version string (e.g. ``"2024.1.0"``).

    Returns:
        A tuple of integers representing each version component.
    """
    return tuple(map(int, v.split(".")))


AI_VERSION = version_tuple(os.getenv("AI_VERSION", ""))


def command_version_check(command: dict) -> bool:
    """Check whether a command is compatible with the running Illustrator version.

    Reads optional ``min_version`` and ``max_version`` keys from the command
    dict and compares them against the ``AI_VERSION`` module-level tuple.

    Args:
        command: A command dict that may contain ``"min_version"`` and/or
            ``"max_version"`` strings in dot-separated form.

    Returns:
        ``True`` if the current Illustrator version falls within the
        command's supported range; ``False`` otherwise.
    """
    if (
        command.get("min_version")
        and version_tuple(command["min_version"]) > AI_VERSION
    ):
        return False

    if (  # noqa: SIM103
        command.get("max_version")
        and version_tuple(command["max_version"]) < AI_VERSION
    ):
        return False

    return True


def main(argv: Sequence[str] | None = None) -> int:
    """Build and output the Alfred Script Filter payload for Illustrator commands.

    Loads ``commands.json`` from the same directory, filters out entries that
    are incompatible with the running Illustrator version, and appends fixed
    workflow items (Update Commands, User Actions, Recent Files).  The
    resulting JSON is written to ``stdout`` in Alfred Script Filter format.

    Args:
        argv: Unused command-line arguments; reserved for future use.

    Returns:
        Exit code ``0`` on success.
    """
    # load commands.json
    fp = Path(__file__).resolve().parent / "commands.json"
    try:
        with fp.open("r", encoding="utf-8") as f:
            data: list[dict[str, str]] = json.load(f)
    except FileNotFoundError:
        sys.stderr.write(f"commands.json not found at {fp}\n")
        data = []
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Failed to parse commands.json: {e}\n")
        data = []

    items: list[ResultItem] = []
    for row in data:
        title = row["title"]
        subtitle = row.get("subtitle", "")
        uid = f"alfred_ai_{row['uid']}"
        arg = row["arg"]

        # ensure ai version compatibility
        if not command_version_check(row):
            sys.stderr.write(f"command '{title}' failed version check\n")
            continue
        items.append(
            ResultItem(
                title=title,
                subtitle=subtitle,
                uid=uid,
                arg=arg,
                icon=None,
            )
        )

    # add workflow items
    workflow_items = [
        ResultItem(
            title="Update Commands",
            subtitle="Download the latest commands",
            arg="update-commands",
        ),
        ResultItem(
            title="User Actions",
            subtitle="Run user action...",
            arg="user-actions",
        ),
        ResultItem(
            title="Recent Files",
            subtitle="Open recent file...",
            arg="recent-files",
        ),
    ]

    items.extend(workflow_items)

    payload = ScriptFilterPayload(items=items)

    sys.stdout.write(payload.to_json())

    return 0


if __name__ == "__main__":
    main()
