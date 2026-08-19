#!/usr/bin/env python3
"""Create a non-destructive task workspace for English learning materials."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from content_contract import (
    CONTENT_CONTRACT_VERSION,
    FORBIDDEN_MODULES,
    MANIFEST_SCHEMA_VERSION,
    MODULE_STRING,
    SKILL_VERSION,
    UNIT_POSTER,
    VOCABULARY_POSTER,
)


STYLE_PRESETS = {
    "primary-handdrawn-poster-v1": "手绘童趣",
    "campus-magazine-v1": "校园杂志风",
    "modern-study-journal-v1": "现代学习手账风",
    "youth-comic-poster-v1": "少年漫画海报风",
}


def resolve_style(style_id: str) -> tuple[str, str, str]:
    style_name = STYLE_PRESETS[style_id]
    skill_root = Path(__file__).resolve().parent.parent
    asset_manifest = skill_root / "assets/style-references/asset-manifest.json"
    relative_reference = ""
    expected_digest = ""
    if asset_manifest.is_file():
        data = json.loads(asset_manifest.read_text(encoding="utf-8"))
        active_item = next(
            (
                item
                for item in data.get("assets", [])
                if item.get("style_id") == style_id and item.get("role") == "active"
            ),
            None,
        )
        if active_item:
            relative_reference = active_item["path"]
            expected_digest = active_item["sha256"]
    reference_path = skill_root / relative_reference
    digest_matches = (
        reference_path.is_file()
        and hashlib.sha256(reference_path.read_bytes()).hexdigest() == expected_digest
    )
    if digest_matches:
        return style_name, "文字视觉 DNA + 参考图增强", relative_reference
    return style_name, "文字视觉 DNA", "无"


def safe_slug(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", value):
        raise argparse.ArgumentTypeError(
            "slug must use 1-64 ASCII letters, digits, dots, underscores, or hyphens"
        )
    if value in {".", ".."}:
        raise argparse.ArgumentTypeError("slug cannot be . or ..")
    return value


def unit_slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized[:40] or "unit"


def manifest_text(unit: str, scale: str, style_id: str, material_type: str) -> str:
    style_name, style_mode, style_reference = resolve_style(style_id)
    is_unit = material_type == UNIT_POSTER
    content_scope = (
        "教材标题 + 核心词汇 + 核心句型 + 知识提示"
        if is_unit else "教材标题 + 核心词汇"
    )
    sentence_state = "展示" if is_unit else "不展示"
    tip_state = "展示" if is_unit else "不展示"
    sentence_content = "待填写" if is_unit else "不适用"
    tip_content = "待填写" if is_unit else "不适用"
    supporting_count = "待计算" if is_unit else "0"
    sentence_candidate_row = (
        "| 1 | 待填写 | 待填写 | 待计算 | 待填写 | 待填写 |" if is_unit else ""
    )
    tip_candidate_row = (
        "| 1 | 待填写 | 待填写 | 待计算 | 待填写 | 待填写 |" if is_unit else ""
    )
    supporting_content_rows = (
        "| 2 | 核心句型区 | 句型 | 待填写 | 待填写 | 不适用 | 待填写 | 待填写 | 待填写 |\n"
        "| 3 | 知识提示区 | 知识提示 | 待填写 | 待填写 | 不适用 | 待填写 | 待填写 | 待填写 |"
        if is_unit else ""
    )
    return f"""# 英语学习资料任务清单

## 任务信息

- 清单版本：{MANIFEST_SCHEMA_VERSION}
- Skill版本：{SKILL_VERSION}
- 内容契约版本：{CONTENT_CONTRACT_VERSION}
- 资料类型：{material_type}
- 内容范围：{content_scope}
- 主体模块：{MODULE_STRING[material_type]}
- 额外学习模块：禁止
- 词汇数量档位：待计算
- 词汇网格：待计算
- 句型组数：{supporting_count}
- 知识提示组数：{supporting_count}
- 生成规模：{scale}
- 生成模式：纯生图
- 出版社：待填写
- 教材名称：待填写
- 版本或年份：待填写
- 版本策略：当前最新适用版本
- 版本检索日期：待填写
- 最新版本核验：未核验
- 版本差异说明：待填写
- 年级册次：待填写
- 学习者年龄段：待填写
- 年龄适配方式：根据年级自动推断
- 单元：{unit}
- 单元标题：待填写
- 主标题：待填写
- 副标题：待填写
- 视觉风格：{style_name}
- 风格编号：{style_id}
- 风格生成方式：{style_mode}
- 风格参考图：{style_reference}
- 版式骨架：standard-grid
- 容量处理：自动适配版式
- 图片尺寸：竖版 3:4
- 教材确认：未确认
- 内容确认：未确认
- 知识提示语言：中文功能 + 英文核心句式

## 来源证据

| 来源标题 | URL或文件位置 | 支持内容 | 证据级别 |
|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 待填写 |

## 词汇候选池

| 教材顺序 | 英文 | 中文 | 内容类型 | 重要性等级 | 是否入选 | 选择说明 | 来源位置 |
|---:|---|---|---|---:|---|---|---|
| 1 | 待填写 | 待填写 | 词汇 | 1 | 待计算 | 待计算 | 待填写 |

## 句型候选池

| 教材顺序 | 英文 | 中文 | 是否入选 | 使用场景 | 来源位置 |
|---:|---|---|---|---|---|
{sentence_candidate_row}

## 知识提示候选池

| 教材顺序 | 中文学习功能 | 英文核心句式 | 是否入选 | 使用场景 | 来源位置 |
|---:|---|---|---|---|---|
{tip_candidate_row}

## 学习内容

| 编号 | 成品区域 | 内容类型 | 英文可见文字 | 中文可见文字 | 音标或词性 | 配图或呈现方式 | 使用场景或说明 | 来源位置 |
|---:|---|---|---|---|---|---|---|---|
| 1 | 核心词汇区 | 词汇 | 待填写 | 待填写 | 不适用 | 待填写 | 待填写 | 待填写 |
{supporting_content_rows}

## 主体模块锁定

| 序号 | 模块 | 状态 | 允许内容 |
|---:|---|---|---|
| 1 | 核心词汇 | 必须展示 | 已入选词汇、教材义和对应配图 |
{('| 2 | 核心句型 | 必须展示 | 已入选核心问答或句型 |' + chr(10) + '| 3 | 知识提示 | 必须展示 | 已入选中文学习功能和英文核心句式 |') if is_unit else ''}

- 禁止模块：{'、'.join(FORBIDDEN_MODULES)}

## 成品分区确认

| 区域 | 状态 | 已确认内容 | 版式责任 |
|---|---|---|---|
| 标题区 | 展示 | 待填写 | 教材、年级册次和资料主标题 |
| 单元主题区 | 展示 | 待填写 | 单元编号和中英文主题 |
| 核心词汇区 | 展示 | 待填写 | 词汇、释义与配图一一对应 |
| 核心句型区 | {sentence_state} | {sentence_content} | 核心问答或句型串联 |
| 知识提示区 | {tip_state} | {tip_content} | 中文学习功能与英文核心句式 |
| 视觉信息区 | 展示 | 待填写 | 年龄、人物、场景、风格与信息密度 |

- 页面拆分：单页；如内容超出可读密度则重新确认

## 唯一可见文字白名单

- 待填写

## 视觉与版式

- 标题区：待填写
- 内容区：待填写
- 句型区：待填写
- 知识提示区：待填写
- 装饰元素：待填写
- 参考图角色：无 / 风格参考

## 生图约束

- 只允许出现白名单中的可见文字。
- 学习内容、中文说明和配图必须一一对应。
- 不得重复、漏写、改写或增加文字。
- 不得添加水印、品牌标识或无关口号。
- 配图语义是不可见指令，不得作为词卡标签、注释或正文显示。

## 验收记录

- 清单校验：未执行
- 图片数量：待填写
- 文字检查：未执行
- 配图检查：未执行
- 整组一致性：不适用
- 已知限制：无
"""


def batch_index_text(units: list[str], style_id: str) -> str:
    style_name, style_mode, style_reference = resolve_style(style_id)
    rows = []
    for index, unit in enumerate(units, start=1):
        folder = f"{index:02d}-{unit_slug(unit)}"
        rows.append(f"| {index} | {folder} | {unit} | 草稿 | 未生成 |")
    return f"""# 批量任务索引

- 生成模式：纯生图
- 总任务数：{len(units)}
- 整组风格：{style_name}
- 风格生成方式：{style_mode}
- 风格参考图：{style_reference}
- 批量确认：未确认

| 编号 | 任务目录 | 教材与单元 | 清单状态 | 图片状态 |
|---:|---|---|---|---|
{chr(10).join(rows)}
"""


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def build_job(
    output: Path,
    slug: str,
    units: list[str],
    force: bool,
    style_id: str,
    material_type: str,
) -> list[Path]:
    root = output.expanduser().resolve() / slug
    planned = []
    if len(units) == 1:
        planned.append(root / "material-manifest.md")
    else:
        planned.append(root / "batch-index.md")
        for index, unit in enumerate(units, start=1):
            planned.append(root / f"{index:02d}-{unit_slug(unit)}" / "material-manifest.md")

    conflicts = [path for path in planned if path.exists()]
    if conflicts and not force:
        joined = "\n".join(str(path) for path in conflicts)
        raise FileExistsError(f"refusing to overwrite existing files:\n{joined}")

    if len(units) == 1:
        write_text(planned[0], manifest_text(units[0], "单张", style_id, material_type), force)
    else:
        write_text(planned[0], batch_index_text(units, style_id), force)
        for path, unit in zip(planned[1:], units):
            write_text(path, manifest_text(unit, "批量", style_id, material_type), force)
    return planned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="parent output directory")
    parser.add_argument("--slug", required=True, type=safe_slug, help="task folder name")
    parser.add_argument("--units", required=True, nargs="+", help="one or more unit labels")
    parser.add_argument(
        "--style-id",
        choices=sorted(STYLE_PRESETS),
        default="primary-handdrawn-poster-v1",
        help="built-in visual style; reference image is selected automatically when present",
    )
    parser.add_argument(
        "--material-type",
        choices=(VOCABULARY_POSTER, UNIT_POSTER),
        default=UNIT_POSTER,
        help="poster content contract; default is the three-module unit review poster",
    )
    parser.add_argument("--force", action="store_true", help="overwrite only managed files")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    try:
        files = build_job(
            args.output,
            args.slug,
            args.units,
            args.force,
            args.style_id,
            args.material_type,
        )
    except (FileExistsError, OSError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"ERROR: {exc}")
        return 1

    payload = {"status": "ok", "mode": "single" if len(args.units) == 1 else "batch", "files": [str(path) for path in files]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Created {len(files)} file(s):")
        for path in files:
            print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
