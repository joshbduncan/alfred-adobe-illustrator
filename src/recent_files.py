#!/usr/bin/env python3
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from alfred_results import ScriptFilterPayload
from alfred_results.result_item import ResultItem


def main(argv: Sequence[str] | None = None) -> int:
    """Build and output the Alfred Script Filter payload for recent files.

    Reads the ``RECENT_FILES`` environment variable, which is expected to
    contain a comma-separated list of file paths.  Each path is converted to
    a ``ResultItem`` via ``ResultItem.from_path`` and the resulting JSON
    payload is written to ``stdout``.

    Args:
        argv: Unused command-line arguments; reserved for future use.

    Returns:
        Exit code ``0`` on success.
    """
    data = os.getenv("RECENT_FILES", "")

    items: list[ResultItem] = []
    for line in data.split(","):
        stripped = line.strip()
        if not stripped:
            continue
        fp = Path(stripped)
        item = ResultItem.from_path(fp)
        items.append(item)

    payload = ScriptFilterPayload(items=items)
    sys.stdout.write(payload.to_json())

    return 0


if __name__ == "__main__":
    main()
