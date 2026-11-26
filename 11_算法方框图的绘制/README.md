# 11｜科研绘图：三步工作流

**科学蓝图 → 基础矢量图 → 全局设计与原生可编辑工程。** 用户依次向 ChatGPT 提供三组 Prompt：Step 1 输出蓝图，Step 2/3 输出可直接交给 Codex 的专项执行指令。仅 Step 1 需要一次科学确认，第三步内完成 Draw.io 及验收，不另设第四步。

| 阶段 | 输入与执行 | 必要输出 |
|---|---|---|
| [F11-A｜科学蓝图与视觉构思](F11-A_科学结构设计与文字蓝图.md) | 已有科研材料/参考图 → ChatGPT → 用户确认 | Figure Profile、Message、N/E/F、Visual Encoding、Layout、Risks |
| [F11-B｜基础结构与矢量实现](F11-B_基础方框图_Codex指令生成.md) | 已确认蓝图 → ChatGPT 自包含指令 → Codex | `figure_base.html`、`figure_base.svg`、`figure_structure.json`；预留原生可编辑性 |
| [F11-C｜全局设计与可编辑交付](F11-C_设计增强与SVG资产_Codex指令生成.md) | 蓝图、基础图、结构文件、审美参考 → ChatGPT 指令 → Codex | **`figure_final.html`、`figure_final.svg`、`figure_final.drawio`**；保留冻结结构、按需布局/主题/源文件 |

## 使用原则

- **科学与视觉解耦：** N/E/F 固定科学含义，不固定视觉对象数量、坐标和形状。允许共享连接、分组、标签、机制示意、公式和真实数据图；禁止虚构机制、因果和评价泄漏。P0 与已选 P1 保留；MUST_SHOW 可见表达，MUST_PRESERVE 遵守而不强制写字，OPTIONAL 按需，OMIT 不画。
- **自适应图形类型：** 支持 Graphical Abstract、算法架构、机制、实验流程、概念框架及结果图，可组合形式。根据核心创新和最终期刊尺寸选择构图，不机械堆方框。
- **上下文交接：** B 的指令完整转述蓝图和 Skill，无需 Codex 重读论文；C 必须给参考图可访问路径或具体视觉 brief，不能假设跨工具共享聊天。跨对话只交接确认蓝图和必要工程。
- **设计与实现：** 先构图和层级，再配色与局部形状，最后按需插画。同一论文复用主题。共享视觉布局/生成数据，或由 Draw.io 原生布局输出 SVG/HTML；简单图不强制额外工程。蓝图是最高科学基准，B 校验 JSON 转录后冻结并记录校验值；C 选择唯一视觉实现源，所有格式同步生成。原 `figure_structure.json` 不改写，最终视觉映射另记，按图号独立目录避免混用。
- **强制 Draw.io：** C 生成原生 `.drawio`，主要文字、节点、公式、数据图形可独立编辑，语义连接真实绑定；仅复杂局部插画允许内嵌 SVG，禁止整图单图片替代编辑工程。参考 [官方生成规范](https://www.drawio.com/docs/reference/diagram-generation/)。
- **验收与 Token：** 科学交接、参数化几何、真实数值、跨格式一致性、目标字号、Draw.io 原生编辑及视觉联合检查。工具可用时实际渲染、打开图像分析、修复再预览；仅文件存在不算通过。总状态 PASS（必要检查全通过）/PARTIAL（文件生成但必要验证未执行）/FAIL（已知缺陷）/BLOCKED（关键条件缺失）。不自动安装工具链、不反复读论文或增加普通视觉审批；缺少 Draw.io 或未通过必要门禁不得 PASS。

已有满意图或用户提供红框/箭头标注时，直接使用 C 的 REVISION MODE；定位问题、保留满意部分、清除批注、检查同类缺陷并同步最终格式，无须重新执行三步。

## 视觉规范与 SVG 资产（保留原样）

默认白底深字、细描边、适当圆角与留白，但不把这些作为强制形状。优先复用论文级 Figure Theme；没有时从 [科研配色 A/B/C 三方案](references/F11-C_科研配色方案_三套.md) 选择一套（默认 Paul Tol Pale），同一语义保持一致，不仅依靠颜色表达科学关系。

[完整 manifest](assets/manifest.json) · [版权与使用](assets/README.md) · [通用图标](assets/icons/README.md) · [Robot Toast](assets/robots/robot-toast/README.md)

已批准的 **56 个**：Robot Toast 16、OpenMoji 4、Lucide 12、Tabler 12、Phosphor Duotone 12；SciSVG 未入库。仅 Step 3 定向选择有语义价值的素材。

[render_demo.py](examples/render_demo.py) 是独立线性流程的基础 SVG 演示，不是完整 F11 实现，不生成最终 Draw.io，也不证明任何实际科研图已经通过验收。

设计优先级：科学正确性、核心科研表达与目标尺寸可读性 ＞ 清晰构图和视觉叙事 ＞ 装饰。原生可编辑工程及一致性为最终交付门禁。
