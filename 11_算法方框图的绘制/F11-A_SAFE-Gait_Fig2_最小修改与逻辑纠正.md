# F11-A｜SAFE-Gait Fig.2：HTML/SVG 算法框架图最小逻辑修正

> **场景**：已有满意的 HTML 内嵌 SVG 算法框架图，只允许极小范围修改，补足关键数据/模型依赖并保持视觉设计不变。
>
> **来源**：用户提供的 SAFE-Gait Fig.2 历史修图提示词，按 Markdown 文本排版整理；科研含义、操作范围和禁止事项均予保留。**这不是从零生成框架图的提示词。**

## 使用说明

将**待修改的原始 HTML 文件**与下方提示词一同交给能够读取和修改文件的 AI（例如 Codex/WorkBuddy）。输出只应是修改后的完整 HTML，不能额外导出 SVG、PNG 或 PDF。若输入版本已经包含两项指定依赖线，先核对是否已满足，避免重复叠加。

## 可直接复制的 Prompt

```text
请基于当前已有的 SAFE-Gait Fig.2 HTML 文件进行最小修改。

重要要求：

- 只修改 HTML 文件中的 SVG 代码。
- 先不要生成独立 SVG 文件。
- 先不要导出 PNG/PDF。
- 不要重新设计整张图。
- 不要改变现有配色、字体、尺寸、框体内容、方法名称和整体布局。
- 不要修改 CP / SB / DS / MCS 内部内容。
- 不要修改 Personalized prediction 中现有公式。
- 不要修改其他已有箭头，除非为了加入下面两条新依赖线而必须做极小位置调整。
- 修改完成后直接输出完整 HTML 代码。

需要修正两个原则性问题：

==================================================

1. 增加 query ground truth 到 Method comparison 的评价输入

==================================================

当前图中：
Personalized prediction → Method comparison

但是 Method comparison 中要计算 MAE / gain / harm，因此还需要真实 query ground truth y_qry。

请做以下修改：

1. 从 “Independent query pass B” 框单独引出一条虚线箭头，指向最右侧 “Method comparison” 框。
2. 这条虚线旁标注两行：
   Query ground truth y_qry
   (evaluation only)
3. 这条虚线只表示：
   query label 在 personalization 完成后，仅用于最终 evaluation。
4. 这条线不能进入：
   - One-shot personalization
   - CP / SB / DS / MCS
   - Personalized prediction
5. 保留现有：
   Query pass B → Personalized prediction
6. 最终 Method comparison 应同时接收：
   - Personalized prediction
   - Query ground truth y_qry（evaluation only）
7. 新增虚线尽量走图的下方或其他空白区域，避免压到文字和现有箭头。

==================================================

2. 增加 Frozen population state 对 query-side prediction 的依赖

==================================================

当前图中 Frozen population state 的：
Population model / normalization

只连接到了 calibration-side 的：
Population prediction and residual extraction。

但 query-side prediction 也必须使用相同的 frozen population model f(·) 和 training-only normalization。

请做以下修改：

1. 从 “Frozen population state” 再增加一条虚线 dependency arrow。
2. 该虚线直接指向：
   “Personalized prediction” 框。
3. 在线旁标注：
   Population model / normalization
4. 使用与现有 frozen-state dependency 完全一致的样式：
   - dashed line
   - 相同颜色
   - 相同线宽
   - 相同箭头样式
5. 这条线只表示 frozen model / normalization 对 query prediction 的依赖。
6. 不要让这条线进入：
   - Independent query pass B
   - One-shot personalization
   - Method comparison
7. 尽量从图上方或空白区域绕线，避免与已有文字、虚线和主流程箭头重叠。

==================================================

修改完成后检查

==================================================

最终图的逻辑必须保持为：

Calibration branch:
Unseen subject
→ Calibration pass A
→ Population prediction and residual extraction
→ One-shot personalization

Query branch:
Unseen subject
→ Independent query pass B
→ Personalized prediction

Frozen population state:
→ calibration-side population prediction
→ Personalized prediction

One-shot personalization:
→ Personalized prediction

Evaluation:
Personalized prediction
→ Method comparison

Query ground truth y_qry
→ Method comparison
(evaluation only)

必须确认：

- Query ground truth 不进入 personalization。
- 不出现 One-shot personalization → Query pass B 的顺序关系。
- 不修改现有其他算法逻辑。
- 不新增任何其他内容。

完成后只输出修改后的完整 HTML 代码。
```

## 本案例的核心验收

- 校准支路与 query 支路来自同一未见受试者，但必须是不同的物理 pass。
- Query ground truth 只在最终 Method comparison 中作为评价真值，不进入个性化或预测。
- Query-side prediction 复用 frozen population model 和 training-only normalization。
- 不改 CP / SB / DS / MCS 的内部内容、预测公式与原有布局；图的正确性必须核对实际 SVG 路径端点，而不是仅检查文字。

**适用边界**：本提示词针对 SAFE-Gait 特定 Fig.2 的局部纠错；其他论文必须先核实本身的计算图、数据泄漏边界和图形结构，不直接套用名称或箭头。
