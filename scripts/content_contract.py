#!/usr/bin/env python3
"""Shared deterministic content contract for poster manifests."""

from __future__ import annotations


SKILL_VERSION = "1.2.0"
MANIFEST_SCHEMA_VERSION = "4"
CONTENT_CONTRACT_VERSION = "exact-modules-v1"

VOCABULARY_POSTER = "词汇复习海报"
UNIT_POSTER = "单元复习海报"
POSTER_TYPES = {VOCABULARY_POSTER, UNIT_POSTER}

VOCABULARY_TIERS = (25, 20, 16, 12, 9)
VOCABULARY_GRIDS = {
    25: "5×5",
    20: "5×4",
    16: "4×4",
    12: "4×3",
    9: "3×3",
}
LAYOUT_TIER_CAPS = {
    "compact-grid": 25,
    "standard-grid": 20,
    "large-card-grid": 12,
    "custom": 20,
}

EXACT_MODULES = {
    VOCABULARY_POSTER: ("核心词汇",),
    UNIT_POSTER: ("核心词汇", "核心句型", "知识提示"),
}

FORBIDDEN_MODULES = (
    "语音",
    "音标训练",
    "语法总结",
    "学习目标",
    "趣味挑战",
    "课堂练习",
    "易错题",
    "文化拓展",
    "阅读拓展",
    "单元任务",
    "学习方法",
    "任何未经清单确认的学习模块",
)

MODULE_STRING = {
    material_type: " + ".join(modules)
    for material_type, modules in EXACT_MODULES.items()
}


def choose_vocabulary_tier(candidate_count: int, layout: str) -> int | None:
    """Return the largest allowed tier supported by candidates and layout."""
    cap = LAYOUT_TIER_CAPS.get(layout, LAYOUT_TIER_CAPS["custom"])
    return next(
        (tier for tier in VOCABULARY_TIERS if tier <= candidate_count and tier <= cap),
        None,
    )


def choose_supporting_count(candidate_count: int) -> int | None:
    """Choose 2-4 sentence/tip groups; fewer than two is a source gap."""
    if candidate_count < 2:
        return None
    return min(candidate_count, 4)
