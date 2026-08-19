# `primary-handdrawn-poster-v1` 风格协议

使用这套协议生成英语手绘复习海报，并根据已确认的学习者年龄调整人物、场景和装饰成熟度。参考图是可选增强素材，不是生成前提。

## 双通道

- `文字视觉 DNA`：始终可用，只根据本文件生成。
- `文字视觉 DNA + 参考图增强`：当下列资产存在且运行时支持图片输入时使用：
  `assets/style-references/primary-handdrawn-fresh-v2.png`

不得因参考图缺失而停止内置风格生成。使用参考图时，只借鉴媒介、色彩、信息密度、区域结构和装饰语言；不要复制其中的教材文字、PEP 标识、人物、具体配图或独特内容组合。

## 视觉 DNA

- 画布：竖版，优先 3:4；运行时只支持 2:3 时允许 2:3，但保持相同区域结构。
- 背景：明亮的中性象牙白或柔和暖白，整体接近白色；纸张纹理轻且主要存在于手绘笔触中，不给整页覆盖黄色颗粒或旧纸滤镜。
- 主色：清透校园蓝、清爽珊瑚红；辅色为少量向日葵黄和浅天蓝。黄色只用于星星、标签和便签等约5%–8%的局部强调，不作为背景色。
- 区域比例：25%–27%头部、51%–54%词汇区、18%–21%复习区和约3%页脚是标准密度下的推荐起点；按内容量调整，但头部保持饱满、底部保持完整且不出现无意义留白。
- 标题：顶部两行饱满的圆润手绘中文标题，第一行深校园蓝、第二行珊瑚橙，字面约占画布宽度72%–82%；标题左右用目标年龄学生、徽章形状、气泡、铅笔、纸飞机或植物形成环绕构图，不把这些元素压缩成孤零零的小图标。
- 单元区：紧贴主标题下方，用横向深蓝手绘丝带承载单元信息，下方用黄色圆角胶囊承载英文主题；丝带和胶囊居中，形成标题、单元、主题的三级层级。
- 内容区：只使用一个蓝色虚线圆角外框。`核心词汇` 标签压在外框左上角并遮断该处外框，不建立独立标题行、第二层顶边或嵌套外框。内部单元格只用浅蓝色细实线分隔，不再使用虚线。
- 词汇卡层级：单元格等宽等高，但不得拉伸其中内容。左上角为蓝色圆形编号；插图放入居中的4:3安全框，以 `contain` 方式完整放入，最大宽度为单格88%、最大高度为单格52%，允许自然留白；下方依次为深蓝粗体英文和较小中文，所有文字基线对齐。
- 比例保护：人物、物体、建筑、图标、圆形编号、边框和文字均保持自然宽高比。不得横向拉宽、纵向压扁、强制填满、非等比缩放或裁切关键部分。英文使用正常字宽；长词只在单词边界自然换行，不使用压缩或拉宽字体。
- 插图：教育插画式彩铅轮廓与轻水彩填色，造型友好并符合已确认年龄；白色区域保持干净，阴影使用浅灰或淡蓝灰，避免棕黄环境色；不得使用日系动漫立绘或企业扁平矢量风。
- 复习区：底部左侧约占60%宽度，使用珊瑚橙丝带标题和逐条编号句型；右侧约占30%宽度，使用浅黄色纸张知识提示卡。知识提示逐项显示中文学习功能和可直接套用的英文核心句式，不显示功能标签的英文翻译。二者文字字号不得小于词汇中文释义。
- 装饰：星星、铅笔、爱心、纸飞机、植物、气泡和蓝色手绘波浪页脚只放在页边、标题空隙和分区转角，数量适中且不遮挡文字。
- 明度与清晰度：整体明亮、清新、自然且不刺眼；保持近白背景、鲜蓝和珊瑚红的清晰对比。禁止黄色覆盖层、棕褐复古滤镜、羊皮纸、牛皮纸、旧纸张、灰暗杂志色调、写实景观大片和过重棕色阴影。
- 年龄：按照 `age-adaptation.md` 调整人物、场景和信息密度，不把“卡通”默认等同于幼儿化。

## 版式骨架

根据学习内容数量选择：

- `compact-grid`：16–20 项，4–5 列紧凑宫格，适合完整单元复习。
- `standard-grid`：10–15 项，3–4 列宫格，保留句型区和知识提示卡。
- `large-card-grid`：6–9 项，2–3 列，保留手绘标题层级、虚线结构和至少一个完整复习模块；丝带、人物与页脚按内容空间组合。

不要仅因为内容较少就退化成纯白背景的两列大卡片。

## 核心风格提示块

把以下不可变风格锚点原样放入生图提示，再根据清单追加自适应版式说明：

```text
Style ID: primary-handdrawn-poster-v1.
Create a fresh, bright Chinese English-learning hand-drawn review poster on luminous neutral off-white or soft ivory. Use colored-pencil, crayon and light-watercolor texture inside strokes and illustrations, with clear school blue and coral red as the dominant identity and sunflower yellow only as a small accent. Preserve the rounded two-level hand-drawn title, blue unit ribbon or equivalent hand-drawn unit marker, one blue dashed vocabulary boundary with thin light-blue internal dividers, and a blue wave-footer cue or equivalent non-text finishing detail. Keep every person, object, icon, circular number badge and letterform at natural proportions; contain illustrations with clean blank space and normal-width text. Add sentence-pattern or learning-tip treatment only when those modules are present in EXACT MODULES; a vocabulary-only poster must extend its grid and must not invent review-language panels. This block defines the hand-drawn medium and layout, not the learner age; character age, clothing, scene maturity and age-coded decoration must follow the separate confirmed age adaptation lock.
Avoid translated metalinguistic function labels, unconfirmed Chinese-only tips, stretched or squashed content, condensed lettering, double dashed vocabulary borders, nested frames, yellow wash, sepia or aged paper, brown color cast, corporate flat-vector styling, Japanese anime rendering, photorealistic people, empty or undersized headers, tiny review text, generic bottom boxes, generic worksheet styling and any character-age cue that conflicts with the confirmed age adaptation lock.
```

随后再追加画布、版式骨架、年龄适配、内容映射和唯一可见文字白名单。

## 风格验收

至少同时满足以下项目才算通过：

- 背景呈明亮中性象牙白，手绘颗粒主要存在于笔触中，没有全页泛黄。
- 蓝色与珊瑚橙构成主要视觉识别。
- 顶部大标题、蓝色丝带和虚线宫格存在。
- 页面以推荐比例为起点并按内容量自适应；头部饱满、词汇可扫描、复习区可读，区域之间没有明显失衡或无意义留白。
- 核心词汇区只有一个虚线外框；标题标签压住外框，内部仅使用浅蓝细实线，不存在双层顶边或嵌套边框。
- 词汇卡等宽等高，但内部插图保持自然比例并允许留白；编号保持正圆，英文未被压缩或拉宽，中文和英文基线整齐。
- 插图呈彩铅或轻水彩绘本感。
- 底部保留句型或复习区，并有手绘页脚。
- 右侧浅黄色知识提示卡逐项使用“中文学习功能＋英文核心句式”，不出现功能标签英文直译；除非用户明确确认仅中文，否则不得缺少英文句式。
- 色彩明快清透，不得出现黄色覆盖层、棕褐复古滤镜、旧纸张或灰暗杂志色调。
- 没有退化为纯白双栏卡片、商务扁平风或日系动漫风。

任一核心项失败，按照 `qa-checklist.md` 记录 `S01`–`S08`，强化具体缺失项并只重做当前图片。
