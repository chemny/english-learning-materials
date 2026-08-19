#!/usr/bin/env python3
"""Build a deterministic, read-only image-generation package from a manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from age_profiles import age_prompt_block
from content_contract import EXACT_MODULES, FORBIDDEN_MODULES
from generation_preflight import (
    FIRST_PASS_EXECUTION_LOCK,
    ILLUSTRATION_SURFACE_LOCK,
    VISIBLE_OCCURRENCE_LOCK,
    material_type_style_lock,
    runtime_canvas_lock,
    sanitize_visual_instruction,
    visual_risk_guard,
)

from validate_manifest import (
    analyze_layout_capacity,
    bullet_fields,
    section,
    table_rows,
    validate,
    visible_fragments,
    whitelist_items,
)


STYLE_PROTOCOLS = {
    "primary-handdrawn-poster-v1": "references/style-primary-handdrawn-v1.md",
    "campus-magazine-v1": "references/style-campus-magazine-v1.md",
    "modern-study-journal-v1": "references/style-modern-study-journal-v1.md",
    "youth-comic-poster-v1": "references/style-youth-comic-poster-v1.md",
}


def _normalized_visible_text(value: str) -> str:
    """Normalize spacing and punctuation for semantic title-alias comparison."""
    return re.sub(r"[^0-9a-z\u3400-\u9fff]+", "", value.casefold())


def _confirmed_header_text(region_rows: list[list[str]]) -> list[tuple[str, str]]:
    placements: list[tuple[str, str]] = []
    for row in region_rows:
        if len(row) < 3 or row[0] not in {"标题区", "单元主题区"} or row[1] != "展示":
            continue
        for item in re.split(r"\s*[；;]\s*", row[2]):
            if item and item not in {"无", "不适用"}:
                placements.append((row[0], item))
    return placements


def _confirmed_module_labels(
    region_rows: list[list[str]], whitelist: list[str]
) -> list[tuple[str, str]]:
    """Bind confirmed visible module labels, including user-facing aliases, to their regions."""
    module_regions = {"核心词汇区", "核心句型区", "知识提示区"}
    whitelist_set = set(whitelist)
    placements: list[tuple[str, str]] = []
    for row in region_rows:
        if len(row) < 3 or row[0] not in module_regions or row[1] != "展示":
            continue
        first_item = re.split(r"\s*[；;]\s*", row[2], maxsplit=1)[0].strip()
        if first_item in whitelist_set:
            placements.append((row[0], first_item))
    return placements


def compile_visible_text_plan(
    whitelist: list[str],
    region_rows: list[list[str]],
    content_rows: list[list[str]],
    exact_modules: tuple[str, ...] | list[str],
) -> dict[str, object]:
    """Compile allowed text into region-bound required text and zero-count title aliases."""
    header = _confirmed_header_text(region_rows)
    placements: list[tuple[str, str]] = list(header)
    # A module can be structurally present without a printed label. Prefer the
    # user-facing label confirmed in that region (for example 句子串联), while
    # retaining the exact internal module name as a fallback when it is the
    # confirmed visible label.
    module_labels = _confirmed_module_labels(region_rows, whitelist)
    placements.extend(module_labels)
    placed_module_labels = {value for _region, value in module_labels}
    placements.extend(
        ("主体模块标签", module)
        for module in exact_modules
        if module in whitelist and module not in placed_module_labels
    )
    for row in content_rows:
        if len(row) < 9:
            continue
        region = row[1]
        for value in (row[3], row[4], row[5]):
            placements.extend((region, fragment) for fragment in visible_fragments(value))

    whitelist_set = set(whitelist)
    missing = [value for _region, value in placements if value not in whitelist_set]
    if missing:
        raise ValueError("P01 placement text missing from whitelist: " + ", ".join(dict.fromkeys(missing)))

    placed_values = {value for _region, value in placements}
    extras = [item for item in whitelist if item not in placed_values]
    header_values = [value for _region, value in header]
    normalized_headers = [_normalized_visible_text(value) for value in header_values]
    aliases: list[str] = []
    unresolved: list[str] = []
    for extra in extras:
        normalized_extra = _normalized_visible_text(extra)
        is_alias = any(
            normalized_extra == "".join(normalized_headers[start:end])
            for start in range(len(normalized_headers))
            for end in range(start + 2, len(normalized_headers) + 1)
        )
        (aliases if is_alias else unresolved).append(extra)
    if unresolved:
        raise ValueError(
            "P01 whitelist text has no confirmed region or learning-item placement: " + ", ".join(unresolved)
        )

    counts: dict[str, int] = {}
    for _region, value in placements:
        counts[value] = counts.get(value, 0) + 1
    renderable = list(dict.fromkeys(value for _region, value in placements))
    return {
        "placements": placements,
        "counts": counts,
        "renderable": renderable,
        "zero_count_aliases": aliases,
    }

def core_style_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^## 核心风格提示块\s*$.*?```text\n(.*?)\n```",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"core style prompt block not found: {path}")
    return match.group(1).strip()


def portable_reference(skill_root: Path, stored: str) -> tuple[str, str]:
    if stored in {"", "无", "不适用"}:
        return "文字视觉 DNA", "无"
    candidate = Path(stored).expanduser()
    resolved = candidate if candidate.is_absolute() else skill_root / candidate
    if resolved.is_file():
        return "参考图增强", stored
    return "文字视觉 DNA（参考图不可用，自动回退）", "无"


def reference_asset_digest(skill_root: Path, stored: str) -> str:
    if stored in {"", "无", "不适用"}:
        return "无"
    asset_manifest = skill_root / "assets/style-references/asset-manifest.json"
    if not asset_manifest.is_file():
        return "未登记"
    data = json.loads(asset_manifest.read_text(encoding="utf-8"))
    for item in data.get("assets", []):
        if item.get("path") == stored:
            candidate = skill_root / stored
            actual = hashlib.sha256(candidate.read_bytes()).hexdigest() if candidate.is_file() else "missing"
            if actual != item.get("sha256"):
                raise ValueError(f"reference asset hash mismatch: {stored}")
            return f"sha256:{actual}"
    return "未登记"


def build(manifest: Path, skill_root: Path) -> str:
    result = validate(manifest, "generate")
    if result["status"] != "ok":
        raise ValueError("manifest is not ready for generation: " + "; ".join(result["errors"]))

    text = manifest.read_text(encoding="utf-8")
    metadata = bullet_fields(section(text, "任务信息"))
    visual = bullet_fields(section(text, "视觉与版式"))
    whitelist = whitelist_items(section(text, "唯一可见文字白名单"))
    content_rows = [row for row in table_rows(section(text, "学习内容")) if len(row) >= 9]
    region_rows = table_rows(section(text, "成品分区确认"))
    visible_plan = compile_visible_text_plan(
        whitelist,
        region_rows,
        content_rows,
        EXACT_MODULES[metadata["资料类型"]],
    )
    capacity = analyze_layout_capacity(metadata, content_rows)

    style_id = metadata["风格编号"]
    protocol_relative = STYLE_PROTOCOLS.get(style_id)
    if protocol_relative:
        protocol_path = skill_root / protocol_relative
        style_block = core_style_block(protocol_path)
    else:
        protocol_relative = "无（用户自带参考图）"
        style_block = "Follow the confirmed custom-reference composition and the manifest's visual plan."

    age_block = age_prompt_block(metadata["学习者年龄段"])
    runtime_pixels, runtime_block = runtime_canvas_lock(metadata["图片尺寸"])
    material_style_block = material_type_style_lock(metadata["资料类型"])

    reference_mode, reference_path = portable_reference(skill_root, metadata.get("风格参考图", "无"))
    reference_digest = reference_asset_digest(skill_root, reference_path)

    mappings: list[str] = []
    for row in content_rows:
        number, region, content_type, english, chinese, phonics, visual_instruction, usage, _source = row[:9]
        english_lines = visible_fragments(english)
        visible = [fragment for value in (english, chinese, phonics) for fragment in visible_fragments(value)]
        line_instruction = " Render the English fragments on separate visible lines in this exact order." if len(english_lines) > 1 else ""
        safe_visual_instruction = sanitize_visual_instruction(visual_instruction, usage)
        mappings.append(
            f"- ITEM {number} [{region}/{content_type}]: visually present {', '.join(visible)}; "
            f"illustrate or present it as follows: {safe_visual_instruction}. Context: {usage}. "
            f"This entire instruction is non-visible and must never be printed."
            f"{visual_risk_guard(safe_visual_instruction, usage)}{line_instruction}"
        )

    canonical = {
        "metadata": metadata,
        "visual": visual,
        "whitelist": whitelist,
        "visible_text_plan": visible_plan,
        "content_rows": content_rows,
        "style_protocol": protocol_relative,
        "style_block": style_block,
        "age_block": age_block,
        "runtime_canvas": runtime_pixels,
        "runtime_block": runtime_block,
        "material_style_block": material_style_block,
        "compiled_mappings": mappings,
        "reference_mode": reference_mode,
        "reference_digest": reference_digest,
        "capacity": capacity,
    }
    digest = hashlib.sha256(
        json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    manifest_file_digest = hashlib.sha256(manifest.read_bytes()).hexdigest()

    lines = [
        "# 标准生图任务包",
        "",
        f"- 内容指纹：`sha256:{digest}`",
        f"- 清单文件指纹：`sha256:{manifest_file_digest}`",
        f"- 来源清单：`{manifest.name}`",
        f"- 资料类型：{metadata['资料类型']}",
        f"- 教材：{metadata['出版社']}《{metadata['教材名称']}》 {metadata['年级册次']}；单元编号：{metadata['单元']}；单元标题：{metadata['单元标题']}",
        f"- 学习者：{metadata['学习者年龄段']}（{metadata['年龄适配方式']}）",
        f"- 风格：{metadata['视觉风格']}（`{style_id}`）",
        f"- 风格协议：`{protocol_relative}`",
        f"- 风格输入：{reference_mode}",
        f"- 参考图：{reference_path}",
        f"- 参考图指纹：`{reference_digest}`",
        f"- 版式与尺寸：{metadata['版式骨架']}；{metadata['图片尺寸']}",
        f"- 运行时画布：{runtime_pixels}",
        f"- 容量预检：{capacity['level']}；词汇 {capacity['metrics']['vocabulary_count']} 项；句型 {capacity['metrics']['sentence_count']} 条；知识提示 {capacity['metrics']['knowledge_count']} 组",
        f"- 容量处理：{capacity['decision']}",
        f"- 输出文件名：final-{style_id}.png",
        "- 用途：scientific-educational",
        "- 生成方式：完整位图，纯生图",
        "",
        "## PRIMARY REQUEST",
        "",
        "Create one complete English-learning poster from this locked package. Preserve the confirmed text, semantic mappings, learner age, page architecture and natural aspect ratios. Do not add, translate, paraphrase or omit visible text.",
        "",
        "## EXACT MODULES — RENDER THESE AND ONLY THESE",
        "",
    ]
    lines.extend(f"- {module}" for module in EXACT_MODULES[metadata["资料类型"]])
    lines.extend(
        [
            "",
            "The title and unit information belong to the header, not to a main learning module. Characters, objects and decorations are visual elements, not learning modules.",
            "",
            "## FORBIDDEN MODULES — DO NOT ADD",
            "",
        ]
    )
    lines.extend(f"- {module}" for module in FORBIDDEN_MODULES)
    lines.extend(
        [
            "",
            "No additional titled box, learning panel, exercise, goal, grammar summary or footer learning module is permitted.",
            "",
            "## VISIBLE TEXT — RENDER VERBATIM",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in visible_plan["renderable"])
    lines.extend(
        [
            "",
            "### Region-bound visible-text placement plan",
            "",
        ]
    )
    for region, value in visible_plan["placements"]:
        lines.append(f"- {region}: {value} ×1")
    lines.extend(
        [
            "",
            "### Semantic alias zero-lock",
            "",
        ]
    )
    if visible_plan["zero_count_aliases"]:
        lines.append(
            f"- Detected and removed {len(visible_plan['zero_count_aliases'])} alternate combined header alias(es). "
            "Never concatenate adjacent header entries into an additional title."
        )
    else:
        lines.append("- No alternate combined title aliases detected.")
    lines.extend(
        [
            "",
            "### Visible-text occurrence lock",
            "",
            VISIBLE_OCCURRENCE_LOCK,
            "",
            "## NON-VISIBLE VISUAL INSTRUCTIONS — NEVER RENDER AS TEXT",
            "",
            "### Runtime canvas lock",
            "",
            runtime_block,
            "",
            "### Fixed style DNA",
            "",
            style_block,
            "",
            "### Material-type style lock",
            "",
            material_style_block,
            "",
            "### Age adaptation lock — overrides conflicting character-age cues",
            "",
            age_block,
            "",
            "### Reference-image age boundary",
            "",
            "Use any reference image for the confirmed layout, drawing medium, palette, hierarchy and decoration rhythm. Never copy or inherit reference characters, body proportions, clothing, school-stage props or age-coded decoration when they conflict with the age adaptation lock above.",
            "",
            "### Illustration surface text lock",
            "",
            ILLUSTRATION_SURFACE_LOCK,
            "",
            "### Adaptive layout decision",
            "",
            "Preserve the core style anchors above, but adapt exact region ratios, grid columns, character count and decorative props to the confirmed content load and reference image. Numeric ratios and named props are strong defaults, not mandatory inventory. Related semantic regions may share one visual container when every confirmed item remains clearly identifiable and readable. Never solve density by deleting text, distorting content or shrinking essential text below comfortable reading size.",
            "",
            "### Confirmed page plan",
            "",
        ]
    )
    lines.extend(f"- {key}: {value}" for key, value in visual.items())
    lines.extend(["", "### Content-to-visual mapping", ""])
    lines.extend(mappings)
    lines.extend(
        [
            "",
            "## FORBIDDEN VISIBLE TEXT",
            "",
            "- Any instruction, style term, object description, layout note, source note, filename, path, watermark, brand or slogan not listed in VISIBLE TEXT.",
            "- Do not print metalinguistic translations of Chinese learning functions. English inside the learning-tip module must be the approved reusable sentence frames from VISIBLE TEXT.",
        ]
    )
    lines.extend(
        [
            "",
            "## EXECUTION LOCK",
            "",
            "Use this package as read-only. A sub-agent may append runtime call metadata, but may not change the whitelist, content mapping, style block, age, page count or output target.",
            "",
            "### First-pass execution lock",
            "",
            FIRST_PASS_EXECUTION_LOCK,
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest = args.manifest.expanduser().resolve()
    skill_root = Path(__file__).resolve().parent.parent
    output = args.output.expanduser().resolve() if args.output else manifest.with_name("generation-package.md")
    if output.exists() and not args.force:
        print(f"ERROR: refusing to overwrite existing file: {output}")
        return 1
    try:
        rendered = build(manifest, skill_root)
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_name(f".{output.name}.tmp")
        temporary.write_text(rendered, encoding="utf-8", newline="\n")
        temporary.replace(output)
        print(output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
