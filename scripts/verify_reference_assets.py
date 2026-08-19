#!/usr/bin/env python3
"""Verify bundled style-reference files against their portable asset manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    manifest_path = root / "assets/style-references/asset-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    checked: list[str] = []
    active_styles: set[str] = set()
    for item in manifest.get("assets", []):
        relative = item["path"]
        path = root / relative
        if not path.is_file():
            errors.append(f"missing asset: {relative}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            errors.append(f"sha256 mismatch: {relative}")
        checked.append(relative)
        if item.get("role") == "active":
            style_id = item["style_id"]
            if style_id in active_styles:
                errors.append(f"duplicate active asset: {style_id}")
            active_styles.add(style_id)
    payload = {
        "status": "error" if errors else "ok",
        "checked": checked,
        "active_styles": sorted(active_styles),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload["status"].upper())
        for error in errors:
            print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
