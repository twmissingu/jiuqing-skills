# LOG · jiuqing-skill-evolve 进化记录

## 2026-06-20 进化了 jiuqing-image-generate
- 结果：keep 2 轮；baseline 69 → R1 92（+23）→ R2 精简正文（预估 93-94）
- 有效的改法：Round 1 补充 failure-path-encoding（失败路径表 +6 分）、high-risk-blacklist（安全约束 +3 分）、failure-coverage（+1 分）效果最显著；Round 2 下沉参考材料到 REFERENCE.md 改善 info-layering
- 踩的坑：judge 输出格式不统一（有的嵌套 dimensions、有的有 extra total 字段），aggregate.py 校验严格会报错；需要在 judge prompt 中明确指定平铺 JSON 格式
- 对本 skill 的改进线索：judge prompt 应加一句"输出平铺 JSON，不要嵌套在 dimensions 或其他 key 下"；或 aggregate.py 增加 format auto-detection

## 2026-06-20 进化了 jiuqing-video-generate
- 结果：keep 1 轮；baseline 93，补充失败路径表 + 安全约束 + REFERENCE.md
- 有效的改法：与 image-generate 同构——补 failure-path table（7 个场景）和安全约束，下沉 API 边界/设计 rationale 到 REFERENCE.md
- 踩的坑：judge1.json 有未转义的中文引号导致 JSON 解析失败，需要在 judge prompt 中强调"reason 字段内不要使用双引号包裹中文术语"
- 对本 skill 的改进线索：aggregate.py 可增加 JSON 自修复能力（自动转义常见问题）

## 2026-06-20 进化了 jiuqing-prompt-refine
- 结果：keep 1 轮；baseline 90，补充对抗性输入拒绝 + ②b 死循环兜底
- 有效的改法：在边界 section 补充 2 条 failure path（对抗性输入、②b 无限循环）
- 踩的坑：prompt-refine 的 process-predictability（12/15）主要来自 ②b 流程复杂度，纯文字改进难以大幅提升，需要更结构化的流程指引
- 对本 skill 的改进线索：高 baseline skill 的边际改进递减，投入产出比不如低 baseline skill

## 2026-06-20 进化了 jiuqing-idea-grill
- 结果：keep 1 轮；baseline 89，补充 3 个失败路径（用户拒绝对齐、极度模糊输入、中途切换需求）
- 有效的改法：新增"失败路径"表，把 3 个常见边界场景编码为信号→处理对
- 踩的坑：high-risk-blacklist 有 variance 警告（2.36），说明 judge 对该维度判定不一致——纯文档型 skill 的黑名单适用性确实模糊
- 对本 skill 的改进线索：variance 高的维度应增补 judge 或在 prompt 中给出更明确的判定锚点

## 2026-06-20 进化了 jiuqing-agents-inject
- 结果：keep 1 轮；baseline 91，补充 3 个失败路径（RULES.md 缺失、用户要求违规注入、规范已完整）
- 有效的改法：新增"失败路径"表，覆盖了 RULES.md 不可读和用户注入违规规则的场景
- 踩的坑：无
- 对本 skill 的改进线索：process-predictability（12/15）的增量合并步骤仍有发散风险，可考虑更明确的合并规则
