#!/usr/bin/env python3
import json
import os
import sys
from collections.abc import Sequence

from alfred_results import ScriptFilterPayload
from alfred_results.result_item import ResultItem


def main(argv: Sequence[str] | None = None) -> int:
    """Build and output the Alfred Script Filter payload for user actions.

    Reads the ``USER_ACTIONS`` environment variable, which is expected to
    contain a JSON array of action objects with ``id``, ``set``, and ``name``
    keys.  Each action becomes a ``ResultItem`` whose ``arg`` is the
    JavaScript call to execute the action inside Illustrator.  The resulting
    JSON payload is written to ``stdout``.

    Args:
        argv: Unused command-line arguments; reserved for future use.

    Returns:
        Exit code ``0`` on success.
    """
    data = os.getenv("USER_ACTIONS", "[]")
    try:
        actions = json.loads(data)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Failed to parse USER_ACTIONS: {e}\n")
        actions = []

    items: list[ResultItem] = []
    for line in actions:
        action_id = line["id"]
        action_set = line["set"]
        action_name = line["name"]
        item = ResultItem(
            title=action_name,
            subtitle=action_set,
            uid=action_id,
            arg=f"app.doScript('{action_name}', '{action_set}');",
        )
        items.append(item)

    payload = ScriptFilterPayload(items=items)
    sys.stdout.write(payload.to_json())

    return 0


if __name__ == "__main__":
    main()
