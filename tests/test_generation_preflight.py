from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_generation_package import build, compile_visible_text_plan  # noqa: E402
from generation_preflight import (  # noqa: E402
    ILLUSTRATION_SURFACE_LOCK,
    material_type_style_lock,
    runtime_canvas_lock,
    sanitize_visual_instruction,
    score_generation_package,
    verify_manifest_freshness,
    visual_risk_guard,
)
from test_content_contract_v4 import manifest  # noqa: E402
from content_contract import VOCABULARY_POSTER  # noqa: E402


class GenerationPreflightTests(unittest.TestCase):
    def write_manifest(self, content: str) -> Path:
        directory = Path(tempfile.mkdtemp())
        path = directory / "material-manifest.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_portrait_design_resolves_to_one_exact_runtime_canvas(self) -> None:
        pixels, block = runtime_canvas_lock("竖版 3:4")
        self.assertEqual(pixels, "1024×1536")
        self.assertIn("exactly 1024×1536 pixels", block)
        self.assertIn("do not generate an unsupported intermediate ratio", block)

    def test_explicit_pixel_dimensions_are_preserved(self) -> None:
        pixels, block = runtime_canvas_lock("竖版 2160×3840")
        self.assertEqual(pixels, "2160×3840")
        self.assertIn("exactly 2160×3840 pixels", block)

    def test_vocabulary_style_lock_removes_review_modules(self) -> None:
        block = material_type_style_lock(VOCABULARY_POSTER)
        self.assertIn("exactly one learning module", block)
        self.assertIn("ignore any style-protocol", block)
        self.assertIn("sentence-pattern panel", block)

    def test_text_bearing_semantics_receive_specific_guards(self) -> None:
        guard = visual_risk_guard("学生证上的完整姓名与年级数字", "个人信息")
        self.assertIn("TEXT-RISK GUARD", guard)
        self.assertIn("do not invent names", guard)
        self.assertIn("do not invent digits", guard)

    def test_clothing_and_prop_surfaces_receive_text_and_number_guards(self) -> None:
        guard = visual_risk_guard("穿蓝色球衣并制作机器人", "人物能力")
        self.assertIn("TEXT-RISK GUARD", guard)
        self.assertIn("digits", guard)
        self.assertIn("logos", guard)

    def test_numeric_positive_semantics_are_rewritten_not_merely_negated(self) -> None:
        age = sanitize_visual_instruction("生日蜡烛与年龄数字", "年龄信息")
        grade = sanitize_visual_instruction("年级数字徽章", "学校信息")
        self.assertIn("普通未编号蜡烛", age)
        self.assertNotIn("年龄数字", age)
        self.assertIn("抽象校园等级徽章", grade)
        self.assertNotIn("年级数字徽章", grade)

    def test_text_surface_positive_semantics_are_rewritten_as_blank(self) -> None:
        card = sanitize_visual_instruction("学生证上的完整姓名", "个人身份信息")
        interface = sanitize_visual_instruction("论坛中的一张个人帖子卡片", "线上交友语境")
        self.assertIn("空白抽象学生资料卡", card)
        self.assertIn("无文字的抽象数字界面", interface)

    def test_visual_subject_takes_priority_over_usage_context(self) -> None:
        page = sanitize_visual_instruction("翻开的资料页面", "阅读论坛帖子")
        self.assertIn("翻开的空白页面", page)
        self.assertNotIn("抽象数字界面", page)

    def test_low_risk_semantics_do_not_gain_noise(self) -> None:
        self.assertEqual(visual_risk_guard("学生挥拍打网球", "兴趣爱好"), "")

    def test_built_package_passes_first_pass_readiness(self) -> None:
        package = build(self.write_manifest(manifest(VOCABULARY_POSTER)), ROOT)
        score = score_generation_package(package)
        self.assertEqual(score["total"], 100)
        self.assertTrue(score["ready"])
        self.assertIn("### Runtime canvas lock", package)
        self.assertIn("### Material-type style lock", package)
        self.assertIn("### Visible-text occurrence lock", package)
        self.assertIn("### Illustration surface text lock", package)
        self.assertIn(ILLUSTRATION_SURFACE_LOCK, package)
        self.assertIn("### First-pass execution lock", package)

    def test_manifest_fingerprint_blocks_stale_generation_package(self) -> None:
        manifest_path = self.write_manifest(manifest(VOCABULARY_POSTER))
        package_text = build(manifest_path, ROOT)
        package_path = manifest_path.with_name("generation-package.md")
        package_path.write_text(package_text, encoding="utf-8")
        self.assertTrue(verify_manifest_freshness(package_path, package_text)["pass"])

        manifest_path.write_text(manifest_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        stale = verify_manifest_freshness(package_path, package_text)
        self.assertFalse(stale["pass"])
        self.assertIn("changed after package build", stale["reason"])

    def test_combined_header_alias_is_zero_locked_not_rendered(self) -> None:
        regions = [
            ["标题区", "展示", "核心词汇清单", "标题"],
            ["单元主题区", "展示", "Unit 1；You and Me", "单元"],
        ]
        content = [["1", "核心词汇区", "词汇", "friend", "朋友", "不适用", "朋友击掌", "关系", "source"]]
        plan = compile_visible_text_plan(
            ["核心词汇清单", "Unit 1", "You and Me", "Unit 1 You and Me", "核心词汇", "friend", "朋友"],
            regions,
            content,
            ["核心词汇"],
        )
        self.assertNotIn("Unit 1 You and Me", plan["renderable"])
        self.assertEqual(plan["zero_count_aliases"], ["Unit 1 You and Me"])

    def test_unplaced_non_alias_text_blocks_compilation(self) -> None:
        regions = [["标题区", "展示", "英语复习", "标题"]]
        with self.assertRaisesRegex(ValueError, "P01"):
            compile_visible_text_plan(["英语复习", "随意口号", "核心词汇"], regions, [], ["核心词汇"])

    def test_confirmed_user_facing_module_aliases_are_region_bound(self) -> None:
        regions = [
            ["标题区", "展示", "英语复习", "标题"],
            ["核心词汇区", "展示", "核心词汇；16项词汇", "词汇"],
            ["核心句型区", "展示", "句子串联；2组句型", "句型"],
            ["知识提示区", "展示", "句型特点；3组提示", "提示"],
        ]
        plan = compile_visible_text_plan(
            ["英语复习", "核心词汇", "句子串联", "句型特点"],
            regions,
            [],
            ["核心词汇", "核心句型", "知识提示"],
        )
        self.assertIn(("核心词汇区", "核心词汇"), plan["placements"])
        self.assertIn(("核心句型区", "句子串联"), plan["placements"])
        self.assertIn(("知识提示区", "句型特点"), plan["placements"])
        self.assertNotIn(("主体模块标签", "核心句型"), plan["placements"])
        self.assertNotIn(("主体模块标签", "知识提示"), plan["placements"])

    def test_built_package_removes_combined_header_alias_everywhere(self) -> None:
        content = manifest(VOCABULARY_POSTER).replace(
            "| 单元主题区 | 展示 | Unit 1 | 单元 |",
            "| 单元主题区 | 展示 | Unit 1；Test unit | 单元 |",
        ).replace(
            "- Unit 1\n",
            "- Unit 1\n- Test unit\n- Unit 1 Test unit\n",
            1,
        )
        package = build(self.write_manifest(content), ROOT)
        visible = package.split("## VISIBLE TEXT — RENDER VERBATIM", 1)[1].split(
            "### Region-bound visible-text placement plan", 1
        )[0]
        self.assertIn("- Unit 1\n", visible)
        self.assertIn("- Test unit\n", visible)
        self.assertNotIn("Unit 1 Test unit", visible)
        self.assertNotIn("Unit 1 Test unit", package)
        self.assertIn("Detected and removed 1 alternate combined header alias", package)

    def test_legacy_package_scores_lower_than_compiled_package(self) -> None:
        legacy = """# 标准生图任务包
- 版式与尺寸：compact-grid；竖版 3:4
## EXACT MODULES
- 核心词汇
## VISIBLE TEXT — RENDER VERBATIM
- word
## NON-VISIBLE VISUAL INSTRUCTIONS — NEVER RENDER AS TEXT
### Age adaptation lock
Hand-drawn, cartoon, comic, magazine and journal are media or layout choices, not age assignments.
- ITEM 1: 学生证上的完整姓名与年级数字. This entire instruction is non-visible and must never be printed.
"""
        current = build(self.write_manifest(manifest(VOCABULARY_POSTER)), ROOT)
        self.assertLess(score_generation_package(legacy)["total"], score_generation_package(current)["total"])


if __name__ == "__main__":
    unittest.main()
