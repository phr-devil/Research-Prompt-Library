# 11｜算法方框图的绘制：三步工作流

**科学正确 → 可验证的基础结构 → 有设计感的科研图**。三个 Prompt 均由用户发给 ChatGPT；第一步 ChatGPT 直接输出文字方案，第二/三步 ChatGPT **只生成给 Codex 的指令**，由 Codex 修改 HTML/SVG。

| 顺序 | 可复制提示词 | 输入 | 输出 |
|---|---|---|---|
| **Step 1** | [F11-A｜科学结构设计与文字蓝图](F11-A_科学结构设计与文字蓝图.md) | 论文方法、图的目的、参考图 | 核心模块/依赖/版式文字方案；**一次科学确认** |
| **Step 2** | [F11-B｜基础方框图 Codex 指令](F11-B_基础方框图_Codex指令生成.md) | Step 1 已确认蓝图 | ChatGPT 写 Codex 指令；Codex 生成基础 HTML/SVG 与结构基准 |
| **Step 3** | [F11-C｜设计增强与 SVG 资产 Codex 指令](F11-C_设计增强与SVG资产_Codex指令生成.md) | 蓝图、基础 HTML/SVG、审美参考图 | ChatGPT 写 Codex 指令；Codex 产出设计感更强的最终 HTML/SVG |

**只需一次核心人工确认**：用户审核 Step 1 的科学结构。Step 2、3 可在同一 Codex 工作区连续执行，优先复用已有代码与结构基准，减少重复阅读和 Token 开销。三步是质量分层，不是三个强制审批点。已有满意图的简单修复可直接走局部修改，无须重做三步。

## 科学结构与视觉设计的分界

- **Step 1** 确定科学节点、连接、公式、数据隔离和主要信息取舍；参考图只提供信息组织方式，不复制其内容。
- **Step 2** 用几何框、文字、箭头构建准确骨架，不使用插图素材；固定科学结构基准。
- **Step 3** 可充分进行版式重排、信息层级、容器区、留白、视觉动线和插图搭配；**不得改变科研节点、边及关键公式**。设计感不是换颜色或堆图标。

## SVG 资产（原样保留）

[资产清单](assets/manifest.json) · [授权与使用](assets/README.md) · [三套小图标](assets/icons/README.md) · [Robot Toast 角色](assets/robots/robot-toast/README.md)

当前 **56 个已批准 SVG**：Robot Toast 16、OpenMoji 4、Lucide 12、Tabler 12、Phosphor Duotone 12；SciSVG 未收录。素材只在 Step 3 按需加载；优先统一风格和许可合规，不要求用满。

[基础渲染示例](examples/render_demo.py) 是独立的线性 SVG/HTML 技术示例，不代表已经验证三步工作流效果。

**历史说明**：本次替换了旧 F11-A SAFE-Gait 专项修图提示词和旧 F11-B 一体化绘图提示词。旧内容仍可通过仓库 Git 提交历史恢复，不再作为当前默认入口。
