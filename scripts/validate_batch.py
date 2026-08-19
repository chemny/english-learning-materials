#!/usr/bin/env python3
"""Validate every material manifest in a single or batch task directory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_manifest import bullet_fields, validate


def batch_metadata(index_path: Path) -> dict[str, str]:
    if not index_path.exists():
        return {}
    return bullet_fields(index_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_dir", type=Path)
    parser.add_argument("--stage", choices=("draft", "confirm", "generate", "delivery"), default="draft")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.task_dir.expanduser().resolve()
    manifests = sorted(root.rglob("material-manifest.md")) if root.exists() else []
    errors: list[str] = []
    if not manifests:
        errors.append(f"no material-manifest.md found under {root}")

    results = [validate(path, args.stage) for path in manifests]
    if any(result["status"] != "ok" for result in results):
        errors.append("one or more manifests failed validation")

    index_path = root / "batch-index.md"
    if len(manifests) > 1:
        metadata = batch_metadata(index_path)
        if not metadata:
            errors.append("batch-index.md is required for multiple manifests")
        else:
            declared = metadata.get("总任务数", "")
            match = re.fullmatch(r"\d+", declared)
            if not match or int(declared) != len(manifests):
                errors.append(f"总任务数 does not match manifest count: {declared!r} vs {len(manifests)}")
            if metadata.get("生成模式") != "纯生图":
                errors.append("batch generation mode must be 纯生图")
            if args.stage in {"generate", "delivery"} and metadata.get("批量确认") != "已确认":
                errors.append("批量确认 must be 已确认 before batch generation")

    payload = {
        "task_dir": str(root),
        "stage": args.stage,
        "status": "ok" if not errors else "error",
        "manifest_count": len(manifests),
        "errors": errors,
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"{payload['status'].upper()}: {root} ({args.stage})")
        print(f"Manifests: {len(manifests)}")
        for message in errors:
            print(f"ERROR: {message}")
        for result in results:
            print(f"- {result['status'].upper()}: {result['path']}")
            for message in result["errors"]:
                print(f"  ERROR: {message}")
            for message in result["warnings"]:
                print(f"  WARNING: {message}")
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
