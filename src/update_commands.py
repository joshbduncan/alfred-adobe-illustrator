#!/usr/bin/env python3
import csv
import json
from io import TextIOWrapper
from pathlib import Path
from urllib.request import urlopen


def create_items_from_csv(url: str, item_type: str) -> list[dict[str, str]]:
    """Fetch a remote CSV and convert each row into a command dict.

    The CSV is expected to contain at minimum the columns ``value``, ``en``,
    ``id``, and optionally ``minVersion`` / ``maxVersion``.  Depending on
    ``item_type``, the generated ``arg`` value calls either
    ``app.executeMenuCommand`` (for menu commands) or ``app.selectTool``
    (for tool commands).

    Args:
        url: The URL of the remote CSV file to download.
        item_type: Either ``"menu"`` or ``"tool"`` (case-insensitive),
            determining which JavaScript call is used for the ``arg`` field.

    Returns:
        A list of dicts with keys ``title``, ``subtitle``, ``uid``, ``arg``,
        ``item_type``, ``min_version``, and ``max_version``.
    """
    items: list[dict[str, str]] = []
    is_menu = item_type.lower() == "menu"

    with urlopen(url) as response:
        reader = csv.DictReader(TextIOWrapper(response, encoding="utf-8"))

        for row in reader:
            val = row["value"]
            title = row["en"]
            uid = row["id"]
            arg = (
                f"app.executeMenuCommand('{val}')"
                if is_menu
                else f"app.selectTool('{val}')"
            )
            subtitle = "Menu Command" if is_menu else "Tool Command"
            min_version = row.get("minVersion", "")
            max_version = row.get("maxVersion", "")
            items.append(
                {
                    "title": title,
                    "subtitle": subtitle,
                    "uid": uid,
                    "arg": arg,
                    "item_type": item_type,
                    "min_version": min_version,
                    "max_version": max_version,
                }
            )

    return items


def main() -> None:
    """Download the latest menu and tool commands and write them to ``commands.json``.

    Fetches two remote CSVs (menu commands and tool commands) from the
    AiCommandPalette repository, merges the results, and serialises them as
    JSON to ``commands.json`` in the same directory as this script.
    """
    menu_commands_url = (
        "https://raw.githubusercontent.com/joshbduncan/"
        "AiCommandPalette/main/data/menu_commands.csv"
    )
    tool_commands_url = (
        "https://raw.githubusercontent.com/joshbduncan/"
        "AiCommandPalette/main/data/tool_commands.csv"
    )

    results: list[dict[str, str]] = []
    results.extend(create_items_from_csv(menu_commands_url, "menu"))
    results.extend(create_items_from_csv(tool_commands_url, "tool"))

    fp = Path(__file__).resolve().parent / "commands.json"

    with fp.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
