# Robot Toast · 16 SVG 姿态

用户已明确选择完整 16 姿态，全部来自 [Pratham2703005/robot-toast-package](https://github.com/Pratham2703005/robot-toast-package) 的固定提交 `8b57d204b2e1545de3b8aadbe3e49f872ba7b7de`。这一系列是算法图 **ILLUSTRATED** 模式的主角色库。

| [![base](base.svg)](base.svg) | [![base2](base2.svg)](base2.svg) | [![think](think.svg)](think.svg) | [![search](search.svg)](search.svg) |
| 通用 `base` | 通用变体 `base2` | 思考 `think` | 检索 `search` |
| [![type](type.svg)](type.svg) | [![validation](validation.svg)](validation.svg) | [![validation2](validation2.svg)](validation2.svg) | [![wave](wave.svg)](wave.svg) |
| 打字 `type` | 验证 `validation` | 验证变体 `validation2` | 挥手 `wave` |
| [![success](success.svg)](success.svg) | [![error](error.svg)](error.svg) | [![loading](loading.svg)](loading.svg) | [![headPalm](headPalm.svg)](headPalm.svg) |
| 成功 `success` | 错误 `error` | 运行中 `loading` | 扶额 `headPalm` |
| [![angry](angry.svg)](angry.svg) | [![angry2](angry2.svg)](angry2.svg) | [![shock](shock.svg)](shock.svg) | [![sleep](sleep.svg)](sleep.svg) |
| 生气 `angry` | 生气变体 `angry2` | 震惊 `shock` | 休眠 `sleep` |

## SVG 处理
- 原始姿态 SVG 嵌在 `src/robots/*.ts` 中，以 SVG 模板导出。本仓库已抽取为独立 SVG。
- 去掉 `width="100%" height="100%"`，保留原始 `viewBox`、原始路径及配色。
- 为每个文件的渐变及其他 `id` 加 `f11-robot-toast-<pose>-` 前缀，同时更新其 `url(#...)` 引用，避免内联到一张大型 SVG 时发生 ID 冲突。
- 未将项目的 toast UI、JavaScript 运行逻辑、CSS 或依赖引入 F11。
- SVG 仍需在真实论文绘图环境中检查渲染和排版；图形素材并不证明论文科学逻辑正确。

## 来源及许可

原项目 MIT 许可，保留 [LICENSE-MIT.txt](LICENSE-MIT.txt)；版权声明为 **Copyright (c) 2026 Pratham2703005**。每个姿态的原始 TS Blob SHA 和转换后 SVG Blob SHA 均记录在 [全库 manifest](../../manifest.json)。

**风格约束**：同一幅论文图优先使用 1–4 个语义恰当的 Robot Toast 姿态；不因为拥有 16 个姿态就全部绘制。研究方法图的科学结构仍由证据决定。
