#!/usr/bin/env python3
"""Compile first-pass image safeguards and score generation-package readiness."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEXT_SURFACE_RE = re.compile(
    r"姓名|学生证|证件|卡片|名片|门牌|班级牌|黑板|白板|书|页面|论坛|帖子|屏幕|电脑|手机|资料|信息|档案|界面|地图|路牌|标牌|标签|日历|旗|包装|报纸|表格|"
    r"\b(?:name|id|card|sign|board|book|page|forum|post|screen|computer|phone|profile|information|interface|map|label|calendar|flag|package)\b",
    flags=re.IGNORECASE,
)
NUMERIC_SURFACE_RE = re.compile(
    r"数字|年龄|年级|日期|时间|时钟|钟表|日历|门牌|"
    r"\b(?:number|age|grade|date|time|clock|calendar)\b",
    flags=re.IGNORECASE,
)
BRAND_SURFACE_RE = re.compile(
    r"商标|品牌|包装|旗帜|国旗|徽标|"
    r"\b(?:brand|logo|package|flag)\b",
    flags=re.IGNORECASE,
)


def runtime_canvas_lock(size_spec: str) -> tuple[str, str]:
    """Resolve a design-oriented size description to one exact built-in canvas."""
    compact = re.sub(r"\s+", "", size_spec).lower()
    explicit = re.search(r"(?<!\d)(\d{3,4})[x×*](\d{3,4})(?!\d)", compact)
    if explicit:
        width, height = int(explicit.group(1)), int(explicit.group(2))
        pixels = f"{width}×{height}"
        if width == height:
            orientation = "square"
        elif width > height:
            orientation = "landscape"
        else:
            orientation = "portrait"
    elif "横" in compact or "landscape" in compact:
        pixels, orientation = "1536×1024", "landscape 3:2"
    elif "正方" in compact or "square" in compact or "1:1" in compact:
        pixels, orientation = "1024×1024", "square 1:1"
    else:
        pixels, orientation = "1024×1536", "portrait 2:3"
    block = (
        f"Runtime canvas: exactly {pixels} pixels, {orientation}. This is the resolved execution canvas for the "
        f"current built-in image runtime. Treat the manifest value “{size_spec}” as design intent only. Do not ask "
        "the image model to choose between ratios, do not generate an unsupported intermediate ratio, and do not "
        "plan a second generation merely to correct dimensions. Preserve all content by composing directly for this canvas."
    )
    return pixels, block


def material_type_style_lock(material_type: str) -> str:
    """Return a module-aware style override that removes cross-type prompt conflicts."""
    if material_type == "词汇复习海报":
        return (
            "Material type: vocabulary-review poster. Render exactly one learning module: 核心词汇. Preserve the "
            "selected style's medium, palette, title hierarchy, grid topology and decorative rhythm, but ignore any "
            "style-protocol or reference-image sentence-pattern panel, learning-tip panel, grammar box, review-language "
            "box or instructional footer. Extend the confirmed vocabulary grid through the available content area and "
            "use only a non-text decorative footer if needed."
        )
    if material_type == "单元复习海报":
        return (
            "Material type: unit-review poster. Render exactly the three confirmed learning modules: 核心词汇、核心句型、"
            "知识提示. Preserve the selected style's medium and layout identity, and do not add any fourth learning module."
        )
    raise ValueError(f"unsupported material type: {material_type or '<empty>'}")


def visual_risk_guard(visual_instruction: str, usage: str = "") -> str:
    """Add concrete no-text/no-number guards for illustrations that naturally invite labels."""
    combined = f"{visual_instruction} {usage}"
    guards: list[str] = []
    if TEXT_SURFACE_RE.search(combined):
        guards.append(
            "render all text-bearing surfaces as blank or abstract shapes with empty lines and unlabeled icons; "
            "do not invent names, letters, words, captions or interface copy"
        )
    if NUMERIC_SURFACE_RE.search(combined):
        guards.append("do not invent digits, ages, grades, dates, times or class numbers")
    if BRAND_SURFACE_RE.search(combined):
        guards.append("do not invent logos, brands, flag text or packaging text")
    if not guards:
        return ""
    return " TEXT-RISK GUARD: " + "; ".join(guards) + "."


def sanitize_visual_instruction(visual_instruction: str, usage: str = "") -> str:
    """Replace risky positive semantics with text-free positive visual evidence."""
    subject = visual_instruction
    if re.search(r"生日|年龄", subject) and NUMERIC_SURFACE_RE.search(subject):
        return "无任何数字或数字形蜡烛的生日蛋糕，只画几支普通未编号蜡烛"
    if re.search(r"年级", subject) and NUMERIC_SURFACE_RE.search(subject):
        return "无任何数字、字母或标签的抽象校园等级徽章，配合叠放课本表达学习阶段"
    if re.search(r"学生证|证件|姓名卡|名片|姓名|个人资料卡", subject):
        return "空白抽象学生资料卡，只保留头像轮廓、纯色色块和空白横线，不出现姓名、字母或数字"
    if re.search(r"页面|翻开|书本|资料页面", subject):
        return "翻开的空白页面或资料册，只保留纸张轮廓和极少抽象空白线，不出现文字或数字"
    if re.search(r"论坛|帖子|界面|屏幕|电脑|手机", subject):
        return "无文字的抽象数字界面，只使用头像圆形、纯色色块、空白横线和未标注图标"
    if re.search(r"教室门牌|班级牌|门牌|路牌|标牌", subject):
        return "无文字、无字母、无数字的场景与空白标牌"
    if re.search(r"地图|定位", subject):
        return "无地名、无文字、无数字的抽象地图轮廓与定位图标"
    return visual_instruction


VISIBLE_OCCURRENCE_LOCK = (
    "Each numbered learning item must appear exactly once in its confirmed card: one number badge, one approved English "
    "entry and one approved Chinese meaning. Do not repeat a whitelist item as decoration or inside an illustration. "
    "Header and module labels must appear only in their confirmed placements. The whitelist is an allowed-and-required "
    "text set, not permission to create duplicate copies, alternate combined titles or extra captions."
)


FIRST_PASS_EXECUTION_LOCK = (
    "Generate exactly one initial image from this package. Do not proactively create drafts, alternatives, comparison "
    "versions or style variants. The first image is the intended final. A second image is permitted only after the first "
    "has a recorded hard acceptance failure such as missing or incorrect required text, wrong module count, unresolved "
    "extra text, wrong runtime dimensions or clear age mismatch. Make at most one targeted retry and never generate a "
    "third image without explicit user approval. Copying or renaming one generated file is not a generation call and must "
    "not be recorded as a retry."
)


def score_generation_package(text: str) -> dict[str, object]:
    """Score prevention of known first-pass failure classes on a 100-point scale."""
    components: dict[str, dict[str, object]] = {}

    exact_canvas = "### Runtime canvas lock" in text and bool(
        re.search(r"exactly \d{3,4}×\d{3,4} pixels", text)
    )
    components["runtime_canvas"] = {
        "score": 20 if exact_canvas else (8 if "版式与尺寸" in text else 0),
        "max": 20,
        "pass": exact_canvas,
    }

    module_lock = "### Material-type style lock" in text and (
        "Render exactly one learning module" in text or "Render exactly the three confirmed learning modules" in text
    )
    components["module_style_consistency"] = {
        "score": 20 if module_lock else (8 if "## EXACT MODULES" in text else 0),
        "max": 20,
        "pass": module_lock,
    }

    mapping_lines = [line for line in text.splitlines() if line.startswith("- ITEM ")]
    risky_lines = [line for line in mapping_lines if TEXT_SURFACE_RE.search(line) or NUMERIC_SURFACE_RE.search(line) or BRAND_SURFACE_RE.search(line)]
    guarded_lines = [line for line in risky_lines if "TEXT-RISK GUARD:" in line]
    if risky_lines:
        text_risk_score = round(20 * len(guarded_lines) / len(risky_lines))
        if not guarded_lines and "NEVER RENDER AS TEXT" in text:
            text_risk_score = 8
    else:
        text_risk_score = 20
    components["illustration_text_safety"] = {
        "score": text_risk_score,
        "max": 20,
        "pass": len(guarded_lines) == len(risky_lines),
        "risky_items": len(risky_lines),
        "guarded_items": len(guarded_lines),
    }

    age_lock = "### Age adaptation lock" in text and "not age assignments" in text
    components["age_consistency"] = {
        "score": 15 if age_lock else (5 if "学习者：" in text else 0),
        "max": 15,
        "pass": age_lock,
    }

    placement_lock = "### Region-bound visible-text placement plan" in text
    alias_lock = "### Semantic alias zero-lock" in text
    occurrence_lock = (
        "### Visible-text occurrence lock" in text
        and "exactly once" in text
        and placement_lock
        and alias_lock
    )
    components["visible_text_determinism"] = {
        "score": 15 if occurrence_lock else (7 if "## VISIBLE TEXT" in text else 0),
        "max": 15,
        "pass": occurrence_lock,
    }

    economy_lock = "### First-pass execution lock" in text and "exactly one initial image" in text
    components["execution_economy"] = {
        "score": 10 if economy_lock else 0,
        "max": 10,
        "pass": economy_lock,
    }

    total = sum(int(item["score"]) for item in components.values())
    return {
        "total": total,
        "max": 100,
        "ready": total >= 90 and all(bool(item["pass"]) for item in components.values()),
        "components": components,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-score", type=int, default=90)
    args = parser.parse_args()
    text = args.package.expanduser().resolve().read_text(encoding="utf-8")
    result = score_generation_package(text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"GENERATION_READINESS {result['total']}/{result['max']} ready={result['ready']}")
        for name, item in result["components"].items():
            print(f"{name}: {item['score']}/{item['max']} pass={item['pass']}")
    return 0 if bool(result["ready"]) and int(result["total"]) >= args.min_score else 1


if __name__ == "__main__":
    raise SystemExit(main())
