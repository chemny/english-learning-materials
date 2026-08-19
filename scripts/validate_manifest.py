#!/usr/bin/env python3
"""Validate an English learning material manifest without external packages."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from content_contract import (
    CONTENT_CONTRACT_VERSION,
    EXACT_MODULES,
    FORBIDDEN_MODULES,
    MANIFEST_SCHEMA_VERSION,
    MODULE_STRING,
    POSTER_TYPES,
    SKILL_VERSION,
    UNIT_POSTER,
    VOCABULARY_GRIDS,
    VOCABULARY_POSTER,
    VOCABULARY_TIERS,
    choose_supporting_count,
    choose_vocabulary_tier,
)


REQUIRED_SECTIONS = (
    "任务信息",
    "来源证据",
    "学习内容",
    "唯一可见文字白名单",
    "视觉与版式",
    "生图约束",
    "验收记录",
)

REQUIRED_METADATA = (
    "资料类型",
    "生成规模",
    "生成模式",
    "出版社",
    "教材名称",
    "版本或年份",
    "年级册次",
    "学习者年龄段",
    "年龄适配方式",
    "单元",
    "单元标题",
    "视觉风格",
    "风格编号",
    "风格生成方式",
    "风格参考图",
    "版式骨架",
    "图片尺寸",
    "教材确认",
    "内容确认",
)

REQUIRED_V2_METADATA = (
    "清单版本",
    "内容范围",
    "主标题",
    "副标题",
)

REQUIRED_V3_METADATA = (
    "版本策略",
    "版本检索日期",
    "最新版本核验",
    "版本差异说明",
)

REQUIRED_V4_METADATA = (
    "Skill版本",
    "内容契约版本",
    "主体模块",
    "额外学习模块",
    "词汇数量档位",
    "词汇网格",
    "句型组数",
    "知识提示组数",
)

REQUIRED_V4_SECTIONS = (
    "词汇候选池",
    "句型候选池",
    "知识提示候选池",
    "主体模块锁定",
)

PLACEHOLDERS = {"", "待填写", "未确认", "未执行", "待确认", "未核验"}
NON_VISIBLE = {"", "不适用", "无"}
AGE_BANDS = {
    "学前（4–6岁）",
    "小学低年级（6–8岁）",
    "小学中年级（8–10岁）",
    "小学高年级（10–12岁）",
    "初中（12–15岁）",
    "高中（15–18岁）",
    "成人（18岁以上）",
}
AGE_MODES = {"根据年级自动推断", "用户指定"}
STYLE_IDS = {
    "primary-handdrawn-poster-v1",
    "campus-magazine-v1",
    "modern-study-journal-v1",
    "youth-comic-poster-v1",
    "custom-reference-v1",
}
LEGACY_STYLE_IDS = {
    "cartoon-classroom-v1": "modern-study-journal-v1",
    "fresh-study-card-v1": "campus-magazine-v1",
}
REGISTERED_STYLE_IDS = STYLE_IDS | set(LEGACY_STYLE_IDS)
STYLE_MODES = {"文字视觉 DNA", "文字视觉 DNA + 参考图增强"}
KNOWLEDGE_LANGUAGE_MODES = {"中文功能 + 英文核心句式", "仅中文（用户已确认）", "中英双语"}
CAPACITY_DECISIONS = {"自动适配版式", "用户确认单页", "拆页"}
META_LANGUAGE_TRANSLATIONS = {
    "make requests",
    "ask about preferences",
    "describe food",
    "express needs",
    "ask about likes",
}
LAYOUT_ARCHETYPES = {"compact-grid", "standard-grid", "large-card-grid", "custom"}
CONTENT_REQUIREMENTS = {
    "词汇复习海报": (("词汇",),),
    "单元复习海报": (("词汇",), ("句型",), ("知识提示", "语法")),
    "句型卡": (("句型",),),
    "语法总结": (("语法", "知识提示"),),
    "练习单": (("练习",),),
    "阅读辅助": (("阅读",),),
}
POSTER_REGIONS = {
    "标题区",
    "单元主题区",
    "核心词汇区",
    "核心句型区",
    "知识提示区",
    "视觉信息区",
}
REGION_STATES = {"展示", "不展示"}
NO_ILLUSTRATION = NON_VISIBLE | {"装饰", "抽象插图", "好看", "待定"}
VERSION_STRATEGIES = {"当前最新适用版本", "用户指定版本"}
VERSION_EVIDENCE_TERMS = ("版本", "版次", "新版", "适用学年", "教学用书目录")

STYLE_CAPACITY = {
    "primary-handdrawn-poster-v1": {"sentence_review": 210, "sentence_split": 300, "tip_review": 75, "tip_split": 120},
    "campus-magazine-v1": {"sentence_review": 200, "sentence_split": 285, "tip_review": 70, "tip_split": 110},
    "modern-study-journal-v1": {"sentence_review": 190, "sentence_split": 270, "tip_review": 70, "tip_split": 110},
    "youth-comic-poster-v1": {"sentence_review": 170, "sentence_split": 240, "tip_review": 60, "tip_split": 95},
}

LAYOUT_VOCAB_CAPACITY = {
    "compact-grid": 25,
    "standard-grid": 20,
    "large-card-grid": 12,
    "custom": 20,
}


def infer_age_band(grade: str) -> str | None:
    normalized = re.sub(r"\s+", "", grade)
    if any(token in normalized for token in ("学前", "幼儿")):
        return "学前（4–6岁）"
    if any(token in normalized for token in ("一年级", "二年级", "1年级", "2年级")):
        return "小学低年级（6–8岁）"
    if any(token in normalized for token in ("三年级", "四年级", "3年级", "4年级")):
        return "小学中年级（8–10岁）"
    if any(token in normalized for token in ("五年级", "六年级", "5年级", "6年级")):
        return "小学高年级（10–12岁）"
    if any(token in normalized for token in ("七年级", "八年级", "九年级", "7年级", "8年级", "9年级", "初一", "初二", "初三", "初中")):
        return "初中（12–15岁）"
    if any(token in normalized for token in ("高一", "高二", "高三", "高中")):
        return "高中（15–18岁）"
    if any(token in normalized for token in ("大学", "成人", "职场", "职业英语")):
        return "成人（18岁以上）"
    return None


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def bullet_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in body.splitlines():
        match = re.match(r"^\s*-\s*([^：:]+)[：:]\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def table_rows(body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def whitelist_items(body: str) -> list[str]:
    return [
        match.group(1).strip()
        for line in body.splitlines()
        if (match := re.match(r"^\s*-\s+(.+?)\s*$", line))
    ]


def visible_fragments(value: str) -> list[str]:
    """Split approved visual line breaks without making the marker visible."""
    if value in NON_VISIBLE:
        return []
    return [part.strip() for part in re.split(r"\s*<br\s*/?>\s*", value, flags=re.IGNORECASE) if part.strip()]


def text_units(value: str) -> float:
    total = 0.0
    for char in re.sub(r"<br\s*/?>", "", value, flags=re.IGNORECASE):
        codepoint = ord(char)
        if 0x3400 <= codepoint <= 0x9FFF:
            total += 1.0
        elif char.isalnum():
            total += 0.55
        elif char.isspace():
            total += 0.2
        else:
            total += 0.3
    return round(total, 1)


def normalized_content_row(row: list[str]) -> tuple[str, str, str] | None:
    if len(row) >= 9:
        return row[2], row[3], row[4]
    if len(row) >= 6:
        return row[1], row[2], row[3]
    return None


def analyze_layout_capacity(metadata: dict[str, str], content_rows: list[list[str]]) -> dict[str, object]:
    """Estimate layout risk without treating heuristic thresholds as objective facts."""
    style_id = metadata.get("风格编号", "")
    layout = metadata.get("版式骨架", "")
    decision = metadata.get("容量处理", "自动适配版式")
    capacity = STYLE_CAPACITY.get(
        style_id,
        {"sentence_review": 190, "sentence_split": 270, "tip_review": 70, "tip_split": 110},
    )
    normalized = [(row, values) for row in content_rows if (values := normalized_content_row(row))]
    vocabulary = [(row, values) for row, values in normalized if values[0] in {"词汇", "短语"}]
    sentences = [(row, values) for row, values in normalized if values[0] == "句型"]
    tips = [(row, values) for row, values in normalized if values[0] in {"知识提示", "语法"}]
    vocabulary_count = len(vocabulary)
    sentence_units = round(sum(text_units(values[1]) + text_units(values[2]) for _row, values in sentences), 1)
    tip_units = round(sum(text_units(values[1]) + text_units(values[2]) for _row, values in tips), 1)
    english_fragments = [fragment for _row, values in normalized for fragment in visible_fragments(values[1])]
    longest_word = max(
        (token for fragment in english_fragments for token in re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", fragment)),
        key=len,
        default="",
    )
    longest_tip_line = max((text_units(fragment) for _row, values in tips for fragment in visible_fragments(values[1])), default=0.0)

    level = "pass"
    blocking = False
    reasons: list[str] = []
    suggestions: list[str] = []

    selected_vocab_capacity = LAYOUT_VOCAB_CAPACITY.get(layout, 20)
    if vocabulary_count > 25:
        level = "split_required"
        blocking = True
        reasons.append(f"词汇或短语共 {vocabulary_count} 项，超过单页最高容量 25 项")
        suggestions.append("拆成两张独立清单并重新通过确认门 B")
    elif vocabulary_count > selected_vocab_capacity:
        level = "review"
        reasons.append(f"{layout} 建议最多 {selected_vocab_capacity} 项，当前为 {vocabulary_count} 项")
        suggestions.append("优先自动调整列数与区域比例；仍拥挤时再改用 compact-grid 或拆页")

    if len(sentences) > 4 or sentence_units > capacity["sentence_split"]:
        level = "split_required"
        blocking = True
        reasons.append(f"核心句型区负载过高：{len(sentences)} 条，约 {sentence_units} 单位")
        suggestions.append("把句型复习拆为独立页面，不缩小字体")
    elif sentence_units > capacity["sentence_review"]:
        if level == "pass":
            level = "review"
        reasons.append(f"核心句型区接近容量上限：{len(sentences)} 条，约 {sentence_units} 单位")
        suggestions.append("确认底部区域可读；必要时扩大句型区或拆页")

    if len(tips) > 4 or tip_units > capacity["tip_split"]:
        level = "split_required"
        blocking = True
        reasons.append(f"知识提示区负载过高：{len(tips)} 组，约 {tip_units} 单位")
        suggestions.append("减少单页提示组数或拆成独立句型卡")
    elif tip_units > capacity["tip_review"]:
        if level == "pass":
            level = "review"
        reasons.append(f"知识提示区接近容量上限：{len(tips)} 组，约 {tip_units} 单位")
        suggestions.append("为英文核心句式保留独立换行，不使用压缩字体")

    if longest_tip_line > 23:
        if level == "pass":
            level = "review"
        reasons.append(f"知识提示最长单行约 {longest_tip_line} 单位")
        suggestions.append("使用 <br> 把问句与答句拆成独立可见行")
    if len(longest_word) > 18:
        if level == "pass":
            level = "review"
        reasons.append(f"最长英文词为 {longest_word}（{len(longest_word)} 个字母）")
        suggestions.append("确认词卡允许按单词边界换行且不压缩字宽")

    if level == "split_required" and decision == "用户确认单页":
        level = "override_confirmed"
        blocking = False
        suggestions.append("保留全部已确认文字，允许自适应列数、合并相关区域并扩大内容区；验收不通过时再拆页")
    elif level == "split_required" and decision == "拆页":
        suggestions.append("当前清单仍是单页负载；完成拆页并为每页建立独立清单后再生成")

    return {
        "level": level,
        "blocking": blocking,
        "style_id": style_id,
        "layout": layout,
        "decision": decision,
        "metrics": {
            "vocabulary_count": vocabulary_count,
            "sentence_count": len(sentences),
            "sentence_units": sentence_units,
            "knowledge_count": len(tips),
            "knowledge_units": tip_units,
            "longest_word": longest_word,
            "longest_tip_line_units": longest_tip_line,
        },
        "reasons": reasons,
        "suggestions": list(dict.fromkeys(suggestions)),
    }


def positive_int(value: str) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def selected_candidate_keys(rows: list[list[str]], kind: str, errors: list[str]) -> tuple[list[tuple[str, str]], int]:
    """Validate a v4 candidate pool and return selected visible-text keys."""
    selected: list[tuple[str, str]] = []
    complete: list[tuple[int, int, str, str, str]] = []
    minimum_cells = 8 if kind == "词汇" else 6
    selection_index = 5 if kind == "词汇" else 3
    for row_index, row in enumerate(rows, start=1):
        if len(row) < minimum_cells or any(cell in PLACEHOLDERS for cell in row[:minimum_cells]):
            errors.append(f"D01 {kind}候选池存在不完整行: {row_index}")
            continue
        order = positive_int(row[0])
        if order is None or order == 0:
            errors.append(f"D01 {kind}候选池教材顺序必须为正整数: {row_index}")
            continue
        english, chinese = (row[1], row[2]) if kind != "知识提示" else (row[2], row[1])
        importance = 1
        if kind == "词汇":
            importance = positive_int(row[4]) or 0
            if importance not in range(1, 6):
                errors.append(f"D01 词汇重要性等级必须为 1-5: {row_index}")
        selected_flag = row[selection_index]
        if selected_flag not in {"是", "否"}:
            errors.append(f"D01 {kind}候选池是否入选只能填写 是 或 否: {row_index}")
        complete.append((importance, order, english, chinese, selected_flag))
        if selected_flag == "是":
            selected.append((english, chinese))

    if kind == "词汇":
        expected_order = sorted(complete, key=lambda item: (item[0], item[1], item[2].casefold()))
    else:
        expected_order = sorted(complete, key=lambda item: (item[1], item[2].casefold()))
    expected_selected_count = len(selected)
    expected_keys = {(item[2], item[3]) for item in expected_order[:expected_selected_count]}
    if set(selected) != expected_keys:
        errors.append(f"D02 {kind}候选池入选项不符合确定性排序规则")
    return selected, len(complete)


def validate_v4_contract(
    text: str,
    metadata: dict[str, str],
    valid_content: list[list[str]],
    region_rows: list[list[str]],
    errors: list[str],
) -> None:
    material_type = metadata.get("资料类型", "")
    if material_type not in POSTER_TYPES:
        errors.append("D00 清单版本 4 仅支持词汇复习海报或单元复习海报")
        return
    if metadata.get("Skill版本") != SKILL_VERSION:
        errors.append(f"D00 Skill版本必须为 {SKILL_VERSION}")
    if metadata.get("内容契约版本") != CONTENT_CONTRACT_VERSION:
        errors.append(f"D00 内容契约版本必须为 {CONTENT_CONTRACT_VERSION}")
    if metadata.get("主体模块") != MODULE_STRING[material_type]:
        errors.append(f"D03 主体模块必须精确等于: {MODULE_STRING[material_type]}")
    if metadata.get("额外学习模块") != "禁止":
        errors.append("D03 额外学习模块必须填写 禁止")

    vocab_selected, vocab_candidates = selected_candidate_keys(
        table_rows(section(text, "词汇候选池")), "词汇", errors
    )
    sentence_selected, sentence_candidates = selected_candidate_keys(
        table_rows(section(text, "句型候选池")), "句型", errors
    )
    tip_selected, tip_candidates = selected_candidate_keys(
        table_rows(section(text, "知识提示候选池")), "知识提示", errors
    )

    tier = positive_int(metadata.get("词汇数量档位", ""))
    expected_tier = choose_vocabulary_tier(vocab_candidates, metadata.get("版式骨架", ""))
    if vocab_candidates < 9:
        errors.append("D04 已核验词汇不足 9 个；不得编造，需补充来源或取得用户例外确认")
    if tier not in VOCABULARY_TIERS:
        errors.append(f"D04 词汇数量档位必须为 {VOCABULARY_TIERS}")
    elif tier != expected_tier:
        errors.append(f"D04 词汇数量档位应按候选数和版式确定为 {expected_tier}，当前为 {tier}")
    if tier and metadata.get("词汇网格") != VOCABULARY_GRIDS[tier]:
        errors.append(f"D04 词汇网格必须为 {VOCABULARY_GRIDS[tier]}")
    if tier is not None and len(vocab_selected) != tier:
        errors.append(f"D04 词汇候选池必须精确入选 {tier} 项，当前为 {len(vocab_selected)}")

    content_keys: dict[str, set[tuple[str, str]]] = {"词汇": set(), "句型": set(), "知识提示": set()}
    for row in valid_content:
        content_type = row[2]
        key = (row[3], row[4])
        if content_type in {"词汇", "短语"}:
            content_keys["词汇"].add(key)
        elif content_type == "句型":
            content_keys["句型"].add(key)
        elif content_type == "知识提示":
            content_keys["知识提示"].add(key)
        else:
            errors.append(f"D03 禁止的学习内容类型: {content_type}")
    if content_keys["词汇"] != set(vocab_selected):
        errors.append("D05 学习内容中的词汇与词汇候选池入选项不一致")

    sentence_count = positive_int(metadata.get("句型组数", ""))
    tip_count = positive_int(metadata.get("知识提示组数", ""))
    if material_type == VOCABULARY_POSTER:
        if sentence_count != 0 or tip_count != 0 or sentence_selected or tip_selected:
            errors.append("D06 词汇复习海报的句型和知识提示数量必须均为 0")
        if content_keys["句型"] or content_keys["知识提示"]:
            errors.append("D06 词汇复习海报只能包含核心词汇模块")
    else:
        expected_sentences = choose_supporting_count(sentence_candidates)
        expected_tips = choose_supporting_count(tip_candidates)
        if expected_sentences is None:
            errors.append("D06 核心句型候选不足 2 组；继续检索，不得省略模块")
        if expected_tips is None:
            errors.append("D06 知识提示候选不足 2 组；继续检索，不得省略模块")
        if sentence_count != expected_sentences or len(sentence_selected) != expected_sentences:
            errors.append(f"D06 核心句型必须精确入选 {expected_sentences} 组")
        if tip_count != expected_tips or len(tip_selected) != expected_tips:
            errors.append(f"D06 知识提示必须精确入选 {expected_tips} 组")
        if content_keys["句型"] != set(sentence_selected):
            errors.append("D05 学习内容中的句型与句型候选池入选项不一致")
        if content_keys["知识提示"] != set(tip_selected):
            errors.append("D05 学习内容中的知识提示与知识提示候选池入选项不一致")

    module_rows = table_rows(section(text, "主体模块锁定"))
    locked_modules = tuple(row[1] for row in module_rows if len(row) >= 4 and row[2] == "必须展示")
    if locked_modules != EXACT_MODULES[material_type]:
        errors.append(f"D03 主体模块锁定必须精确为 {EXACT_MODULES[material_type]}")
    forbidden_line = bullet_fields(section(text, "主体模块锁定")).get("禁止模块", "")
    missing_forbidden = [item for item in FORBIDDEN_MODULES if item not in forbidden_line]
    if missing_forbidden:
        errors.append("D03 禁止模块清单不完整: " + "、".join(missing_forbidden))

    region_states = {row[0]: row[1] for row in region_rows if len(row) >= 2}
    expected_states = {
        "核心句型区": "展示" if material_type == UNIT_POSTER else "不展示",
        "知识提示区": "展示" if material_type == UNIT_POSTER else "不展示",
    }
    for region, state in expected_states.items():
        if region_states.get(region) != state:
            errors.append(f"D03 {material_type}要求 {region}={state}")


def validate(path: Path, stage: str) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"path": str(path), "stage": stage, "status": "error", "errors": [str(exc)], "warnings": []}

    if not text.startswith("# 英语学习资料任务清单"):
        errors.append("missing required document title: # 英语学习资料任务清单")

    for heading in REQUIRED_SECTIONS:
        if not section(text, heading):
            errors.append(f"missing or empty section: {heading}")

    metadata = bullet_fields(section(text, "任务信息"))
    schema_version = metadata.get("清单版本", "1")
    is_v2 = schema_version in {"2", "3", "4"}
    is_v3 = schema_version in {"3", "4"}
    is_v4 = schema_version == "4"
    if schema_version not in {"1", "2", "3", "4"}:
        errors.append(f"unsupported 清单版本: {schema_version}")
    if stage in {"confirm", "generate"} and schema_version in {"1", "2", "3"}:
        errors.append("M03 poster manifest must be migrated to 清单版本 4 and reconfirmed before generation")
    for field in REQUIRED_METADATA:
        if field not in metadata:
            errors.append(f"missing task field: {field}")
    if is_v2:
        for field in REQUIRED_V2_METADATA:
            if field not in metadata:
                errors.append(f"missing version 2 task field: {field}")
        if not section(text, "成品分区确认"):
            errors.append("missing or empty version 2 section: 成品分区确认")
    else:
        warnings.append("legacy manifest schema: version 1; migrate new poster tasks to 清单版本 4")
    if is_v3:
        for field in REQUIRED_V3_METADATA:
            if field not in metadata:
                errors.append(f"missing version 3 task field: {field}")
    elif is_v2:
        warnings.append("manifest schema version 2 lacks latest-version verification; migrate new tasks to version 3")
    if is_v4:
        for field in REQUIRED_V4_METADATA:
            if field not in metadata:
                errors.append(f"missing version 4 task field: {field}")
        for heading in REQUIRED_V4_SECTIONS:
            if not section(text, heading):
                errors.append(f"missing or empty version 4 section: {heading}")

    source_rows = table_rows(section(text, "来源证据"))
    content_rows = table_rows(section(text, "学习内容"))
    allowed_text = whitelist_items(section(text, "唯一可见文字白名单"))
    acceptance = bullet_fields(section(text, "验收记录"))
    region_rows = table_rows(section(text, "成品分区确认")) if is_v2 else []

    if stage in {"confirm", "generate", "delivery"}:
        for field in REQUIRED_METADATA:
            if stage == "confirm" and field == "内容确认":
                continue
            value = metadata.get(field, "")
            if value in PLACEHOLDERS:
                errors.append(f"task field is not ready: {field}={value or '<empty>'}")
        if is_v2:
            for field in REQUIRED_V2_METADATA:
                value = metadata.get(field, "")
                if value in PLACEHOLDERS:
                    errors.append(f"version 2 task field is not ready: {field}={value or '<empty>'}")
            identity_fields = ("出版社", "教材名称", "版本或年份", "年级册次", "单元", "单元标题")
            if any(metadata.get(field, "") in PLACEHOLDERS for field in identity_fields):
                errors.append("C01 textbook or unit title is incomplete")
        if is_v3:
            for field in REQUIRED_V3_METADATA:
                value = metadata.get(field, "")
                if value in PLACEHOLDERS:
                    errors.append(f"V01 version field is not ready: {field}={value or '<empty>'}")

            strategy = metadata.get("版本策略", "")
            if strategy not in VERSION_STRATEGIES:
                errors.append(f"V01 版本策略 must be one of {sorted(VERSION_STRATEGIES)}")
            if metadata.get("最新版本核验") != "已核验":
                errors.append("V01 最新版本核验 must be 已核验 before confirmation")

            checked_text = metadata.get("版本检索日期", "")
            try:
                checked_date = date.fromisoformat(checked_text)
            except ValueError:
                errors.append("V01 版本检索日期 must use YYYY-MM-DD")
            else:
                age_days = (date.today() - checked_date).days
                if age_days < 0:
                    errors.append("V01 版本检索日期 cannot be in the future")
                elif age_days > 30 and stage in {"confirm", "generate"}:
                    errors.append("V01 version verification is older than 30 days; search again")
                elif age_days > 30:
                    warnings.append("version verification is older than 30 days")
        if is_v4:
            for field in REQUIRED_V4_METADATA:
                value = metadata.get(field, "")
                if value in PLACEHOLDERS:
                    errors.append(f"version 4 task field is not ready: {field}={value or '<empty>'}")
        if metadata.get("生成模式") != "纯生图":
            errors.append("default generation mode must be 纯生图")

        knowledge_language = metadata.get("知识提示语言", "")
        if knowledge_language:
            if knowledge_language not in KNOWLEDGE_LANGUAGE_MODES:
                errors.append(
                    f"知识提示语言 must be one of {sorted(KNOWLEDGE_LANGUAGE_MODES)}"
                )
        elif metadata.get("资料类型") == "单元复习海报":
            warnings.append("legacy manifest lacks 知识提示语言; new jobs should record 中文功能 + 英文核心句式 or confirmed Chinese-only")
        if metadata.get("教材确认") != "已确认":
            errors.append("教材确认 must be 已确认 before generation")
        if stage in {"generate", "delivery"} and metadata.get("内容确认") != "已确认":
            errors.append("内容确认 must be 已确认 before generation")

        age_band = metadata.get("学习者年龄段", "")
        age_mode = metadata.get("年龄适配方式", "")
        if age_band not in AGE_BANDS:
            errors.append(f"学习者年龄段 must use a standard value: {age_band or '<empty>'}")
        if age_mode not in AGE_MODES:
            errors.append(f"年龄适配方式 must be one of {sorted(AGE_MODES)}")
        if age_mode == "根据年级自动推断":
            inferred = infer_age_band(metadata.get("年级册次", ""))
            if inferred is None:
                errors.append("cannot infer age band from 年级册次; use 用户指定")
            elif age_band != inferred:
                errors.append(f"学习者年龄段 does not match 年级册次; expected {inferred}")

        style_id = metadata.get("风格编号", "")
        style_mode = metadata.get("风格生成方式", "")
        style_reference = metadata.get("风格参考图", "")
        layout = metadata.get("版式骨架", "")
        capacity_decision = metadata.get("容量处理", "自动适配版式")
        if style_id not in REGISTERED_STYLE_IDS:
            errors.append(f"风格编号 must use a registered value: {style_id or '<empty>'}")
        elif style_id in LEGACY_STYLE_IDS:
            warnings.append(
                f"legacy style id: {style_id}; migrate to {LEGACY_STYLE_IDS[style_id]}"
            )
        if style_mode not in STYLE_MODES:
            errors.append(f"风格生成方式 must be one of {sorted(STYLE_MODES)}")
        if layout not in LAYOUT_ARCHETYPES:
            errors.append(f"版式骨架 must be one of {sorted(LAYOUT_ARCHETYPES)}")
        if capacity_decision not in CAPACITY_DECISIONS:
            errors.append(f"容量处理 must be one of {sorted(CAPACITY_DECISIONS)}")
        if style_mode == "文字视觉 DNA + 参考图增强" and style_reference in NON_VISIBLE:
            errors.append("风格参考图 is required only when 参考图增强 is selected")

        valid_sources = [row for row in source_rows if len(row) >= 4 and all(cell not in PLACEHOLDERS for cell in row[:4])]
        if not valid_sources:
            errors.append("at least one complete source row is required")
        if is_v3 and valid_sources and not any(
            any(term in row[2] for term in VERSION_EVIDENCE_TERMS)
            for row in valid_sources
        ):
            errors.append("V02 at least one source row must support version or applicable school year")

        minimum_cells = 9 if is_v2 else 6
        valid_content = [
            row
            for row in content_rows
            if len(row) >= minimum_cells
            and all(cell not in PLACEHOLDERS for cell in row[:minimum_cells])
        ]
        if not valid_content:
            errors.append("at least one complete learning-content row is required")
        if is_v2 and len(valid_content) != len(content_rows):
            errors.append("C03 one or more version 2 learning-content rows are incomplete")

        seen: set[tuple[str, str, str]] = set()
        for row_index, row in enumerate(valid_content, start=1):
            if is_v2:
                content_type, english, chinese = row[2], row[3], row[4]
                visible_values = (english, chinese, row[5])
                if content_type == "词汇" and row[6] in NO_ILLUSTRATION:
                    errors.append(f"C02 vocabulary row lacks a concrete illustration: {row_index}")
            else:
                content_type, english, chinese = row[1], row[2], row[3]
                visible_values = (english, chinese)
            key = (content_type.casefold(), english.casefold(), chinese.casefold())
            if key in seen:
                errors.append(f"duplicate learning-content row: {row_index}")
            seen.add(key)
            for value in visible_values:
                for fragment in visible_fragments(value):
                    if fragment not in allowed_text:
                        errors.append(f"visible content missing from whitelist: {fragment}")

        if is_v2:
            material_type = metadata.get("资料类型", "")
            content_types = {row[2] for row in valid_content}
            for accepted_types in CONTENT_REQUIREMENTS.get(material_type, ()):
                if not content_types.intersection(accepted_types):
                    label = " or ".join(accepted_types)
                    errors.append(f"C03 content contract missing required type: {label}")

            if material_type == "单元复习海报" and stage in {"confirm", "generate"} and knowledge_language in {"", "中英双语"}:
                errors.append(
                    "M01 legacy knowledge-tip mode must be upgraded to 中文功能 + 英文核心句式 and reconfirmed before generation"
                )

            if material_type == "单元复习海报" and knowledge_language == "中英双语":
                for row_index, row in enumerate(valid_content, start=1):
                    if row[2] in {"知识提示", "语法"}:
                        if row[3] in NON_VISIBLE or row[4] in NON_VISIBLE:
                            errors.append(
                                f"T06 bilingual knowledge tip requires English and Chinese: row {row_index}"
                            )

            if material_type == "单元复习海报":
                for row_index, row in enumerate(valid_content, start=1):
                    if row[2] in {"知识提示", "语法"}:
                        english_fragments = visible_fragments(row[3])
                        if knowledge_language == "中文功能 + 英文核心句式" and (not english_fragments or row[4] in NON_VISIBLE):
                            errors.append(
                                f"T06 learning tip requires a Chinese function and an English sentence frame: row {row_index}"
                            )
                        if any(fragment.casefold() in META_LANGUAGE_TRANSLATIONS for fragment in english_fragments):
                            errors.append(
                                f"T07 learning-tip English must be a reusable sentence frame, not a translated function label: row {row_index}"
                            )

            if stage in {"confirm", "generate"}:
                capacity_result = analyze_layout_capacity(metadata, valid_content)
                if material_type in POSTER_TYPES and capacity_result["level"] == "split_required":
                    errors.append("L02 single-page content exceeds the selected style capacity; split pages and reconfirm")
                elif material_type in POSTER_TYPES and capacity_result["blocking"]:
                    errors.append("L02 selected layout cannot hold the confirmed content; adjust layout and reconfirm")
                elif material_type in POSTER_TYPES and capacity_result["level"] == "review":
                    warnings.append("L01 content is near the selected style capacity; review the preflight report before confirmation")
                elif material_type in POSTER_TYPES and capacity_result["level"] == "override_confirmed":
                    warnings.append("L03 heuristic overload accepted for a confirmed single-page adaptive attempt; inspect readability after generation")

            if material_type in POSTER_TYPES:
                region_names = [row[0] for row in region_rows if len(row) >= 4]
                if len(region_names) != len(set(region_names)):
                    errors.append("C04 duplicate confirmed poster region")
                regions: dict[str, list[str]] = {
                    row[0]: row for row in region_rows if len(row) >= 4
                }
                missing_regions = sorted(POSTER_REGIONS - set(regions))
                for region in missing_regions:
                    errors.append(f"C04 missing confirmed poster region: {region}")
                for region, row in regions.items():
                    if region not in POSTER_REGIONS:
                        errors.append(f"C04 unknown poster region is forbidden: {region}")
                        continue
                    if row[1] not in REGION_STATES:
                        errors.append(f"C04 invalid region state: {region}={row[1]}")
                    if any(cell in PLACEHOLDERS for cell in row[:4]):
                        errors.append(f"C04 poster region is not ready: {region}")
                required_visible = {"标题区", "单元主题区", "核心词汇区", "视觉信息区"}
                if material_type == "单元复习海报":
                    required_visible = POSTER_REGIONS
                for region in sorted(required_visible):
                    if region in regions and regions[region][1] != "展示":
                        errors.append(f"C04 required poster region must be 展示: {region}")

                split_plan = bullet_fields(section(text, "成品分区确认")).get("页面拆分", "")
                if split_plan in PLACEHOLDERS:
                    errors.append("C04 页面拆分 must be confirmed")

            if is_v4:
                validate_v4_contract(text, metadata, valid_content, region_rows, errors)

        if not allowed_text or any(item in PLACEHOLDERS for item in allowed_text):
            errors.append("visible-text whitelist is empty or contains placeholders")
        if is_v2:
            for field in ("主标题", "副标题"):
                value = metadata.get(field, "")
                if value not in NON_VISIBLE and value not in allowed_text:
                    errors.append(f"C04 visible title missing from whitelist: {field}={value}")

    if stage == "delivery":
        for field in ("清单校验", "文字检查", "配图检查"):
            if acceptance.get(field) != "通过":
                errors.append(f"delivery acceptance must be 通过: {field}")
        image_count = acceptance.get("图片数量", "")
        if not re.search(r"\b[1-9]\d*\b", image_count):
            errors.append("图片数量 must contain a positive integer")
        if acceptance.get("已知限制", "") in PLACEHOLDERS:
            warnings.append("已知限制 has not been recorded")

    return {
        "path": str(path),
        "stage": stage,
        "status": "ok" if not errors else "error",
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "source_rows": len(source_rows),
            "content_rows": len(content_rows),
            "whitelist_items": len(allowed_text),
            "schema_version": schema_version,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--stage", choices=("draft", "confirm", "generate", "delivery"), default="draft")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(args.manifest.expanduser().resolve(), args.stage)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status'].upper()}: {result['path']} ({result['stage']})")
        for message in result["errors"]:
            print(f"ERROR: {message}")
        for message in result["warnings"]:
            print(f"WARNING: {message}")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
