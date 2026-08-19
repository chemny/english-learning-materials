from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_generation_package import build  # noqa: E402
from age_profiles import AGE_VISUAL_PROFILES, age_prompt_block  # noqa: E402
from content_contract import (  # noqa: E402
    FORBIDDEN_MODULES,
    UNIT_POSTER,
    VOCABULARY_POSTER,
    choose_vocabulary_tier,
)
from render_confirmation_card import render  # noqa: E402
from validate_manifest import validate  # noqa: E402


def manifest(material_type: str) -> str:
    unit = material_type == UNIT_POSTER
    modules = "核心词汇 + 核心句型 + 知识提示" if unit else "核心词汇"
    sentence_count = 4 if unit else 0
    tip_count = 4 if unit else 0
    vocab_candidates = "\n".join(
        f"| {i} | word{i} | 词{i} | 词汇 | 1 | 是 | 按教材顺序入选 | source#{i} |"
        for i in range(1, 10)
    )
    sentence_candidates = "\n".join(
        f"| {i} | Question {i}?<br>Answer {i}. | 问答{i} | 是 | 场景{i} | source#s{i} |"
        for i in range(1, 5)
    ) if unit else ""
    tip_candidates = "\n".join(
        f"| {i} | 功能{i} | Frame {i} ... | 是 | 场景{i} | source#t{i} |"
        for i in range(1, 5)
    ) if unit else ""
    vocab_content = "\n".join(
        f"| {i} | 核心词汇区 | 词汇 | word{i} | 词{i} | 不适用 | 画对象{i} | 语境{i} | source#{i} |"
        for i in range(1, 10)
    )
    sentence_content = "\n".join(
        f"| {9+i} | 核心句型区 | 句型 | Question {i}?<br>Answer {i}. | 问答{i} | 不适用 | 对话场景{i} | 场景{i} | source#s{i} |"
        for i in range(1, 5)
    ) if unit else ""
    tip_content = "\n".join(
        f"| {13+i} | 知识提示区 | 知识提示 | Frame {i} ... | 功能{i} | 不适用 | 便签{i} | 场景{i} | source#t{i} |"
        for i in range(1, 5)
    ) if unit else ""
    module_rows = "| 1 | 核心词汇 | 必须展示 | 已入选词汇 |"
    if unit:
        module_rows += "\n| 2 | 核心句型 | 必须展示 | 已入选句型 |\n| 3 | 知识提示 | 必须展示 | 已入选提示 |"
    sentence_state = "展示" if unit else "不展示"
    tip_state = "展示" if unit else "不展示"
    sentence_region = "4组句型" if unit else "不适用"
    tip_region = "4组提示" if unit else "不适用"
    whitelist = ["英语复习", "Unit 1"]
    for i in range(1, 10):
        whitelist.extend((f"word{i}", f"词{i}"))
    if unit:
        for i in range(1, 5):
            whitelist.extend((f"Question {i}?", f"Answer {i}.", f"问答{i}", f"Frame {i} ...", f"功能{i}"))
    whitelist_text = "\n".join(f"- {item}" for item in whitelist)
    forbidden = "、".join(FORBIDDEN_MODULES)
    return f"""# 英语学习资料任务清单

## 任务信息

- 清单版本：4
- Skill版本：1.2.0
- 内容契约版本：exact-modules-v1
- 资料类型：{material_type}
- 内容范围：已确认范围
- 主体模块：{modules}
- 额外学习模块：禁止
- 词汇数量档位：9
- 词汇网格：3×3
- 句型组数：{sentence_count}
- 知识提示组数：{tip_count}
- 生成规模：单张
- 生成模式：纯生图
- 出版社：人民教育出版社
- 教材名称：英语
- 版本或年份：2026
- 版本策略：当前最新适用版本
- 版本检索日期：{date.today().isoformat()}
- 最新版本核验：已核验
- 版本差异说明：已核对当前版本
- 年级册次：三年级下册
- 学习者年龄段：小学中年级（8–10岁）
- 年龄适配方式：根据年级自动推断
- 单元：Unit 1
- 单元标题：Test unit
- 主标题：英语复习
- 副标题：Unit 1
- 视觉风格：手绘童趣
- 风格编号：primary-handdrawn-poster-v1
- 风格生成方式：文字视觉 DNA + 参考图增强
- 风格参考图：assets/style-references/primary-handdrawn-fresh-v2.png
- 版式骨架：standard-grid
- 容量处理：自动适配版式
- 图片尺寸：竖版 3:4
- 教材确认：已确认
- 内容确认：已确认
- 知识提示语言：中文功能 + 英文核心句式

## 来源证据

| 来源标题 | URL或文件位置 | 支持内容 | 证据级别 |
|---|---|---|---|
| 官方目录 | https://example.com | 版本与全部测试内容 | A |

## 词汇候选池

| 教材顺序 | 英文 | 中文 | 内容类型 | 重要性等级 | 是否入选 | 选择说明 | 来源位置 |
|---:|---|---|---|---:|---|---|---|
{vocab_candidates}

## 句型候选池

| 教材顺序 | 英文 | 中文 | 是否入选 | 使用场景 | 来源位置 |
|---:|---|---|---|---|---|
{sentence_candidates}

## 知识提示候选池

| 教材顺序 | 中文学习功能 | 英文核心句式 | 是否入选 | 使用场景 | 来源位置 |
|---:|---|---|---|---|---|
{tip_candidates}

## 学习内容

| 编号 | 成品区域 | 内容类型 | 英文可见文字 | 中文可见文字 | 音标或词性 | 配图或呈现方式 | 使用场景或说明 | 来源位置 |
|---:|---|---|---|---|---|---|---|---|
{vocab_content}
{sentence_content}
{tip_content}

## 主体模块锁定

| 序号 | 模块 | 状态 | 允许内容 |
|---:|---|---|---|
{module_rows}

- 禁止模块：{forbidden}

## 成品分区确认

| 区域 | 状态 | 已确认内容 | 版式责任 |
|---|---|---|---|
| 标题区 | 展示 | 英语复习 | 标题 |
| 单元主题区 | 展示 | Unit 1 | 单元 |
| 核心词汇区 | 展示 | 9个词汇 | 词卡 |
| 核心句型区 | {sentence_state} | {sentence_region} | 句型 |
| 知识提示区 | {tip_state} | {tip_region} | 提示 |
| 视觉信息区 | 展示 | 中年级手绘 | 视觉 |

- 页面拆分：单页

## 唯一可见文字白名单

{whitelist_text}

## 视觉与版式

- 标题区：清晰标题
- 内容区：3×3
- 句型区：底部左侧
- 知识提示区：底部右侧
- 装饰元素：少量文具
- 参考图角色：风格参考

## 生图约束

- 只允许白名单文字。

## 验收记录

- 清单校验：未执行
- 图片数量：1
- 文字检查：未执行
- 配图检查：未执行
- 整组一致性：不适用
- 已知限制：无
"""


class ContractV4Tests(unittest.TestCase):
    def write_manifest(self, content: str) -> Path:
        directory = Path(tempfile.mkdtemp())
        path = directory / "material-manifest.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_both_modes_validate(self) -> None:
        for material_type in (VOCABULARY_POSTER, UNIT_POSTER):
            result = validate(self.write_manifest(manifest(material_type)), "generate")
            self.assertEqual(result["status"], "ok", result["errors"])

    def test_vocabulary_tier_ladder_and_layout_caps(self) -> None:
        self.assertEqual(choose_vocabulary_tier(30, "compact-grid"), 25)
        self.assertEqual(choose_vocabulary_tier(23, "compact-grid"), 20)
        self.assertEqual(choose_vocabulary_tier(19, "compact-grid"), 16)
        self.assertEqual(choose_vocabulary_tier(15, "compact-grid"), 12)
        self.assertEqual(choose_vocabulary_tier(11, "compact-grid"), 9)
        self.assertIsNone(choose_vocabulary_tier(8, "compact-grid"))
        self.assertEqual(choose_vocabulary_tier(30, "standard-grid"), 20)
        self.assertEqual(choose_vocabulary_tier(30, "large-card-grid"), 12)

    def test_random_tier_is_rejected(self) -> None:
        content = manifest(VOCABULARY_POSTER).replace("词汇数量档位：9", "词汇数量档位：12")
        result = validate(self.write_manifest(content), "generate")
        self.assertTrue(any("D04" in item for item in result["errors"]))

    def test_schema_v3_cannot_be_reconfirmed(self) -> None:
        content = manifest(UNIT_POSTER).replace("清单版本：4", "清单版本：3")
        result = validate(self.write_manifest(content), "confirm")
        self.assertTrue(any("M03" in item for item in result["errors"]))

    def test_unknown_region_is_rejected(self) -> None:
        content = manifest(VOCABULARY_POSTER).replace(
            "| 视觉信息区 | 展示 | 中年级手绘 | 视觉 |",
            "| 视觉信息区 | 展示 | 中年级手绘 | 视觉 |\n| 学习目标区 | 展示 | 目标 | 额外模块 |",
        )
        result = validate(self.write_manifest(content), "generate")
        self.assertTrue(any("unknown poster region" in item for item in result["errors"]))

    def test_extra_learning_module_is_rejected(self) -> None:
        content = manifest(UNIT_POSTER).replace(
            "## 主体模块锁定",
            "| 18 | 知识提示区 | 语法 | rule | 规则 | 不适用 | 规则框 | 语境 | source#g |\n\n## 主体模块锁定",
        )
        result = validate(self.write_manifest(content), "generate")
        self.assertTrue(any("D03 禁止的学习内容类型" in item for item in result["errors"]))

    def test_package_is_deterministic_and_locks_modules(self) -> None:
        path = self.write_manifest(manifest(UNIT_POSTER))
        first = build(path, ROOT)
        second = build(path, ROOT)
        self.assertEqual(first, second)
        self.assertIn("## EXACT MODULES", first)
        self.assertIn("## FORBIDDEN MODULES", first)
        self.assertIn("- 核心句型", first)
        self.assertIn("- 学习目标", first)

    def test_package_adds_age_lock_without_replacing_selected_style(self) -> None:
        content = manifest(VOCABULARY_POSTER).replace(
            "年级册次：三年级下册\n- 学习者年龄段：小学中年级（8–10岁）",
            "年级册次：七年级上册\n- 学习者年龄段：初中（12–15岁）",
        )
        package = build(self.write_manifest(content), ROOT)
        self.assertIn("### Age adaptation lock", package)
        self.assertIn("Learner age band: junior high, 12–15 years old.", package)
        self.assertIn("must unmistakably look like teenagers", package)
        self.assertIn("Avoid toddler proportions", package)
        self.assertIn("Style ID: primary-handdrawn-poster-v1.", package)
        self.assertIn("colored-pencil, crayon and light-watercolor", package)
        self.assertNotIn("Chinese primary-school English review poster", package)

    def test_upper_primary_age_lock_rejects_low_age_character_cues(self) -> None:
        content = manifest(VOCABULARY_POSTER).replace(
            "年级册次：三年级下册\n- 学习者年龄段：小学中年级（8–10岁）",
            "年级册次：六年级上册\n- 学习者年龄段：小学高年级（10–12岁）",
        )
        package = build(self.write_manifest(content), ROOT)
        self.assertIn("Learner age band: upper primary, 10–12 years old.", package)
        self.assertIn("preteen students", package)
        self.assertIn("Avoid toddler proportions", package)
        self.assertIn("Reference-image age boundary", package)

    def test_every_supported_age_band_has_a_layout_preserving_lock(self) -> None:
        for age_band in AGE_VISUAL_PROFILES:
            block = age_prompt_block(age_band)
            self.assertIn("Preserve the user's confirmed layout", block)
            self.assertIn("not age assignments", block)
            self.assertIn("reference image", block)

    def test_senior_high_age_lock_rejects_childish_characters(self) -> None:
        content = manifest(VOCABULARY_POSTER).replace(
            "年级册次：三年级下册\n- 学习者年龄段：小学中年级（8–10岁）",
            "年级册次：高一上册\n- 学习者年龄段：高中（15–18岁）",
        )
        package = build(self.write_manifest(content), ROOT)
        self.assertIn("Learner age band: senior high, 15–18 years old.", package)
        self.assertIn("older teenage students", package)
        self.assertIn("Avoid toddler or chibi proportions", package)
        self.assertIn("Style ID: primary-handdrawn-poster-v1.", package)

    def test_confirmation_card_shows_locked_counts(self) -> None:
        card = render(self.write_manifest(manifest(UNIT_POSTER)))
        self.assertIn("EXACT MODULES：核心词汇 + 核心句型 + 知识提示", card)
        self.assertIn("词汇 9 项（3×3）；句型 4 组；知识提示 4 组", card)


if __name__ == "__main__":
    unittest.main()
