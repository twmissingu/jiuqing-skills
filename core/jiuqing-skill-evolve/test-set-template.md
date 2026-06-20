# Test Set 切分（train / holdout）

在同一批 prompt 上既 edit 又 score，改动会 overfit 到该批 prompt——分数虚高、泛化未涨。故将 test set 切成两组：**holdout 全程不参与 edit 决策**，仅在 keep 判定时作 judge，用于识别"仅迎合 train"的 false positive。这是 true gain 不被 overfitting 稀释的纪律保障。

## 切分规则

- 准备 ≥6 道测试 prompt，覆盖多类 scene：normal、boundary、error-prone、adversarial。
- 随机切分：约 60% 入 train，40% 入 holdout；两组均需覆盖各类 scene，不可 train 全 normal、holdout 全 boundary。
- **train** —— 每轮 edit 时定位问题、观察效果，可反复跑。
- **holdout** —— 仅在 keep 判定上跑；判定依据为 holdout 总 median 是否上升。train 涨而 holdout 不涨即 overfitting，revert。

## 存储格式

存为同目录 `test-set.json`（按需创建，不入库）：

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
- test set 会过时：被改 skill 的能力边界变动时，先更新 test set 再继续，并在 commit 中记录。
