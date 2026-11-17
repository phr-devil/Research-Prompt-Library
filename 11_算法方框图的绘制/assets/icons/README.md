# F11｜已批准的通用技术 SVG（A/B/C）

| 组 | 原始系列 | 编号 | 资产目录 | 原始许可 | 建议用途 |
|---|---|---|---|---|---|
| A | Lucide | L01–L12 | [lucide/](lucide/) | [ISC](lucide/LICENSE) | 线条极简，论文技术型框架图优先 |
| B | Tabler Icons | T01–T12 | [tabler/](tabler/) | [MIT](tabler/LICENSE) | 工程拓扑、结构与分支 |
| C | Phosphor Duotone | P01–P12 | [phosphor-duotone/](phosphor-duotone/) | [MIT](phosphor-duotone/LICENSE) | 柔和双色，与 Robot Toast 小插图搭配 |
| D | SciSVG | — | **未入库** | — | 用户明确排除 |

每组原始 SVG 共 12 个，全部保持上游源码、viewBox 与几何路径不变。来源固定 Git commit、原文件路径、Blob SHA 和语义标签均见 [manifest](../manifest.json)。三个来源的 LICENSE 已原样保留在各目录。

## Agent 使用规则

1. 先确定真实算法的 P0/P1 结构，再考虑插图；不要为了使用素材而增加方框。
2. 一张论文图默认只用 **Lucide、Tabler、Phosphor 中的一套**通用图标。TECHNICAL 优先 Lucide，结构/拓扑可用 Tabler，ILLUSTRATED 可用 Phosphor + Robot Toast。OpenMoji 可作少量彩色强调。
3. 按 `concepts` 从 manifest 筛选，**只打开实际使用的 SVG 文件**；不全量读入 36 项。
4. 对原生 SVG 路径等比例缩放；线型的 `currentColor` 要显式继承合适颜色，Duotone 的 `opacity` 不能无故删改。嵌入含重复 ID 的多个 SVG 时须确保每个 ID 唯一且引用匹配。
5. 输出自包含、可编辑的 SVG 和 HTML，按对应许可证保留必要版权信息；源码与 LICENSE 可以通过本目录追溯。

**视觉策略不是“图标越多越好”。** 优先科学表达和留白，缺少图标时宁可不画。
