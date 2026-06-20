# 经验闭环：写 LOG，再用 LOG 自进化

本 skill 每进化完一个别的 skill，就把这次的实战经验追写进 `LOG.md`。攒够若干条后，**手动触发**一次自进化——把 LOG 里反复出现的坑当作 test set，按标准进化循环修自己。LOG 是"问题源"，进化循环是"修复手段"。

## 何时写 LOG

每次跑完 `jiuqing-skill-evolve` 的一次完整进化（无论 keep 还是全程 revert）后，在收尾阶段追写一条到同目录 `LOG.md`（不存在则创建）。这是流程的固定收尾，不是可选项。

## LOG 条目格式

每条一节，追写到文件末尾，**只追加不改旧条目**（旧经验是后续自进化的语料，改了等于篡改 test set）：

```markdown
## <日期> 进化了 <被改 skill 名>
- 结果：keep N 轮 / 全程 revert；baseline → 终值（holdout 总分）
- 有效的改法：哪类 edit 真带来 gain（具体到 dimension）
- 踩的坑：本次流程本身哪里出了问题（如 judge 脑补打分没实跑、阈值淹在噪声里、漏了某失败模式、cluster 划错把不相关维度算进去）
- 对本 skill 的改进线索：上面的坑指向 SKILL.md/rubric/脚本 该怎么改
```

"踩的坑"和"改进线索"是闭环的燃料——记的是**进化流程自身**的问题，不是被改 skill 的问题。

## 手动触发自进化（把 LOG 当 test set）

攒够经验（建议 ≥3 次进化记录）后，由用户手动触发"用 LOG 优化你自己"。此时**被进化对象就是本 skill 自己**（SKILL.md + rubric + 脚本），test set 来自 LOG：

1. **从 LOG 提炼 test prompt** —— 把"踩的坑"里**反复出现**的问题（出现 ≥2 次才算信号，单次可能是偶发）转成测试场景。例如多条都记"judge 没实跑直接打分"，就构造一道"agent 在判分步会不会跳过实跑"的 test prompt。切 train/holdout 同 `test-set-template.md`。
2. **把坑归类到 rubric 维度** —— 每个反复出现的坑对应一个最弱 dimension：判分悬空→`tooling-executability`，阈值拍脑袋→`threshold-calibration`，漏失败模式→`failure-coverage`，流程描述含糊致 agent 走偏→`actionable-specificity`。这一步让盲区进入 locate 视野。
3. **走标准进化循环** —— 按 SKILL.md ② 的 score→edit→re-score→keep/revert 修自己，judge≠editor 照旧。**自指注意**：本 skill 是多文件资产，一轮仍只动一处（某个文件的某个 cluster），改 rubric 时该轮 baseline 作废重新打（评分标准变了，前后不可比）。
4. **更新 LOG** —— 自进化本身也追一条 LOG，记下这次靠经验修了什么。

## 边界

- LOG 是经验语料，不是命令清单——提炼时要判断坑是真信号还是偶发，别把一次性意外当通则去改 skill。
- 自进化改不动的硬伤（如需新增平台相关基础设施）如实记进 LOG「改进线索」，留待人工处理，不强行用文字 edit 假装修好。
