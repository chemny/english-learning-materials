#!/usr/bin/env python3
"""Deterministic age-appropriate visual prompt blocks for learning materials."""

from __future__ import annotations


AGE_VISUAL_PROFILES = {
    "学前（4–6岁）": (
        "Learner age band: preschool, 4–6 years old. Use clearly preschool-age children in safe, "
        "ordinary learning or play settings, with simple actions, large readable elements and low "
        "information density. Bright rounded decoration is allowed, but keep bodies, faces and objects "
        "coherent and naturally proportioned for this age. Do not make the children look like babies, "
        "teenagers or adults."
    ),
    "小学低年级（6–8岁）": (
        "Learner age band: lower primary, 6–8 years old. Characters must look like school-age children, "
        "not toddlers or preschoolers. Use natural child proportions, clear classroom or everyday actions, "
        "large readable type and direct illustrations. Avoid baby faces, infant proportions, nursery props, "
        "extreme chibi bodies and characters that look younger than six."
    ),
    "小学中年级（8–10岁）": (
        "Learner age band: middle primary, 8–10 years old. Characters must look like independent school-age "
        "children, with natural proportions, normal-sized eyes, age-appropriate classroom clothing and "
        "clear study or family actions. Keep playful details organized rather than nursery-like. Avoid toddler "
        "faces, baby cheeks as the main age cue, oversized heads or eyes, chibi bodies, kindergarten props and "
        "preschool sticker overload."
    ),
    "小学高年级（10–12岁）": (
        "Learner age band: upper primary, 10–12 years old. Characters must look like preteen students, not "
        "younger primary-school children. Use natural preteen proportions, normal-sized eyes, longer limbs than "
        "early-childhood figures, composed posture, age-appropriate school clothing and more structured campus "
        "or everyday scenes. Reduce nursery decoration and toy-like icons. Avoid toddler proportions, baby faces, "
        "oversized heads or eyes, chibi figures, kindergarten props, giant hearts, crowns and sticker overload."
    ),
    "初中（12–15岁）": (
        "Learner age band: junior high, 12–15 years old. Characters must unmistakably look like teenagers, not "
        "primary-school children. Use natural adolescent proportions, normal-sized eyes, longer limbs, mature but "
        "friendly posture, and age-appropriate school uniforms, hoodies, backpacks, notebooks, clubs, sports or "
        "campus-interest settings. Keep decoration clean and restrained. Avoid toddler proportions, baby faces, "
        "oversized heads or eyes, chibi figures, kindergarten or early-primary classroom styling, crowns, giant "
        "hearts, sticker overload and childish toy props."
    ),
    "高中（15–18岁）": (
        "Learner age band: senior high, 15–18 years old. Characters must look like older teenage students, not "
        "children and not adult professionals. Use natural older-adolescent proportions, composed posture, realistic "
        "school clothing, academic or real-life study contexts, restrained decoration and efficient information "
        "hierarchy. Prefer diagrams or mature study objects when people are unnecessary. Avoid toddler or chibi "
        "proportions, baby faces, oversized eyes, nursery colors, toy-like icons, crowns, giant hearts and sticker overload."
    ),
    "成人（18岁以上）": (
        "Learner age band: adult, 18 years and older. Use adult characters only when they support the learning "
        "context, with natural adult proportions, professional or everyday clothing and efficient real-world scenes. "
        "Keep decoration purposeful and typography scan-friendly. Avoid child, teen, toddler or chibi character styling "
        "and school-age toy props unless the confirmed subject explicitly requires them as content."
    ),
}


def age_prompt_block(age_band: str) -> str:
    """Return the locked prompt block for a validated manifest age band."""
    try:
        profile = AGE_VISUAL_PROFILES[age_band]
    except KeyError as exc:
        raise ValueError(f"unsupported learner age band: {age_band or '<empty>'}") from exc
    return (
        f"{profile}\n"
        "Age adaptation changes characters, scenes, props, decoration maturity, typography maturity and information "
        "density only. Preserve the user's confirmed layout, style identity, color system, border topology and drawing "
        "medium. Hand-drawn, cartoon, comic, magazine and journal are media or layout choices, not age assignments.\n"
        "If a style protocol or reference image suggests a younger or older audience, this age lock overrides only its "
        "character age, body proportions, clothing, scene maturity and age-coded decoration. Do not replace the selected "
        "layout or medium. When no people appear, apply the same age maturity to objects, icons, typography and density."
    )
