#!/usr/bin/env python3
"""Validate generated PNG count, dimensions, and aspect ratio without dependencies."""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError("not a valid PNG with an IHDR header")
    return struct.unpack(">II", header[16:24])


def collect_pngs(inputs: list[Path], recursive: bool) -> list[Path]:
    found: list[Path] = []
    for item in inputs:
        if item.is_file():
            found.append(item)
        elif item.is_dir():
            pattern = "**/*.png" if recursive else "*.png"
            found.extend(item.glob(pattern))
        else:
            raise ValueError(f"path does not exist: {item}")
    return sorted({path.resolve() for path in found})


def parse_ratio(value: str) -> float:
    parts = value.split(":", 1)
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("aspect must use WIDTH:HEIGHT, for example 2:3")
    try:
        width, height = (float(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("aspect values must be numbers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("aspect values must be positive")
    return width / height


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="PNG files or directories")
    parser.add_argument("--width", type=int, help="required pixel width")
    parser.add_argument("--height", type=int, help="required pixel height")
    parser.add_argument("--aspect", type=parse_ratio, help="required ratio such as 2:3")
    parser.add_argument("--tolerance", type=float, default=0.01, help="aspect relative tolerance")
    parser.add_argument("--expected-count", type=int, help="required number of PNG files")
    parser.add_argument("--recursive", action="store_true", help="scan directories recursively")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.width is not None and args.width <= 0:
        raise SystemExit("--width must be positive")
    if args.height is not None and args.height <= 0:
        raise SystemExit("--height must be positive")
    if args.tolerance < 0:
        raise SystemExit("--tolerance cannot be negative")
    if args.expected_count is not None and args.expected_count < 0:
        raise SystemExit("--expected-count cannot be negative")

    try:
        images = collect_pngs(args.paths, args.recursive)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    failures: list[str] = []
    if args.expected_count is not None and len(images) != args.expected_count:
        failures.append(f"expected {args.expected_count} PNG files, found {len(images)}")
    if not images:
        failures.append("no PNG files found")

    for path in images:
        try:
            width, height = png_size(path)
        except (OSError, ValueError) as exc:
            failures.append(f"{path}: {exc}")
            continue
        problems: list[str] = []
        if args.width is not None and width != args.width:
            problems.append(f"width {width} != {args.width}")
        if args.height is not None and height != args.height:
            problems.append(f"height {height} != {args.height}")
        if args.aspect is not None:
            actual = width / height
            relative_error = abs(actual - args.aspect) / args.aspect
            if relative_error > args.tolerance:
                problems.append(
                    f"aspect {width}:{height} differs by {relative_error:.2%} "
                    f"(allowed {args.tolerance:.2%})"
                )
        if problems:
            failures.append(f"{path}: " + "; ".join(problems))
        else:
            print(f"PASS {path} {width}x{height}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"Validated {len(images)} PNG file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
