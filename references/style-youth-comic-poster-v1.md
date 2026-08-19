# `youth-comic-poster-v1` 风格协议

使用这套协议生成更有少年感、节奏鲜明的英语漫画海报。参考图是可选增强素材，不是生成前提。

## 双通道

- `文字视觉 DNA`：始终可用，只根据本文件生成。
- `文字视觉 DNA + 参考图增强`：当下列资产存在且运行时支持图片输入时使用：
  `assets/style-references/youth-comic-poster-v1.png`

不得因参考图缺失而停止生成。使用参考图时，只借鉴漫画媒介、配色、视觉节奏、几何分区和人物成熟度；不要复制其中的教材文字、人物造型、品牌、具体配图或独特内容组合。

## 视觉 DNA

- 画布：竖版，优先 3:4；运行时只支持 2:3 时允许 2:3。
- 背景：干净的中性浅奶白或淡灰白，叠加局部网点、速度线、粗颗粒与几何色块；黄色只在爆炸框、标签和提示卡中局部出现，不形成全页黄色环境光。
- 主色：紫蓝或深海军蓝、亮青色；辅色为暖黄、橙红与白色。
- 版式指纹：31%–35%头部、47%–50%词汇区和15%–18%底部是标准密度下的推荐起点。头部保持主题英雄区、斜切Unit牌、粗体标题和少年感视觉锚点；人物数量和精确比例按内容负载调整。
- 标题：大号压缩粗体、倾斜字块和漫画标题牌形成强入口；允许头部明显大于其他主题，但人物、标题和单元牌要构成一个完整三角构图。
- 单元区：大号斜切Unit标签与主题黄条固定在左上，英文问句使用紫色斜切横条穿过标题下方。
- 内容区：16项使用4列×4行独立青色实线漫画卡片；不要增加全局虚线外框，卡片间距均匀，图、英文、中文自然排列。
- 插图：少年漫画式教育插画，人物接近目标年龄，动作有动势但不过度夸张；面部友好、衣着现代且适合校园。
- 复习区：底部左侧为深海军蓝句型栏，右侧为倾斜暖黄色提示卡，最下方使用亮青漫画页脚和方向箭头；知识提示逐项显示中文学习功能和可直接套用的英文核心句式，不显示功能标签英文直译；不得换成白色工作表底栏。
- 比例保护：人物、漫画卡、食物和文字保持自然宽高比；允许插图留白，不为填满卡片而压扁或拉宽。
- 装饰：网点、闪电、星芒、速度线、贴纸和小型徽章，只在边缘与重点处使用。
- 年龄：按照 `age-adaptation.md` 调整动势、人物成熟度和视觉冲击；小学中年级使用较柔和表情与圆角几何，高年级可提高对比和棱角感。

## 版式骨架

- `compact-grid`：16–20 项，4 列紧凑分镜网格，以局部斜切和编号制造节奏。
- `standard-grid`：10–15 项，3 列漫画模块，保留一个大号场景或句型挑战区。
- `large-card-grid`：6–9 项，2–3 列较大分镜，但仍保留强标题、几何分区、漫画纹理和复习区。

不要退化成日系角色立绘合集、幼儿卡通、游戏战斗界面、霓虹赛博海报或白底双栏人物卡。

## 核心风格提示块

把以下不可变风格锚点原样放入生图提示，再根据清单追加自适应版式说明：

```text
Style ID: youth-comic-poster-v1.
Create an energetic but school-appropriate English-learning poster using purple-blue or deep navy with vivid cyan, localized warm-yellow and small orange-red accents over clean neutral off-white. Preserve a strong comic hero header with an angled Unit marker, bold title, geometric rhythm and at least one age-appropriate youth anchor. Use solid outlined comic learning cards without a global dashed vocabulary frame and keep a cyan directional-footer cue. Add a deep-navy or angled warm-yellow review feature only when a review module is present in EXACT MODULES; a vocabulary-only poster must use those shapes as non-text accents instead of inventing review copy. Pair a Chinese learning function with a reusable English sentence frame only when the confirmed knowledge-tip module exists. Adapt exact hero height, character count, card columns and bottom split to the content load while keeping natural proportions, strong hierarchy and comfortable readability.
Avoid translated metalinguistic labels, unconfirmed Chinese-only tips, yellow wash, sepia or vintage paper, Japanese anime character sheets, toddler or chibi proportions, empty hero headers, generic centered ribbons, combat or neon-cyber interfaces, stretched content, photorealism, excessive effects behind text, global dashed vocabulary frames, generic white bottom boxes and generic worksheets.
```

随后追加画布、版式骨架、年龄适配、内容映射和唯一可见文字白名单。

## 风格验收

- 紫蓝或深蓝、亮青与暖黄形成明确识别。
- 背景为干净的中性浅奶白或淡灰白，人物肤色、白衣和词卡没有黄色污染。
- 标题和单元标签具有漫画式动势，正文仍清晰可读。
- 页面以推荐比例为起点并按内容量自适应；Unit牌、英雄标题、少年视觉锚点、实线漫画卡和复习模块共同保持明确漫画节奏。
- 分镜、斜切几何和局部网点共同构成节奏。
- 人物有少年感但年龄、衣着和动作符合学习者阶段。
- 句型或重点区具有挑战框、对话框或总结带特征。
- 黄色提示卡逐项使用“中文学习功能＋英文核心句式”，不出现功能标签英文直译；除非用户明确确认仅中文，否则不得缺少英文句式。
- 没有退化成日系立绘、游戏界面、低幼卡通或白底闪卡。

任一核心项失败，按照 `qa-checklist.md` 记录 `S01`–`S08`，指出具体缺失项并只重做当前图片。
