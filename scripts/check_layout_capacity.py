#!/usr/bin/env python3
"""Report style-aware text and grid capacity before poster confirmation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_manifest import analyze_layout_capacity, bullet_fields, section, table_rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = args.manifest.expanduser().resolve()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 2
    metadata = bullet_fields(section(text, "任务信息"))
    rows = [row for row in table_rows(section(text, "学习内容")) if len(row) >= 6]
    result = analyze_layout_capacity(metadata, rows)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{str(result['level']).upper()}: {path}")
        print(f"DECISION {result['decision']}")
        for key, value in result["metrics"].items():
            print(f"METRIC {key}={value}")
        for reason in result["reasons"]:
            print(f"REASON {reason}")
        for suggestion in result["suggestions"]:
            print(f"SUGGEST {suggestion}")
    return 1 if result["blocking"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
