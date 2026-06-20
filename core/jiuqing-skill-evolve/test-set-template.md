# Test Set 切分（train / holdout）

在同一批 prompt 上既 edit 又 score，改动会 overfit 到该批 prompt——分数虚高、泛化未涨。故将 test set 切成两组：**holdout 全程不参与 edit 决策**，仅在 keep 判定时作 judge，用于识别"仅迎合 train"的 false positive。这是 true gain 不被 overfitting 稀释的纪律保障。

## 切分规则

- 准备 ≥6 道测试 prompt，覆盖多类 scene：normal、boundary、error-prone、adversarial。
- 随机切分：约 60% 入 train，40% 入 holdout；两组均需覆盖各类 scene，不可 train 全 normal、holdout 全 boundary。
- **train** —— 每轮 edit 时定位问题、观察效果，可反复跑。
- **holdout** —— 仅在 keep 判定上跑；判定依据为 holdout 总 median 是否上升。train 涨而 holdout 不涨即 overfitting，revert。

## 存储格式

存为 `.evolution/<skill-name>/test-set.json`（按需创建，不入库）：

```json
{
  "train": [
    {"id": "t1", "scene": "normal", "prompt": "……", "expect": "评分关注点"},
    {"id": "t2", "scene": "boundary", "prompt": "……", "expect": "……"},
    {"id": "t3", "scene": "error-prone", "prompt": "……", "expect": "……"}
  ],
  "holdout": [
    {"id": "h1", "scene": "normal", "prompt": "……", "expect": "……"},
    {"id": "h2", "scene": "adversarial", "prompt": "……", "expect": "……"}
  ]
}
```

- `scene` —— 场景类型，用于核对切分均衡。
- `expect` —— 该 prompt 的评分关注点（非标准答案），减少 judge 理解漂移。

## 使用纪律

- holdout 一旦定下，进化全程不看、不改；中途修改即污染 judge，本轮所有 keep 判定作废。
- test set 跨轮保持稳定以确保分数可比——不大幅重写、不替换已有 case。

## 增量更新（跨轮）

进化过程中 LOG 暴露的新 gap 可以补充到 test set，但必须遵守以下规则：

1. **只追加，不修改已有 case** —— 已有 case 的 prompt 和 expect 是跨轮可比的基准，改了就破坏可比性。
2. **新 case 来源必须是 LOG** —— 只把 LOG 中反复出现（≥2 次）的问题转为 test prompt，单次偶发不加。
3. **新 case 归入正确 split** —— 新 case 加入后，检查 train/holdout 的 scene 均衡性；若打破均衡则调整切分。
4. **新 case 需标注来源** —— 在 expect 字段中注明"来源：LOG <日期>"，便于追溯。
5. **单次最多追加 2 道** —— 防止 test set 膨胀导致评分成本失控。若需要加入更多，先删除同等数量的低价值 case。

增量更新后在 commit 中记录："test set +N case（来源：LOG），train/holdout 保持均衡"。
