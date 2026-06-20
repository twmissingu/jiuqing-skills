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

## ① Setup（进化前一次性）

1. **single editable asset** —— 一次只 edit 一个 SKILL.md，改动才可归因。多个 skill 排队逐个进化。
2. **构建 test set 并切分** —— 写 ≥6 道测试 prompt（让 agent 实际执行该 skill 的典型场景），按 `test-set-template.md` 随机切成 **train** 与 **holdout**。holdout 全程不参与 edit 决策，仅在 keep 判定时作 judge；无 holdout 不许进化。
3. **baseline score** —— 派 ≥3 个 independent judge（judge ≠ 后续 edit agent），各按 `evaluation-rubric.md` 在 train 与 holdout 上实跑后 score。用 `scripts/aggregate.py` 校验各 judge 的评分 JSON、取每个 dimension 的 median、算 variance，并 `--emit` 出 baseline 文件。脚本会在 judge 文件缺失或维度不全时直接报错，挡住"跳过实跑、脑补打分"。
4. 🔴 **CHECKPOINT** —— 把 baseline 报告（各 dimension 分、最弱 dimension、variance）交用户，确认改进方向再继续。

## ② Evolution loop（每轮一次，可多轮）

> 一轮只 edit 一个 **dimension cluster**（rubric 内相关的一组 dimension）。最弱 dimension 常与相邻 dimension 强相关（如 step-verifiability 弱常伴 actionable-specificity 弱），单独改一个会被相关 dimension 拖回；按 cluster 联合 edit 才抓得住 true gain。联合 edit 有损坏其他 dimension 的风险，故配 **regression guard**。

1. **locate** —— 读最新 score，找出最弱 dimension 及其相关 cluster。本轮只动这一 cluster。
2. **edit** —— 对该 cluster 生成**一处**具体改动，落到实在措辞（不写"优化一下"这类空话），编辑 SKILL.md。
3. **commit** —— `git commit` 本轮改动，说明动了哪个 cluster、怎么改。
4. **re-score** —— 派**新一批** independent judge（不复用上轮 judge，避免 anchoring 上轮分数），train、holdout 上实跑后 score，用 `scripts/aggregate.py --baseline 上轮 --target-cluster 本轮簇` 聚合。脚本据 median 与上轮对比、算 gain、按阈值自动标出 regression 与高 variance。
5. **regression guard** —— 由 `aggregate.py` 落实：任一**非目标 cluster** 的 dimension median 较上轮跌幅 > 阈值（脚本内集中定义），即便总分上升也判 revert。
6. **keep / revert** —— 采纳脚本建议：keep 须 holdout gain ≥ 阈值、无 regression、variance 未告警。否则 `git revert`（**禁用 `git reset --hard`**，保留失败轨迹供分析）。keep 时把本轮聚合 `--emit` 为新 baseline；baseline 只锁定被 keep 过的最高分，revert 轮不污染 baseline。
7. **early-stop** —— 单轮 holdout gain < 1 分，或连续 2 轮无 keep，自动 early-stop。
8. 🔴 **CHECKPOINT** —— 展示本轮 diff、各 dimension 分变化、keep/revert 结论，由用户确认是否进入下一轮。

## ③ 交付前自检

每轮被 keep 的改动落地后，被改的 skill 须按 `jiuqing-skill-create` 的"④ 起草自检"清单逐条过。任一条不过，在下一轮将其作为目标 dimension 修掉。score 上升但自检不过的 skill 不算合格交付。

## ④ 收尾

- 复盘：从 baseline 到最终，holdout 总分增量、贡献最大的 cluster、被 revert 的轮次（失败轨迹也是产出）。
- 交付最终 SKILL.md、test-set.json、各轮分数轨迹，供用户复核 gain 真实可查。
- **写 LOG** —— 按 `self-evolve.md` 的格式，把本次进化的效果与踩过的坑追写进 `LOG.md`。这是固定收尾，不可跳过——它是后续自进化的语料。

## ⑤ 自进化（手动触发）

攒够进化经验后，由用户手动触发"用 LOG 优化你自己"。此时被进化对象是本 skill 自身，test set 由 `LOG.md` 里反复出现的坑提炼而来——把它们归类到对应 dimension（判分悬空→tooling-executability、阈值拍脑袋→threshold-calibration、漏失败模式→failure-coverage 等），再走 ②③④ 的标准循环修自己。完整规程与自指注意事项见 `self-evolve.md`。

## 红线（禁止）

- 同一 agent 既 edit 又 score（自评不足以作 keep 依据）。
- 用 `git reset --hard` 做 revert。
- 跳过 test set 直接 score，或让 holdout 参与 edit 决策。
- 一轮跨多个不相关 dimension cluster 乱改。
- 为凑分灌水。
- 静默吞掉异常（judge 超时、输出非 JSON 必须报出，不当作通过）。
