# Scoring Rubric（满分 100）

每轮按本表 score。structural dimension 靠静态分析判定；effectiveness dimension **必须实跑 test set 观察 agent 产出**，不能凭读 SKILL.md 想象。effectiveness 权重最高——格式合规但产出差仍为低分。

judge 统一输出 JSON：`{"dimension": {"score": 分, "reason": "依据"}, ...}`，便于多 judge 聚合。

## Structural dimensions（静态分析，共 40 分）

| dimension | 分值 | 判定标准 |
| --- | --- | --- |
| trigger-clarity | 8 | description 是否只写触发条件、能否让 agent 准确判断何时加载；概括了流程则扣分 |
| step-verifiability | 8 | 每步是否以可检验的完成标准收尾；标准模糊（"做好""处理一下"）扣分 |
| info-layering | 6 | 是否按紧迫度排序、随用随查内容是否下沉到指针后，避免正文臃肿 |
| single-source | 6 | 同一含义是否只定义一处，有无重复带来的维护冲突 |
| conciseness | 6 | 有无 no-op 句（模型默认即会做的废话）、有无堆砌雷同例子 |
| consistency | 6 | 术语是否统一、前后说法是否一致 |

## Effectiveness dimensions（必须实跑 test set，共 60 分）

| dimension | 分值 | 判定标准 |
| --- | --- | --- |
| process-predictability | 18 | 同类输入多次执行，agent 是否每次走相同*流程*（非相同结果）；流程发散扣分 |
| task-completion | 16 | 测试 prompt 产出是否真正满足要求、有无半途收工 |
| failure-path-encoding | 12 | 已知 failure path 是否被显式编码、被测时是否成功避开；只写"别犯错"不算 |
| actionable-specificity | 8 | 有无模糊措辞（"建议""可以考虑""视情况""灵活处理"）导致行为漂移 |
| high-risk-blacklist | 6 | 破坏性操作（`rm -rf`、`git reset --hard`、强推）是否被显式禁止 |

## Scoring discipline

- **judge ≠ editor** —— edit agent 不得给自己产出的改动 score，自评准确率不足以作 keep 依据。
- **no judge reuse** —— 每轮换一批 judge，避免 anchoring 上轮分数。
- **median aggregation** —— judge 取奇数个（≥3，奇数使 median 唯一），每个 dimension 取 median 再加总，比 mean 抗极端打分。
- **track variance** —— variance 大说明 judge 分歧大、该轮 gain 不可信，需增补 judge 或保守 revert。
