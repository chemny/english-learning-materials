# 视觉风格与纯生图提示规范

视觉风格决定画面语言，年龄适配决定这种语言的成熟度。选定风格后，必须再读取 [age-adaptation.md](age-adaptation.md)，不得把“卡通”默认等同于“幼儿化”。

## 参考图优先判断

每次生图前按固定优先级解析风格输入：

1. 用户本轮提供且可读取的参考图。
2. 所选内置主题对应且真实存在的 `assets/style-references/*.png` 案例图。
3. 所选主题协议中的完整文字视觉 DNA 和核心风格提示块。

命中第1或第2项且运行时支持图片输入时，默认使用参考图的版式骨架、栏目比例、配色层级、信息密度和装饰节奏，同时替换其教材文字、人物和主题插图；不要退化成仅借鉴颜色。只有参考图不存在、不可读或运行时不支持图片输入时才进入第3项。进入第3项后继续生成，不询问用户补图，也不把缺图当成错误。

## 预设风格

### 手绘童趣

- 风格编号：`primary-handdrawn-poster-v1`。
- 完整文字视觉 DNA、版式骨架、负面约束和固定提示块见 [style-primary-handdrawn-v1.md](style-primary-handdrawn-v1.md)。
- 可选增强资产：`assets/style-references/primary-handdrawn-fresh-v2.png`。存在且工具支持时传入；不存在时按文字视觉 DNA 正常生成，不得报错或停止。
- 明亮中性象牙白背景，蜡笔、彩铅或轻水彩手绘质感；纹理集中在笔触，不给全页增加黄色旧纸滤镜。
- 蓝色与珊瑚橙为主色，搭配黄色和浅蓝装饰。
- 圆润标题字、虚线宫格、丝带、小星星、铅笔和儿童角色。
- 适合小学词汇复习海报和单元复习海报。

### 校园杂志风

- 风格编号：`campus-magazine-v1`。
- 完整协议见 [style-campus-magazine-v1.md](style-campus-magazine-v1.md)。
- 可选增强资产：`assets/style-references/campus-magazine-v1.png`。
- 深青绿与珊瑚红、柔和中性象牙白纸张、编辑网格和现代手绘插画。
- 适合小学中高年级、希望清爽成熟但仍保留亲和感的资料。

### 现代学习手账风

- 风格编号：`modern-study-journal-v1`。
- 完整协议见 [style-modern-study-journal-v1.md](style-modern-study-journal-v1.md)。
- 可选增强资产：`assets/style-references/modern-study-journal-v1.png`。
- 深蓝、薄荷绿与局部明黄，配合清爽冷白网格纸、页签、便签和模块化学习路径。
- 适合小学中高年级、课堂复习和强调结构化阅读的资料。

### 少年漫画海报风

- 风格编号：`youth-comic-poster-v1`。
- 完整协议见 [style-youth-comic-poster-v1.md](style-youth-comic-poster-v1.md)。
- 可选增强资产：`assets/style-references/youth-comic-poster-v1.png`。
- 紫蓝、亮青与局部暖黄，使用中性浅奶白背景、漫画分镜、斜切几何、局部网点和少年感人物。
- 适合小学高年级及初中；小学中年级使用时按照年龄协议降低棱角和视觉冲击。

### 用户参考图

- 风格编号：`custom-reference-v1`。
- 把每张输入图明确标为“风格参考”，说明借鉴的色彩、媒介、信息密度和版式特征。
- 不复制参考图中的人物、商标、教材标题、独特构图或可识别素材。
- 临时上传路径可能失效；若任务需要长期复用，先征得用户同意再保存合规资产。

## 选择建议与兼容说明

- 未指定风格时，优先推荐 `primary-handdrawn-poster-v1`；小学中高年级可根据内容气质推荐校园杂志风或现代学习手账风。
- `cartoon-classroom-v1` 和 `fresh-study-card-v1` 仅为历史清单兼容编号，不再向用户展示为可选主题。读取旧清单时分别建议迁移到 `modern-study-journal-v1` 和 `campus-magazine-v1`。
- 内置案例图是优先输入但不是必要条件。有图默认用参考图版式；无图时根据对应协议的完整文字视觉 DNA 和核心风格提示块继续生成。

核心风格提示块锁定媒介、主色、标题层级、边框拓扑、年龄气质和比例保护。协议中的精确区域比例、列数、人物数量与典型道具属于强默认值，按内容负载和参考图调整；不得为了凑齐道具而挤压学习内容。

## 纯生图默认规则

- 使用当前运行时可用的原生图片生成工具；在 Codex 中优先使用内置 `imagegen` 路径。
- 使用 `scientific-educational` 类型。
- 一张独立资料对应一次生成调用；批量任务逐张调用。
- 把清单里的文字作为逐字可见文本，不让模型自由补文案。
- 要求配图与词义一一对应，并避免水印、乱码、重复和无关装饰文字。
- 项目交付图片从默认生成目录复制到任务目录，保留原始生成结果，不覆盖已验收版本。
- 内置参考资产是优先但非必要条件：可用且工具支持时必须作为风格与版式参考传入；不可用时自动使用对应文字视觉 DNA，不能把缺图作为阻断项。

## 提示词骨架

```text
Use case: scientific-educational
Asset type: <资料类型与使用场景>
Primary request: 根据已确认的教材内容制作一张完整英语学习资料图片。
Input images: <如有，逐张标注为风格参考>
Subject: <单元主题与主要学习对象>
Learner age band: <清单中的学习者年龄段>
Character age and visual maturity: <人物年龄、比例、衣着和动作成熟度>
Scene and object maturity: <场景和物件适配>
Style/medium: <预设风格的核心描述>
Composition/framing: <尺寸、横竖版、标题区、内容区、句型区>
Color palette: <主色和辅助色>
Background and white balance: <主题规定的中性浅色背景；黄色只作局部强调；禁止全页黄色、棕褐色或复古旧纸覆盖层>
Typography and information density: <字号、行长和单页信息量>
Text (verbatim): <逐条粘贴唯一可见文字白名单>
Non-visible visual instructions: <逐条填写配图对象或动作；这些说明只决定画什么，绝不能显示为标签、注释或正文>
Constraints: 单词、释义、句型和配图一一对应；仅出现白名单文字；每张词卡只显示一个编号，英文词汇前不得再次添加数字；保持清晰可读。
Avoid: 拼写错误、乱码、重复编号、漏词、错译、错配、水印、品牌标识、清单外口号、yellow wash、sepia tone、vintage parchment、kraft paper、aged paper、brown color cast。
```

## 批量一致性

同一批次固定以下内容：

- 画面比例和像素目标。
- 色彩、媒介、线条和角色年龄段。
- 学习者年龄段及对应的人物、场景和装饰成熟度。
- 标题层级、宫格结构和页脚样式。
- 插图复杂度和单页信息密度。

允许变化：单元主题、词汇图标、标题和局部装饰。不要通过一次长提示词同时生成多张不同海报。
