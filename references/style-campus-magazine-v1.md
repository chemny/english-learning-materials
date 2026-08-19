# `campus-magazine-v1` 风格协议

使用这套协议生成清爽、成熟而不成人化的小学英语校园杂志式复习海报。参考图是可选增强素材，不是生成前提。

## 双通道

- `文字视觉 DNA`：始终可用，只根据本文件生成。
- `文字视觉 DNA + 参考图增强`：当下列资产存在且运行时支持图片输入时使用：
  `assets/style-references/campus-magazine-v1.png`

不得因参考图缺失而停止生成。使用参考图时，只借鉴媒介、配色、信息密度、编辑版式和装饰节奏；不要复制其中的教材文字、品牌标识、人物、具体食物插图或独特内容组合。

## 视觉 DNA

- 画布：竖版，优先 3:4；运行时只支持 2:3 时允许 2:3。
- 背景：柔和中性象牙白纸张，明亮但不呈办公文档纯白；印刷颗粒极轻，不叠加米黄、棕褐或旧纸覆盖层。
- 主色：深青绿与珊瑚红；辅色为奶油黄、浅薄荷绿和少量深蓝。
- 版式指纹：24%–27%头部、52%–56%词汇区和17%–21%底部是标准密度下的推荐起点。保持居中刊头、编辑网格和专题复习区；书本、笔筒、植物、灯泡或笔记本是可选视觉锚点，不要求全部出现。
- 标题：顶部使用醒目的两行中英文杂志刊头式标题；第一层教材年级较小，第二层核心主题最大，字形粗而友好，允许轻微印刷套色感，但不得做幼儿泡泡字。
- 单元区：用宽青绿色丝带和奶油黄副标题胶囊承载单元与英文主题，置于刊头下方中央。
- 内容区：16项优先使用4列×4行轻量编辑网格；只保留一个细绿色外框，内部为细虚线或极细实线，不堆叠大号圆角框。
- 插图：现代手绘编辑插画，人物为目标年龄附近的学生，比例自然、动作自信；物件简洁但有质感。
- 复习区：底部左侧使用珊瑚红丝带句型栏目，右侧放两名10–12岁学生或学习静物，最下方使用深青绿总结条；总结条或配套提示区必须逐项显示中文学习功能和可直接套用的英文核心句式，不显示功能标签英文直译；不得退化为孤立白色文本框。
- 文字 DNA 锚点：没有参考图时，使用一至两组校园静物平衡刊头，并保留珊瑚句型栏目或深青绿总结区等杂志专题特征；根据内容选择学生互动或学习静物，不堆砌全部道具。
- 比例保护：所有人物、食物、器物和文字保持自然宽高比；等宽单元格只控制容器，插图采用contain并允许留白。
- 装饰：少量手绘箭头、星形、胶带、下划线、编号和校园物件；装饰服务阅读动线。
- 年龄：按照 `age-adaptation.md` 调整人物、衣着、场景和信息密度；小学中高年级避免低幼表情与玩具化比例。

## 版式骨架

- `compact-grid`：16–20 项，3–4 列紧凑编辑网格，句型区压缩为底部横栏。
- `standard-grid`：10–15 项，2–3 列杂志栏目，保留明显的句型侧栏或底部专题区。
- `large-card-grid`：6–9 项，2 列图文栏目，但保留刊头、标签系统、编辑分区和至少一个复习模块。

不要退化成白底双栏闪卡、企业宣传册或只有整齐圆角卡片的通用模板。

## 核心风格提示块

把以下不可变风格锚点原样放入生图提示，再根据清单追加自适应版式说明：

```text
Style ID: campus-magazine-v1.
Create a polished school-magazine English-learning poster on bright neutral soft-ivory paper with extremely subtle editorial print grain. Use deep teal and coral red as the main identity, supported by small cream-yellow, pale-mint and navy accents. Preserve a friendly two-level magazine masthead, a clear unit marker and a lightweight editorial vocabulary grid. Use a coral or deep-teal review feature only when a review module is present in EXACT MODULES; a vocabulary-only poster must use that color as a non-text editorial accent instead of inventing a review panel. Use one or two meaningful campus still-life or student anchors to balance the composition rather than filling a fixed prop inventory. Pair a Chinese learning function with a reusable English sentence frame only when the confirmed knowledge-tip module exists. Keep editorial illustrations and typography naturally proportioned, readable, fresh and appropriate to the confirmed learner age.
Avoid translated metalinguistic labels, unconfirmed Chinese-only tips, yellow or beige wash, vintage paper, brown shadows, office-document styling, empty headers, oversized generic flashcards, nested grid frames, childish bubble lettering, toddler proportions, stretched content, corporate templates, photorealism, copied branding, generic bottom boxes and generic worksheets.
```

随后追加画布、版式骨架、年龄适配、内容映射和唯一可见文字白名单。

## 风格验收

- 明亮中性象牙白纸张和轻微编辑印刷质感存在，没有全页米黄覆盖层。
- 深青绿与珊瑚红构成主要识别色。
- 顶部具有杂志刊头层级，内容呈栏目化编辑网格。
- 页面以推荐比例为起点并按内容量自适应；刊头、编辑网格和专题复习区层级清楚，并使用一至两组校园静物或学生锚点形成平衡。
- 插图是现代手绘编辑感，人物年龄与学习者一致。
- 句型或提示区像专题栏目，而不是孤立大卡片。
- 总结条或提示区逐项使用“中文学习功能＋英文核心句式”，不出现功能标签英文直译；除非用户明确确认仅中文，否则不得缺少英文句式。
- 没有退化为白底闪卡、企业模板或低幼卡通。

任一核心项失败，按照 `qa-checklist.md` 记录 `S01`–`S08`，指出具体缺失项并只重做当前图片。
