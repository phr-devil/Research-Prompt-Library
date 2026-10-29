# 中断与恢复合同（参考 GSD 持久状态和 Autoresearch 有界实验记录）

1. **检查**：读取 STATE 中最后可信工作点，进程/锁、已结束的 Run ID、日志尾部、数据/配置/代码哈希、checkpoints 与当前资源预算。只读识别后才做任何改动。
2. **分类**：每项执行标记 COMPLETE（有效完成）、PARTIAL（可续但证据不完整）、INVALID（数据/协议失效）、CRASH（运行异常）、BLOCKED（缺证据/权限）。科学结果 SUPPORTED/REFUTED/INCONCLUSIVE 与执行状态分开。
3. **最小恢复**：COMPLETE 不重做；PARTIAL 仅续未完成片段且要求 checkpoint/配置身份一致；INVALID 不能复活为 PASS；CRASH 优先最小复现并有限重试；BLOCKED 只申请必要条件。
4. **授权与预算**：恢复并不增加原预算；累计 wall-time/GPU-time/费用/尝试次数必须含已发生部分。没有明确的剩余额度不新开 GPU 运行。禁止以删除旧 run 或重置 hash 规避上限。
5. **交付**：记录 `RECOVERED/WAITING_AUTH/BLOCKED`、已复用的 Run ID、实际剩余额度、受影响 Claim、下一步唯一任务和本次写入文件；既存冻结证据保持只读。
6. **无长篇重读**：先 STATE 与相关差量；仅在异常无法定位时展开原始日志。恢复不是强迫所有研究执行新模板。
