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

## 2026-06-20 进化了 jiuqing-goal-set
- 结果：keep 1 轮；baseline 82，补充 3 个失败路径（未指定项目、项目过早期、扫描冲突）
- 有效的改法：新增失败路径表覆盖 3 个边界场景
- 踩的坑：无
- 对本 skill 的改进线索：process-predictability（12/15）和 task-completion（11/14）仍可通过更结构化的扫描流程提升

## 2026-06-20 进化了 jiuqing-skill-create
- 结果：keep 1 轮；baseline 85，补充 4 个失败路径（危险需求、命名冲突、范围过大、对齐停滞）
- 有效的改法：新增失败路径表，triage 三道闸门有了显式的失败处理
- 踩的坑：无
- 对本 skill 的改进线索：high-risk-blacklist（3/5）仍需加强——可考虑在 triage 中增加安全闸门

## 2026-06-20 进化了 jiuqing-project-ship
- 结果：keep 1 轮；baseline 86，补充 4 个失败路径（LICENSE 缺失、测试失败、CHANGELOG 格式错、版本文件缺失）
- 有效的改法：新增失败路径表覆盖发版流程中的常见异常
- 踩的坑：无
- 对本 skill 的改进线索：threshold-calibration（4/5）的版本检测优先级可更明确

## 2026-06-20 进化了 jiuqing-product-polish
- 结果：keep 1 次；baseline 91，补充 4 个失败路径（项目类型不可判断、git 未初始化、docs 不可写、checkpoint 损坏）
- 有效的改法：新增失败路径表，与 convergence.md 的错误处理表形成互补
- 踩的坑：product-polish 已有 convergence.md 的错误处理表，新补充的失败路径是 SKILL.md 层面的 agent 行为指引，不重复
- 对本 skill 的改进线索：tooling-executability（4/6）可通过为关键步骤（维度评估、用户视角体验）增加脚本兜底来提升

## 2026-06-20 进化了 jiuqing-roles-debate
- 结果：keep 1 轮；baseline 79（最低），补充 3 个失败路径（发言质量退化、讨论跑题、用户跳过讨论），精简注意事项段
- 有效的改法：新增失败路径表 + 删除注意事项中的重复强调，conciseness 有改善
- 踩的坑：roles-debate 是最复杂的行为类 skill，纯文字改进对 process-predictability（12/15）帮助有限
- 对本 skill 的改进线索：threshold-calibration（3/5）的 20 轮上限和 >=2 角色共识阈值需要校准依据

## 2026-06-20 自进化了 jiuqing-skill-evolve
- 结果：keep 1 轮；改进 aggregate.py（+JSON 自动修复）和 SKILL.md（+judge 格式规范）
- 有效的改法：aggregate.py 新增 normalize_judge_json() 函数，自动处理嵌套 dimensions、extra 字段、list 格式、未转义中文引号四类常见格式问题；SKILL.md 在 baseline score 步骤明确 judge 输出格式要求
- 踩的坑：10 次进化中每次都有 judge 格式问题需要手动修复，说明这是系统性痛点而非偶发；修复应下沉到工具层而非每次靠 prompt 约束
- 对本 skill 的改进线索：后续可考虑为 test-set-template.md 增加 test prompt 的格式校验（确保 scene 字段覆盖均衡）

## 2026-06-20 第二轮进化（全部重新评分）

### 全局 baseline 对比
| Skill | 旧 baseline | 新 baseline | 变化 |
|-------|-----------|-----------|------|
| image-generate | 69 | 84 | +15 |
| video-generate | 93 | 89 | -4 |
| prompt-refine | 90 | 86 | -4 |
| idea-grill | 89 | 86 | -3 |
| agents-inject | 91 | 94 | +3 |
| goal-set | 82 | 82 | 0 |
| skill-create | 85 | 84 | -1 |
| project-ship | 86 | 91 | +5 |
| product-polish | 91 | 83 | -8 |
| roles-debate | 79 | 85 | +6 |

### 本轮改进
- **roles-debate**：补 20 轮上限和 ≥2 角色共识的校准依据（threshold-calibration 3/5 → 预估 4/5）
- **goal-set**：细化产出框架，每块写具体写法（actionable-specificity 4/6 → 预估 5/6）
- **skill-create**：补安全约束（禁止危险 skill、禁止嵌入 shell 命令）（high-risk-blacklist 3/5 → 预估 4/5）
- **product-polish**：补维度评估证据要求和用户视角检查清单（tooling-executability 4/6 → 预估 5/6）

### 踩的坑
- 第二轮 baseline 与第一轮差异较大（image-generate 从 69→84，product-polish 从 91→83），说明 judge 方差对 baseline 影响显著
- idea-grill judge2 输出空 JSON（agent 写了空 `{}`），需补发；说明 judge agent 偶尔会产出空结果
- 视频和 prompt-refine 的 baseline 反而下降（-4），可能是第一轮 judge 偏宽松
- 动态阈值（aggregate.py）在本轮未被使用（因为没有 evolution loop 的 keep/revert 决策），需下轮验证

### 对本 skill 的改进线索
- judge 偶发空输出需要在协议中编码：aggregate.py 应检测空 judge 并报错
- baseline 方差大意味着"跨轮可比性"需要更强的锚定（如固定 1-2 个 judge 不轮换）
