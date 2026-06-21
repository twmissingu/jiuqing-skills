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

### 第二轮 keep/revert 决策
- **roles-debate**：REVERT（85→83，-2 regression）。阈值校准改动导致 process-predictability 下降，回滚。
- **goal-set**：KEEP（82→88，+6）。产出框架细化有效，actionable-specificity 提升。
- **skill-create**：KEEP（84→89，+5）。安全约束有效，high-risk-blacklist 提升。
- **product-polish**：KEEP（83→85，+2）。评分证据要求有效，tooling-executability 提升。

### 第二轮教训
- roles-debate 的阈值校准改动（加 ≥2 共识规则）反而降低了流程可预测性——新规则引入了额外分支但未被 agent 可靠遵循
- goal-set judge1 连续两次给"不适用"维度打 15 分（超过该维度满分），说明 judge prompt 对"不适用按满分计"的表述需要更精确
- 6 个未改动 skill（baseline 84-94）确认无需本轮进化

### 第二轮暴露的协议缺陷（待 skill-evolve 修复）
1. **keep/revert 后未继续循环** —— protocol 写了 early-stop 条件（gain < 阈值或连续 2 轮无 keep），但 agent 在第一次 keep 后就停止了，没有继续 edit→re-score→keep/revert 循环。原因：SKILL.md 的 ② Evolution loop 描述了单轮流程，但没有显式写"keep 后回到第 1 步继续下一轮"。agent 把"一轮 keep"当成了"完成"。
2. **"连续 2 轮无 keep"的 early-stop 条件无意义** —— 当前协议是每轮 edit 后立即 re-score 并 keep/revert。如果第一轮就 early-stop（gain < 阈值），根本没有"连续 2 轮"可言。early-stop 条件应改为"单轮 gain < 阈值"即可。
3. **revert 后的处理路径未编码** —— roles-debate REVERT 后，agent 直接提交了 revert commit 然后跳到下个 skill，没有尝试换一个 cluster 重新 edit。revert 后应该回到 locate 步骤找下一个最弱 cluster 再试。
4. **"无需进化"的判定标准缺失** —— 对于 baseline ≥ 84 的 6 个 skill，agent 直接跳过了，没有走任何进化流程。但 protocol 没有定义"什么条件下可以跳过"。应该明确：baseline ≥ 90 可跳过；80-90 之间仍应尝试一轮进化。

### 第二轮 Round 2 keep/revert 决策
- **goal-set**：KEEP（88→94，+6）。失败路径补充有效，failure-path-encoding 提升。
- **skill-create**：REVERT（89→85，-4）。自检验证步骤的 grep/find 操作反而降低了 step-verifiability——agent 被具体命令干扰了对核心流程的关注。
- **product-polish**：KEEP（85→89，+4）。convergence.md 阈值校准表有效，threshold-calibration 提升。

### 协议修复已落地
- SKILL.md ② 步骤 6：keep 后显式写"回到步骤 1"
- SKILL.md ② 步骤 7：early-stop 简化为"单轮 gain < 阈值"
- SKILL.md ② 步骤 6：revert 后回到 locate 换 cluster
- SKILL.md ①：新增跳过标准（baseline ≥90 可跳过）

## 2026-06-20 自进化（三项协议强化）

### 改进内容
1. **GATE 检查点**：在 ② Evolution loop 步骤 6 后加了强制检查点，逐条检查 early-stop 条件，不满足则必须回到步骤 1。新增红线："在 GATE 检查不满足 early-stop 条件时宣布完成"。
2. **Anchor judge**：① Setup 新增步骤 4（指定 anchor judge），固定贯穿同一 skill 所有轮次。aggregate.py 新增 `--anchor` 参数，输出 anchor 的跨轮 gain 用于稳定对比。② 步骤 4 改为"2 新 judge + anchor judge"。
3. **批量禁止并行**：⑥ 批量进化步骤 2 从"逐个执行"改为"逐个执行，禁止并行"，明确"一个 skill 完成全部循环并写完 LOG 后才开始下一个"。新增红线："同时对多个 skill 启动进化流程"。

### 驱动力
两轮实战中 agent 反复违反协议：跳过 re-score、keep 后停止循环、并行处理 10 个 skill。文字描述不够，需要结构性约束（GATE 检查点）和显式禁止（红线）。

## 2026-06-20 自进化（完整循环）

### Baseline
- 总分：76/100（< 80，必须进化）
- 最弱 dimension：threshold-calibration=2/5, failure-coverage=2/4
- anchor judge：judge1

### Round 1
- cluster：threshold-calibration + failure-coverage + actionable-specificity
- edit：新增阈值校准表（6 个阈值+来源）+ 失败路径表（6 个场景）
- 结果：76→86（+10），anchor 79→87（+8）→ **KEEP**
- 有效：阈值校准表（threshold-calibration 2→4）和失败路径表（failure-coverage 2→3）效果显著

### Round 2
- cluster：actionable-specificity + conciseness
- edit：GATE 检查点从抽象描述改为具体操作清单
- 结果：86→85（-1）→ **REVERT**
- 原因：GATE 改动虽然让措辞更具体，但增加了正文长度和阅读复杂度，process-predictability 从 13 降到 12

### GATE 检查
- gain=-1 < threshold=2.13 → early-stop 条件满足，停止循环

### 终值
- baseline=76 → 终值=86，净增 +10
- 最大贡献 cluster：threshold-calibration + failure-coverage（+7 分）

### 对本 skill 的改进线索
- aggregate.py 的 `--baseline` 对比有 bug（显示 baseline=0），需要修复
- Round 2 的失败说明：让 GATE 更"具体"不一定提升 actionable-specificity，反而可能增加复杂度损害 process-predictability

## 2026-06-20 进化了 jiuqing-context-sync
- 结果：跳过进化；baseline 93（≥90），符合跳过标准
- 有效的改法：无（未执行进化）
- 踩的坑：无
- 对本 skill 的改进线索：baseline ≥90 的 skill 改进空间极小（<10%），投入产出比不划算。该 skill 已在起草时内置了失败路径表、安全约束、可检验完成标准，无需额外进化。

## 2026-06-21 进化了 jiuqing-prd-write
- 结果：keep 1 轮；baseline 89 → R1 92（+3）→ R2 REVERT（-1），终值 92
- 有效的改法：Round 1 改进 actionable-specificity + failure-coverage cluster——把 seam 划定的模糊措辞（"尽可能高位"、"理想是1个"）改为具体规则（复用优先、高位切入、数量控制≤3），补充 4 个失败路径（用户矛盾、模板不适用、中途改主意、要求写代码）
- 踩的坑：Round 2 精简定位段（合并两段为一句话）反而导致 conciseness 从 6 降到 5、info-layering 从 5 降到 4，说明"定位"和"边界"的分离对读者理解有独立价值，不宜为了精简而合并
- 对本 skill 的改进线索：failure-coverage 仍是 3/4，可考虑补充"PRD 过长超出 token 限制"和"用户要求修改已写好 PRD"两个失败路径；conciseness 5/6 有提升空间但需更精细的删减策略，不能靠合并段落

## 2026-06-21 进化了 jiuqing-session-handoff
- 结果：跳过进化；baseline 97（≥90），符合跳过标准
- 有效的改法：无（未执行进化）
- 踩的坑：无
- 对本 skill 的改进线索：baseline 97 分极高，几乎所有维度满分或接近满分。唯一扣分点是 process-predictability（14/15），因为"文档结构参考"的"不必拘泥"措辞引入轻微输出变异。但这是合理的设计选择——交接文档应按焦点裁剪，不应强制统一格式。

## 2026-06-21 进化了 jiuqing-bug-diagnose
- 结果：keep 1 轮；baseline 82 → R1 87（+5）→ R2 REVERT（+0），终值 87
- 有效的改法：Round 1 改进 high-risk-blacklist + failure-coverage cluster——补充禁止破坏性操作（rm -rf、git reset --hard、force push），补充 5 个失败路径（环境差异、外部依赖、工具链故障、范围蔓延、不可修复）
- 踩的坑：Round 2 改进 threshold-calibration（为 2秒/30秒、50%/1% 阈值添加校准依据）没有带来分数提升（gain=+0），说明这些阈值虽然缺乏显式校准依据，但 judge 认为它们在调试领域是合理的经验启发式
- 对本 skill 的改进线索：tooling-executability 仍是 4/6（或 3/6），作为纯流程型 skill 这是合理的——执行依赖 agent 的工具使用能力而非预置脚本。actionable-specificity 5/6 可通过更具体的降级策略提升

## 2026-06-21 自进化了 jiuqing-skill-evolve
- 结果：keep 1 轮；baseline 91 → R1 92（+1）→ R2 REVERT（-8），终值 92
- 有效的改法：Round 1 改进 tooling-executability + step-verifiability cluster——为 edit 步骤添加可验证的改动类型（失败路径、阈值校准、精简合并），为 re-score 步骤详细描述 aggregate.py 的 5 项功能
- 踩的坑：Round 2 改进 info-layering（精简 anchor judge 描述）导致分数大幅下降（-8），说明 anchor judge 的描述虽然有冗余，但删除后反而降低了信息密度——judge 认为冗余是必要的上下文
- 对本 skill 的改进线索：baseline 92 分很高，改进空间有限。info-layering 4/5 和 failure-coverage 4/4 都是高分，精简反而可能损害信息完整性。tooling-executability 5/6 是当前最弱维度，但作为依赖外部脚本的 skill 这是合理的——除非把脚本内嵌，否则难以进一步提升
