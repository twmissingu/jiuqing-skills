---
name: jiuqing-skill-evolve
description: 当用户想优化、改进、进化某个已有 skill，或说"把这个 skill 优化一下""提升 skill 质量""让 skill 自己进化""评估并改进 skills"时使用。
category: core
depends: []
---

# jiuqing-skill-evolve

进化一个 skill，每轮只保留真正提升其质量的改动。循环：**score → edit → re-score → 优于上轮则 keep、否则 revert**。分数单调不降。

## 核心难点：区分 true gain 与 false positive

进化的唯一难点是判断每次 edit 是否真正提升了 skill。手段是评分：edit 前后各 score 一次，分数上升即认为有提升。但分数上升存在 **false positive**——分数涨了而 skill 真实能力未涨。false positive 若被 keep 会逐轮累积、稀释 **true gain**。本 skill 的全部约束都用于识别并剔除三类来源：

1. **scoring noise** —— 同一对象不同 judge 给分 variance 大，单个 judge 偶然宽松即产生虚高分。
2. **test-set overfitting** —— edit 可能只迎合固定的几道测试 prompt，换一批即失效。
3. **dimension negative correlation** —— 为提升某 dimension 的 edit 拖低了相关 dimension，net gain 为零仍被 keep。

后续每步对应堵住这三类来源。评分维度与权重见 `evaluation-rubric.md`，测试集切分见 `test-set-template.md`。

## 协议阈值校准

| 阈值 | 值 | 来源 |
|------|-----|------|
| KEEP_MIN_GAIN_BASE | 1.0 | aggregate.py 内定义，随 baseline 动态缩放 |
| REGRESSION_DROP | 2.0 | 2 分在 100 分制中为 2%，低于此为 judge 噪声 |
| HIGH_VARIANCE | 2.0 | 样本标准差 >2 说明 judge 分歧显著 |
| 跳过标准 | baseline ≥90 | ≥90 分的 skill 改进空间 <10%，投入产出比不划算 |
| 同一 cluster revert 次数上限 | 2 次 | 单次 revert 可能是误判，连续 2 次说明该方向推不动 |
| anchor judge | 1 个固定 | 抵消轮换 judge 方差，提供跨轮可比性锚点 |

## ① Setup（进化前一次性）

1. **single editable asset** —— 一次只 edit 一个 SKILL.md，改动才可归因。多个 skill 排队逐个进化。
2. **跳过判定** —— baseline ≥ 90 分的 skill 可跳过进化（改进空间极小，投入产出比不划算）；80-90 分的 skill 仍应尝试一轮进化；< 80 分的 skill 必须进化。
3. **构建或继承 test set** —— 若 `.evolution/<skill-name>/test-set.json` 已存在（上轮进化遗留），直接复用；若不存在，写 ≥6 道测试 prompt（让 agent 实际执行该 skill 的典型场景），按 `test-set-template.md` 随机切成 **train** 与 **holdout**。test set 跨轮保持稳定以确保分数可比；仅在 LOG 暴露新 gap 时按 `test-set-template.md` 的增量规则补充，不大幅重写。holdout 全程不参与 edit 决策，仅在 keep 判定时作 judge；无 holdout 不许进化。
3. **baseline 继承或新建** —— 若 `.evolution/<skill-name>/baseline.json` 已存在（上轮 keep 的最高分），直接作为本轮 baseline，无需重新打分。若不存在，派 ≥3 个 independent judge（judge ≠ 后续 edit agent），各按 `evaluation-rubric.md` 在 train 与 holdout 上实跑后 score，评分 JSON 存到 `.evolution/<skill-name>/`。judge 输出必须是**平铺 JSON**（`{"维度名": {"score": N, "reason": "..."}}`），不要嵌套在 `dimensions` 等 key 下；reason 字段内不要用双引号包裹中文术语。`scripts/aggregate.py` 会自动修复常见的格式问题，但仍建议 judge 严格按格式输出。脚本会在 judge 文件缺失或维度不全时直接报错，挡住"跳过实跑、脑补打分"。
4. **指定 anchor judge** —— 从 ≥3 个 judge 中指定 1 个为 **anchor judge**，固定贯穿该 skill 的所有进化轮次（不轮换）。anchor judge 的评分 JSON 用 `--anchor` 参数传给 `aggregate.py`，脚本会输出 anchor 的跨轮 gain。其余 2 个 judge 每轮换新。anchor judge 的作用：提供跨轮可比性锚点，抵消轮换 judge 带来的方差。anchor judge 的身份在进化开始时确定，写入 `.evolution/<skill-name>/anchor-id.txt`（仅记录 judge 编号，如 "judge1"）。
5. 🔴 **CHECKPOINT** —— 把 baseline 报告（各 dimension 分、最弱 dimension、variance）交用户，确认改进方向再继续。

## ② Evolution loop（每轮一次，可多轮）

> 一轮只 edit 一个 **dimension cluster**（rubric 内相关的一组 dimension）。最弱 dimension 常与相邻 dimension 强相关（如 step-verifiability 弱常伴 actionable-specificity 弱），单独改一个会被相关 dimension 拖回；按 cluster 联合 edit 才抓得住 true gain。联合 edit 有损坏其他 dimension 的风险，故配 **regression guard**。

1. **locate** —— 读最新 score，找出最弱 dimension 及其相关 cluster。本轮只动这一 cluster。
2. **edit** —— 对该 cluster 生成**一处**具体改动，落到实在措辞（不写"优化一下"这类空话），编辑 SKILL.md。
3. **commit** —— `git commit` 本轮改动，说明动了哪个 cluster、怎么改。
4. **re-score** —— 派 **2 个新 judge**（不复用上轮 judge，避免 anchoring 上轮分数）+ 保留 **anchor judge**（跨轮固定），共 3 个 judge。train、holdout 上实跑后 score，评分 JSON 存到 `.evolution/<skill-name>/`，用 `scripts/aggregate.py --baseline .evolution/<skill-name>/baseline.json --target-cluster 本轮簇 --anchor .evolution/<skill-name>/anchor-<轮次>.json` 聚合。脚本据 median 与上轮对比、算 gain、按阈值自动标出 regression 与高 variance，并输出 anchor judge 的跨轮 gain。
5. **regression guard** —— 由 `aggregate.py` 落实：任一**非目标 cluster** 的 dimension median 较上轮跌幅 > 阈值（脚本内集中定义），即便总分上升也判 revert。
6. **keep / revert** —— 采纳脚本建议：keep 须 holdout gain ≥ 阈值、无 regression、variance 未告警。否则 `git revert`（**禁用 `git reset --hard`**，保留失败轨迹供分析）。
   - **keep 后**：把本轮聚合 `--emit` 为 `.evolution/<skill-name>/baseline.json`，然后**回到步骤 1 开始下一轮**（locate 新的最弱 cluster → edit → re-score → …）。循环直到 early-stop。
   - **revert 后**：baseline 不变，**回到步骤 1 重新 locate**，换一个不同的 cluster 尝试。同一 cluster 连续 revert 2 次则跳过该 cluster。

> 🔴 **GATE — 循环续接检查（步骤 6 之后必须执行）**：
> 完成 keep/revert 后，**逐条回答以下问题**（不可跳过、不可凭印象回答）：
> 1. 本轮 holdout gain 是多少？是否 < 动态阈值？ → gain < 阈值则停止，进入 ③
> 2. 被 edit 的 cluster 名是什么？该 cluster 已连续 revert 几次？ → 连续 2 次则停止，进入 ③
> 3. 已尝试过的 cluster 列表是？是否还有未尝试的 cluster？ → 全部尝试过则停止，进入 ③
> **以上三条答案均为"不满足停止条件" → 写出下一轮要 edit 的 cluster 名，然后回到步骤 1。** 如果你发现自己想停下来但无法回答这三个问题中的任何一个，这是协议违反——继续循环。

7. **early-stop** —— 满足 GATE 任一条件即停止循环。
8. 🔴 **CHECKPOINT** —— 展示本轮 diff、各 dimension 分变化、keep/revert 结论，由用户确认是否进入下一轮。

## ③ 交付前自检

每轮被 keep 的改动落地后，被改的 skill 须按 `jiuqing-skill-create` 的"④ 起草自检"清单逐条过。任一条不过，在下一轮将其作为目标 dimension 修掉。score 上升但自检不过的 skill 不算合格交付。

## ④ 收尾

- 复盘：从 baseline 到最终，holdout 总分增量、贡献最大的 cluster、被 revert 的轮次（失败轨迹也是产出）。
- 交付最终 SKILL.md、`.evolution/<skill-name>/test-set.json`、各轮分数轨迹，供用户复核 gain 真实可查。
- **写 LOG** —— 按 `self-evolve.md` 的格式，把本次进化的效果与踩过的坑追写进 `LOG.md`。这是固定收尾，不可跳过——它是后续自进化的语料。

## ⑤ 自进化（手动触发）

攒够进化经验后，由用户手动触发"用 LOG 优化你自己"。此时被进化对象是本 skill 自身，test set 由 `LOG.md` 里反复出现的坑提炼而来——把它们归类到对应 dimension（判分悬空→tooling-executability、阈值拍脑袋→threshold-calibration、漏失败模式→failure-coverage 等），再走 ②③④ 的标准循环修自己。完整规程与自指注意事项见 `self-evolve.md`。

## ⑥ 批量进化（多 skill 排队）

当用户要求进化多个 skill 时（如"把所有 skill 都进化一遍"），按以下流程组织：

1. **排队** —— 按复杂度从低到高排序（脚本类 → 文档类 → 行为类 → 自进化），先处理简单的积累 LOG 经验，最后处理复杂的。自进化永远放最后。
2. **逐个执行，禁止并行** —— 每个 skill 走完整的 ①→②→③→④ 流程。**一个 skill 完成全部循环（直到 early-stop）并写完 LOG 后，才开始下一个。** 禁止同时对多个 skill 启动进化流程——并行进化会导致 judge 混淆、改动归因不清、上下文超载。
3. **单 skill 内可并行 judge** —— 同一个 skill 的 3 个 judge（含 anchor）应并行派发以节省时间，但不同 skill 的 judge 不得并行。
4. **共享 LOG** —— 所有 skill 的进化经验追写到同一个 `LOG.md`，每条标注被改 skill 名。LOG 是全局语料，不按 skill 隔离。
5. **batch checkpoint** —— 每完成 3-4 个 skill 做一次批量 checkpoint：展示已进化 skill 的 baseline→终值对比、总体进展、剩余 skill 列表。让用户决定是否继续。
6. **test set 复用** —— 同类 skill（如 image-generate 和 video-generate）的 test set 可参考但不直接复用——它们的 API 调用方式相似但参数和边界不同。

## 红线（禁止）

- 同一 agent 既 edit 又 score（自评不足以作 keep 依据）。
- 用 `git reset --hard` 做 revert。
- 跳过 test set 直接 score，或让 holdout 参与 edit 决策。
- 一轮跨多个不相关 dimension cluster 乱改。
- 为凑分灌水。
- 静默吞掉异常（judge 超时、输出非 JSON 必须报出，不当作通过）。
- **同时对多个 skill 启动进化流程**（必须一个完成后再开始下一个）。
- **在 GATE 检查不满足 early-stop 条件时宣布完成**（必须回到步骤 1 继续循环）。

## 失败路径

| 场景 | 信号 | 处理 |
|------|------|------|
| edit 后想跳过 re-score 直接提交 | agent 觉得改动小不需要重新评分 | 红线禁止。每次 edit 后必须 re-score，无例外 |
| keep 后想宣布完成 | agent 觉得"已经改进了，够了" | 检查 GATE：若不满足 early-stop 条件则必须回到步骤 1 |
| revert 后想跳到下个 skill | agent 觉得这个 skill 改不动了 | 回到 locate 换 cluster 重试，同一 cluster 连续 revert 2 次才跳过 |
| 想并行处理多个 skill | agent 觉得这样效率高 | 红线禁止。并行导致 judge 混淆和改动归因不清 |
| judge 输出空 JSON 或超上限分数 | aggregate.py 报错 | 补发 judge；检查 prompt 是否明确写了分数上限 |
| 用户说"不用评分了直接改" | 用户要求跳过评分步骤 | 解释评分是进化的基础，跳过评分的改动无法验证真伪 |
