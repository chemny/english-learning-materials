# 配图语义锁定

在生图前从已确认清单提取“词汇 → 核心对象或动作”表，并在同一批次、不同主题和双通道之间保持不变。画风可以变化，核心语义不得漂移。

## 选择顺序

1. 教材图片或上下文明确指定的对象或动作。
2. 当前句型和单元语境中最直接、最容易识别的对象。
3. 无明确语境时使用单一、具体、儿童可识别的默认语义。

避免用奖杯、礼物、笑脸等泛化装饰代替能够直接表达词义的对象。抽象词优先使用“人物动作＋一个辅助符号”，不要只画孤立符号。

## 常见默认语义

| 类型 | 词汇示例 | 默认核心画面 |
|---|---|---|
| 食物名词 | sandwich, salad, onion | 对应食物本体，完整、居中、无遮挡 |
| 动作 | drink, listen, help, share | 一名目标年龄学生执行该动作 |
| 身体与感受 | thirsty, hungry, tired | 学生动作或表情＋直接相关物件 |
| 品质 | healthy, helpful, polite | 学生执行能证明该品质的具体行为 |
| 偏好 | favourite | 学生指向或拥抱一个带小爱心标记的具体对象 |
| 关系 | dear, friend | 两名人物的关系动作或爱心信封；同批只选一种 |
| 程度与感官 | hot, sweet, delicious | 具体食物＋单一辅助符号，不用无关奖杯 |

## 易混词对照

同一张海报出现下列相近词时，必须用不同的“核心动作或状态证据”，不能只换人物衣服或饮料颜色。

| 易混词 | A 的固定证据 | B 的固定证据 |
|---|---|---|
| drink / thirsty | `drink`：手持明确饮料并正在喝，重点是动作或饮品 | `thirsty`：口渴表情、汗滴或寻找水，水瓶作为缓解对象 |
| healthy / delicious | `healthy`：运动、均衡食物或心电健康符号 | `delicious`：正在品尝具体食物并表现满意 |
| favourite / dear | `favourite`：从多个对象中选择一个，并用小爱心或星标强调偏好 | `dear`：爱心信封或两人亲密关系动作 |
| helpful / kind | `helpful`：实际递书、扶助或共同完成任务 | `kind`：安慰、分享或友善对待他人 |
| funny / happy | `funny`：做出逗笑他人的动作或场景 | `happy`：人物自身开心，不加入搞笑动作 |

## 提示词可见性分区

生图提示必须按以下顺序明确分区，不能把配图说明与可见文字写在同一行：

1. `VISIBLE TEXT — RENDER VERBATIM`：逐条列出唯一可见文字白名单。
2. `NON-VISIBLE VISUAL INSTRUCTIONS — NEVER RENDER AS TEXT`：逐条列出编号、词汇与配图语义映射。
3. `FORBIDDEN VISIBLE TEXT`：再次声明不得显示对象名称、动作说明、构图说明、风格词、颜色词和任务说明。

配图语义使用完整句子并带固定前缀，例如：

```text
NON-VISIBLE VISUAL INSTRUCTION 07 — healthy: illustrate a student exercising beside a small heart-health symbol. Never print this instruction, “student exercising”, or “heart-health symbol”. The card may show only its approved number, English word and Chinese meaning.
```

不得使用容易被模型当作图片标签的裸短语列表，例如 `salad bowl`、`tea cup`、`complete sandwich`。这些短语只能出现在带有 `NEVER RENDER AS TEXT` 的完整不可见指令中。

## 批量规则

- 主 Agent 在派发前冻结语义表并放进每个任务包。
- 同一批次的 `favourite`、`dear`、`healthy` 等抽象词不得在不同主题间改成完全不同对象。
- 参考图中的示例插图不能覆盖已确认语义，只影响媒介、构图和配色。
- 子 Agent 发现语义不够具体时停止该项并报告，不自行创造新的教材含义。
- 验收时同时检查单图词义正确和整组核心对象一致。
- 同一张图出现易混词时，必须按“易混词对照”检查其动作、状态和辅助物是否足以区分。
