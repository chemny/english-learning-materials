# English Learning Materials

English | [中文](./README.zh.md)

Create source-checked vocabulary-review or unit-review posters from a specified textbook and unit. The Skill turns research and design into a deterministic workflow with exact module locking, age-appropriate visuals, and a complete AI-generated image by default.

It is designed for users and teams such as teachers, parents, tutors, course creators, and learning-material producers who need consistent single-page or batch resources without guessing textbook content.

## Preview

![Hand-drawn PEP English Unit 2 review poster](./assets/readme/preview-handdrawn-unit2.png)

![Campus magazine English review poster](./assets/style-references/campus-magazine-v1.png)

![Modern study journal English review poster](./assets/style-references/modern-study-journal-v1.png)

![Youth comic English review poster](./assets/style-references/youth-comic-poster-v1.png)

These generated cases are preferred style-and-layout references whenever the files exist and the runtime accepts image inputs. Their textbook wording, branding, characters, and individual illustrations are not reusable content templates. If a case image is unavailable, the Skill automatically falls back to the theme's complete text visual DNA without blocking generation.

## What It Does

The Skill verifies the textbook identity and unit title, applies a material-type content contract, organizes poster regions into a Markdown manifest, renders a final-product confirmation card, generates one complete image per manifest, and validates visible text and illustrations before delivery.

## Core Capabilities

| Capability | What it helps you do |
|---|---|
| Textbook verification | Confirm publisher, edition, grade, term, unit, and title from inspectable sources |
| Latest-version gate | Re-check the current applicable edition for every new task and prevent silent fallback to richer legacy sources |
| Source-backed manifests | Keep vocabulary, translations, sentence patterns, layout, and evidence in one auditable file |
| Material-type contracts | Prevent a unit review poster from silently degrading into a vocabulary-only list |
| Cross-device stability contract | Lock the two poster modes, vocabulary tiers, supporting-module counts, and forbidden extra modules |
| Product-shaped confirmation | Confirm titles, vocabulary illustrations, sentence patterns, learning tips, regions, and page plan before generation |
| Adaptive layout preflight | Estimate load from the theme, grid, and text length, then choose automatic adaptation, page splitting, or a confirmed single-page attempt |
| Legacy regeneration gate | Keep historical delivery checks compatible while requiring old manifests to migrate and be reconfirmed before regeneration |
| Age adaptation | Match characters, scenes, color maturity, decoration, typography, and density to the learner stage |
| Upper-grade age lock | Keep upper-primary, junior-high, and senior-high characters from drifting into toddler, chibi, or early-primary proportions |
| Four visual themes | Choose Hand-drawn Playful, Campus Magazine, Modern Study Journal, or Youth Comic Poster, or provide a reference image |
| Reference-first style routing | Use a supplied or bundled example for layout by default; automatically fall back to detailed text visual DNA when no readable image is available |
| Pure image generation | Produce a complete visual with the current Agent's native image-generation capability by default |
| First-pass readiness gate | Resolve the runtime canvas, module/style conflicts, text-bearing illustration risks, and learner-age cues before calling the image model |
| Region-bound text plan | Bind every approved title, label, and learning item to a region and occurrence count, removing combined-title aliases before generation |
| Generation economy | Generate one intended final first, allow one targeted retry only after a recorded hard failure, and require explicit approval before a third generation |
| Single or batch production | Generate independent manifests and images for one unit or a larger material pack |
| Quality gates | Check confirmations, source rows, visible-text whitelist, image count, spelling, and semantic alignment through full-resolution region-by-region visual review |

## Platform Compatibility

The Skill uses portable Markdown instructions and Python scripts based on the standard library. It is designed for Codex, Claude Code, and OpenClaw when the current Agent can browse sources, generate images, and inspect full-resolution images. The scripts are portable across macOS and Windows with Python 3.10 or newer.

## Install

Send this to your Agent:

```text
Install this Skill for me:
https://github.com/chemny/english-learning-materials
```

The Agent will choose the installation method for the current client, check dependencies, and verify that the Skill loads.

## Quick Start

```text
Use English Learning Materials to create a unit-review poster for PEP English, Grade 4, first semester, Unit 1. Lock exactly three main modules: vocabulary, sentence patterns, and learning tips. Use the Hand-drawn Playful style, infer learner age from the grade, and keep pure image generation.
```

The workflow pauses first for textbook identity confirmation and again for the final manifest, page plan, visual style, and age adaptation.

## Usage Examples

- Create one vocabulary poster for a specified textbook unit.
- Generate a batch of review cards for several units with a locked visual system.
- Create both a vocabulary-only poster and an exact three-module unit-review poster for the same unit.
- Use a supplied reference image for visual direction without copying its text, characters, or branding.
- Override the inferred learner stage when the student's actual age differs from the textbook grade.

## How It Works

1. Collect the material type, textbook identity, output size, visual style, and learner information.
2. Verify the textbook and unit from inspectable sources, then confirm the identity with the user.
3. Build a schema-v4 `material-manifest.md` with complete candidate pools, deterministic selections, exact modules, a visible-text whitelist, layout, and age profile.
4. Run the theme-aware layout preflight; treat `review` as guidance and choose automatic adaptation, page splitting, or a confirmed single-page attempt for clear overload.
5. Render and confirm a final-product content card that mirrors the planned poster regions.
6. Validate the confirmed manifest and compile a fingerprinted `generation-package.md` with region-bound visible-text placement and combined-title alias removal.
7. Run `generation_preflight.py`; do not generate until every hard component passes and readiness is at least 90/100.
8. Generate one intended-final image per manifest. Retry only after recording a hard acceptance failure.
9. Inspect the full-resolution image region by region for spelling, duplicate or out-of-list text, illustration mapping, region consistency, age fit, and batch consistency before delivery.

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── readme/
│   │   └── preview-handdrawn-unit2.png
│   └── style-references/
│       ├── asset-manifest.json
│       ├── campus-magazine-v1.png
│       ├── modern-study-journal-v1.png
│       ├── primary-handdrawn-fresh-v2.png
│       └── youth-comic-poster-v1.png
├── references/
│   ├── age-adaptation.md
│   ├── content-contracts.md
│   ├── manifest-schema.md
│   ├── qa-checklist.md
│   ├── source-policy.md
│   ├── style-campus-magazine-v1.md
│   ├── style-modern-study-journal-v1.md
│   ├── style-primary-handdrawn-v1.md
│   ├── style-presets.md
│   └── style-youth-comic-poster-v1.md
├── scripts/
    ├── age_profiles.py
    ├── build_generation_package.py
    ├── check_layout_capacity.py
    ├── content_contract.py
    ├── generation_preflight.py
    ├── init_material_job.py
    ├── render_confirmation_card.py
    ├── validate_batch.py
    ├── validate_output_images.py
    ├── verify_reference_assets.py
    └── validate_manifest.py
└── tests/
    ├── test_content_contract_v4.py
    └── test_generation_preflight.py
```

## Requirements

- An Agent runtime that can inspect web sources or user-provided textbook pages.
- A native or connected image-generation capability for final visual production.
- Python 3.10+ for workspace initialization and deterministic manifest validation.
- Access to GitHub during installation.

No API key is stored in this repository. The Skill does not bundle textbook scans, copied lesson pages, or user-uploaded reference images.

Bundled style examples are preferred visual references. When present and supported, the Skill uses their layout, hierarchy, palette, density, and decorative rhythm by default. When unavailable or unsupported, it continues with the registered text visual DNA and fixed style prompt.

## License

Released under the [MIT License](./LICENSE). Textbook content, product names, and user-provided materials remain subject to their respective rights and permitted-use boundaries.
