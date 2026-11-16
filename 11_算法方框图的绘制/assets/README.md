# SVG 资产与复用规范

当前入库 8 个**原创 SVG**：4 个同一机器人风格的分析、检索、分配、提案场景，以及文档、数据库、传感器与 DAG 图标。每幅均为原生矢量路径（128×128），可离线内联到论文 SVG/HTML。

AI 应先从真实方法中凝练科学信息和模块/箭头，再在 [manifest.json](manifest.json) 按 `concepts` 检索素材 ID，只读取所选 .svg。通常整图 0–4 个插图，一个模块至多一个。没有合适素材可留白，不得为配图添加新的算法内容。

**素材来源**：本目录所有 SVG 都是本次原创绘制，并非复制用户参考图或第三方仓库。当前没有添加新的整体项目许可证；`license_status` 是来源说明。未来可参考 [Lucide](https://github.com/lucide-icons/lucide)、[Tabler](https://github.com/tabler/tabler-icons)、[DiceBear](https://github.com/dicebear/dicebear)，但需要逐项确认资源许可、署名、来源及 SVG 安全后才能正式引入，不能把其全部图标默认为自由商用。

[示例代码](../examples/render_demo.py) 说明如何内联资产到 SVG 和 HTML。此脚本仅用于简单横向示例，不替代科学方法分析。
