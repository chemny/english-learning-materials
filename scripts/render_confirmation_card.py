#!/usr/bin/env python3
"""Render a poster-shaped confirmation card from a structured manifest."""

from __future__ import annotations

import argparse
from pathlib import Path

from validate_manifest import PLACEHOLDERS, analyze_layout_capacity, bullet_fields, section, table_rows, validate


def clean(value: str) -> str:
    return value if value else "不适用"


def render(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    metadata = bullet_fields(section(text, "任务信息"))
    if metadata.get("清单版本") != "4":
        raise ValueError("confirmation cards for new posters require 清单版本 4")
    validation = validate(path, "confirm")
    if validation["status"] != "ok":
        raise ValueError("manifest is not ready for confirmation: " + "; ".join(validation["errors"]))

    required = (
        "资料类型",
        "内容范围",
        "出版社",
        "教材名称",
        "版本或年份",
        "年级册次",
        "单元",
        "单元标题",
        "主标题",
        "副标题",
        "学习者年龄段",
        "年龄适配方式",
        "视觉风格",
        "风格编号",
        "风格生成方式",
        "风格参考图",
        "版式骨架",
        "图片尺寸",
    )
    required += (
        "版本策略",
        "版本检索日期",
        "最新版本核验",
        "版本差异说明",
        "主体模块",
        "词汇数量档位",
        "词汇网格",
        "句型组数",
        "知识提示组数",
    )
    missing = [key for key in required if metadata.get(key, "") in PLACEHOLDERS]
    if missing:
        raise ValueError(f"confirmation card fields are not ready: {', '.join(missing)}")

    content_rows = [row for row in table_rows(section(text, "学习内容")) if len(row) >= 9]
    if not content_rows or any(cell in PLACEHOLDERS for row in content_rows for cell in row[:9]):
        raise ValueError("learning content is incomplete; fill every version 2 content field first")

    region_rows = [row for row in table_rows(section(text, "成品分区确认")) if len(row) >= 4]
    if not region_rows or any(cell in PLACEHOLDERS for row in region_rows for cell in row[:4]):
        raise ValueError("product-region confirmation is incomplete")
    split_plan = bullet_fields(section(text, "成品分区确认")).get("页面拆分", "")
    if split_plan in PLACEHOLDERS:
        raise ValueError("页面拆分 is not ready")

    by_type: dict[str, list[list[str]]] = {}
    for row in content_rows:
        by_type.setdefault(row[2], []).append(row)
    capacity = analyze_layout_capacity(metadata, content_rows)

    lines = [
        "# 最终成品内容确认卡",
        "",
        "## 教材与标题",
        "",
        f"- 教材：{metadata['出版社']}《{metadata['教材名称']}》",
        f"- 版本：{metadata['版本或年份']}",
        f"- 版本策略：{metadata.get('版本策略', '历史清单未记录')}",
        f"- 版本检索：{metadata.get('版本检索日期', '历史清单未记录')}；{metadata.get('最新版本核验', '历史清单未记录')}",
        f"- 版本差异：{metadata.get('版本差异说明', '历史清单未记录')}",
        f"- 年级册次：{metadata['年级册次']}",
        f"- 单元：{metadata['单元']} {metadata['单元标题']}",
        f"- 主标题：{metadata['主标题']}",
        f"- 副标题：{metadata['副标题']}",
        f"- 资料类型：{metadata['资料类型']}",
        f"- 内容范围：{metadata['内容范围']}",
        f"- EXACT MODULES：{metadata['主体模块']}",
        f"- 数量锁定：词汇 {metadata['词汇数量档位']} 项（{metadata['词汇网格']}）；句型 {metadata['句型组数']} 组；知识提示 {metadata['知识提示组数']} 组",
        "- 额外学习模块：禁止",
        f"- 知识提示语言：{metadata.get('知识提示语言', '历史清单未记录')}",
    ]

    vocabulary = by_type.get("词汇", []) + by_type.get("短语", [])
    if vocabulary:
        lines.extend(
            [
                "",
                "## 核心词汇与配图",
                "",
                "| 英文 | 音标或词性 | 中文 | 配图语义 |",
                "|---|---|---|---|",
            ]
        )
        for row in vocabulary:
            lines.append(f"| {clean(row[3])} | {clean(row[5])} | {clean(row[4])} | {clean(row[6])} |")

    sentences = by_type.get("句型", [])
    if sentences:
        lines.extend(
            [
                "",
                "## 核心句型",
                "",
                "| 英文 | 中文 | 使用场景 | 呈现方式 |",
                "|---|---|---|---|",
            ]
        )
        for row in sentences:
            lines.append(f"| {clean(row[3])} | {clean(row[4])} | {clean(row[7])} | {clean(row[6])} |")

    knowledge = by_type.get("知识提示", []) + by_type.get("语法", [])
    if knowledge:
        lines.extend(
            [
                "",
                "## 知识提示",
                "",
                "| 中文学习功能 | 英文核心句式或语法结构 | 说明 | 呈现方式 |",
                "|---|---|---|---|",
            ]
        )
        for row in knowledge:
            lines.append(f"| {clean(row[4])} | {clean(row[3])} | {clean(row[7])} | {clean(row[6])} |")

    lines.extend(
        [
            "",
            "## 成品分区",
            "",
            "| 区域 | 状态 | 已确认内容 | 版式责任 |",
            "|---|---|---|---|",
        ]
    )
    for row in region_rows:
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
    lines.extend(
        [
            "",
            f"- 页面拆分：{split_plan}",
            "",
            "## 视觉方案",
            "",
            f"- 学习者：{metadata['学习者年龄段']}（{metadata['年龄适配方式']}）",
            f"- 风格：{metadata['视觉风格']}（`{metadata['风格编号']}`）",
            f"- 风格生成：{metadata['风格生成方式']}；参考图：{metadata['风格参考图']}",
            f"- 版式：{metadata['版式骨架']}；尺寸：{metadata['图片尺寸']}",
            f"- 容量预检：{capacity['level']}；处理方式：{capacity['decision']}；词汇 {capacity['metrics']['vocabulary_count']} 项；句型 {capacity['metrics']['sentence_count']} 条；知识提示 {capacity['metrics']['knowledge_count']} 组",
            *[f"- 容量提醒：{reason}" for reason in capacity["reasons"]],
            "",
            "请确认以上文字、配图语义、成品分区、页面数量、风格与年龄适配。确认后，生图阶段不得临时增加或改写可见内容。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, help="optional Markdown output path")
    args = parser.parse_args()

    try:
        card = render(args.manifest.expanduser().resolve())
        if args.output:
            target = args.output.expanduser().resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(card, encoding="utf-8")
            print(target)
        else:
            print(card, end="")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
