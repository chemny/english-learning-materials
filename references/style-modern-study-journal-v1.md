# `modern-study-journal-v1` 风格协议

使用这套协议生成结构清晰、课堂感强的现代学习手账式英语复习海报。参考图是可选增强素材，不是生成前提。

## 双通道

- `文字视觉 DNA`：始终可用，只根据本文件生成。
- `文字视觉 DNA + 参考图增强`：当下列资产存在且运行时支持图片输入时使用：
  `assets/style-references/modern-study-journal-v1.png`

不得因参考图缺失而停止生成。使用参考图时，只借鉴色彩系统、笔记本媒介、分层卡片、课堂场景和信息结构；不要复制其中的教材文字、人物、品牌、具体配图或独特内容组合。

## 视觉 DNA

- 画布：竖版，优先 3:4；运行时只支持 2:3 时允许 2:3。
- 背景：清爽冷白或中性白方格纸、点阵纸或笔记本纸，带克制纹理；不得使用发黄旧笔记本或全页奶油色覆盖层。
- 主色：深海军蓝与薄荷绿；辅色为明亮黄色、青蓝和少量珊瑚色，用于重点标记。
- 版式指纹：25%–29%头部、54%–58%词汇区和15%–19%底部是标准密度下的推荐起点。保持开放冷白方格纸、不对称标题与课堂锚点；人物数量和精确比例按内容负载调整。
- 标题：左侧深蓝大标题直接写在开放白色方格纸上；教材、PEP、年级和单元只使用小型深蓝或薄荷绿页签，英文主题使用局部黄色高亮条。禁止用一整块深蓝多边形、整列深蓝卡片或企业看板式色块包住全部标题。头部所有深蓝实色块合计不超过头部面积约18%，任何单个深蓝实色块不得横跨左侧标题区的大部分宽度。右侧课堂人物场景与标题同高，不能缩成小角标。
- 单元区：像学习手账的课程页签，与左侧标题组成一体；不要居中改成普通丝带。
- 内容区：16项使用4列×4行卡片，并按行使用低饱和浅黄、浅绿、浅蓝、浅紫四条圆角分组带；每格为独立近白学习卡，不增加全局虚线外框。每格只保留一个圆形编号，英文词汇本身不得带数字前缀，禁止出现“编号圆点＋1 sandwich”一类重复编号。
- 插图：统一使用干净的二维现代教育插画、轻水彩或轻纹理平涂，可包含目标年龄学生与真实课堂动作；人物比例自然，避免幼儿大头身。标题区人物、词卡人物和底部人物必须使用同一插画媒介，禁止照片感皮肤、摄影棚光照、三维渲染或半写实照片与手绘词卡混搭。
- 复习区：底部左侧是活页本或网格纸句型区，右侧是胶带固定的黄色便签提示卡，并辅以笔筒、书本、台灯或植物；保持桌面手账场景完整。黄色便签逐项显示中文学习功能和可直接套用的英文核心句式，不显示功能标签英文直译。
- 文字控制：装饰书本、笔记本封面、黑板、便签页签和文具不得自行出现科目名或口号；黄色知识便签必须逐字显示白名单中的知识提示，包括其中的加号、箭头或其他分隔符，不得用图标替换。
- 比例保护：人物、卡片、食物和文字保持自然宽高比；卡片等宽不代表内容强制铺满，插图采用contain并允许留白。
- 装饰：回形针、胶带、便签、荧光笔、铅笔线、箭头和小型课堂图标，数量克制。
- 年龄：按照 `age-adaptation.md` 调整人物、字体活泼度、卡片密度和课堂物件；年龄越高，装饰越克制、结构越成熟。

## 版式骨架

- `compact-grid`：16–20 项，4 列或紧凑模块网格，句型用底部高亮总结条。
- `standard-grid`：10–15 项，3 列模块卡片或主区加侧栏，保留学习提示与句型区。
- `large-card-grid`：6–9 项，2–3 列较大模块，仍需保留网格纸背景、页签标题、重点标记和总结区。

不要退化成儿童课堂剪贴画、纯白演示文稿、单调表格或松散的两栏人物卡。

## 核心风格提示块

把以下不可变风格锚点原样放入生图提示，再根据清单追加自适应版式说明：

```text
Style ID: modern-study-journal-v1.
Create a structured modern English-learning journal poster on fresh cool-neutral white grid or dot paper. Use deep navy and mint green with localized bright-yellow highlights, cyan details and very small coral accents. Preserve an open white-paper header with a bold title, compact course tabs and a classroom or study anchor; never enclose the entire title in a giant navy panel. Use one consistent 2D educational illustration medium, modular near-white learning cards and exactly one number badge per vocabulary item. Use notebook or sticky-note review language only when a review module is present in EXACT MODULES; a vocabulary-only poster must not invent bottom review text. Pair a Chinese learning function with its whitelisted English sentence frame only when the confirmed knowledge-tip module exists. Adapt exact card columns, character count and region proportions to the content load while keeping natural proportions and comfortable reading size.
Avoid translated metalinguistic labels, unconfirmed Chinese-only tips, giant dark-blue title blocks, corporate dashboard headers, yellow wash, aged paper, duplicate numbers, invented stationery text, photographic or 3D people mixed with drawings, toddler clip art, empty headers, generic ribbon headers, stretched content, generic bottom boxes and decorations that interrupt reading.
```

随后追加画布、版式骨架、年龄适配、内容映射和唯一可见文字白名单。

## 风格验收

- 冷白或中性白网格纸、点阵纸或笔记本媒介清晰可见，没有泛黄旧纸感。
- 深蓝、薄荷绿和明黄形成稳定的重点系统。
- 标题、页签、模块卡片和总结区构成明确学习路径。
- 页面以推荐比例为起点并按内容量自适应；开放白纸标题区、模块卡片和手账复习区形成清楚路径，课堂或学习锚点与内容不争抢空间。
- 头部是开放的冷白方格纸；标题直接落在白底上，深蓝只用于小型页签和文字，深蓝实色块合计不超过头部约18%，不存在包住整组标题的巨大蓝色面板。
- 人物和场景具有真实课堂感，年龄与学习者一致。
- 标题区、词卡和底部人物使用统一二维教育插画媒介，不得出现照片感或三维渲染人物。
- 便签、荧光标记或批注服务内容层级，不喧宾夺主。
- 黄色知识便签逐项使用“中文学习功能＋英文核心句式”，不出现功能标签英文直译；除非用户明确确认仅中文，否则不得缺少英文句式。
- 每张词卡只有一个圆形编号，英文词汇前没有重复数字。
- 没有退化成幼儿剪贴画、白底幻灯片或普通双栏闪卡。

任一核心项失败，按照 `qa-checklist.md` 记录 `S01`–`S08`，指出具体缺失项并只重做当前图片。
