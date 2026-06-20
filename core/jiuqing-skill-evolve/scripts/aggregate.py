#!/usr/bin/env python3
"""aggregate.py — 进化判分的确定性兜底。

它不调度 subagent、不打分（那是 agent 行为，由 SKILL.md 编排、且必须基于真实
跑出的产出）。它只做无法靠"脑补"蒙混的确定性部分：

  1. 校验每个 judge 的评分 JSON 来自真实文件、维度齐全、分值在 rubric 上限内；
  2. 每个 dimension 跨 judge 取 median、算 variance（判分噪声指标）；
  3. 与上一轮（baseline）对比，按阈值给出 keep / revert 建议，并标出 regression。

这样"判分必须基于真实采集的产出"被脚本卡住——judge 文件缺失或维度不全直接报错，
而不是被静默当作通过。阈值集中在此处定义，便于 threshold-calibration。

用法：
  python aggregate.py --judges r3_j1.json r3_j2.json r3_j3.json \
                      --baseline baseline.json \
                      --target-cluster conciseness single-source

judge JSON 格式（与 evaluation-rubric.md 一致）：
  {"conciseness": {"score": 5, "reason": "..."}, "single-source": {...}, ...}

baseline JSON 格式（本脚本上一轮的 --emit 输出，或首轮人工生成）：
  {"dimension_medians": {"conciseness": 4, ...}, "total": 86}
"""
import argparse
import json
import re
import statistics
import sys

# rubric 维度上限（与 evaluation-rubric.md 单一来源对齐；改 rubric 时同步改这里）
RUBRIC_MAX = {
    "trigger-clarity": 7, "step-verifiability": 7, "info-layering": 5,
    "single-source": 5, "conciseness": 6, "consistency": 5,
    "process-predictability": 15, "task-completion": 14, "failure-path-encoding": 10,
    "actionable-specificity": 6, "high-risk-blacklist": 5,
    "tooling-executability": 6, "threshold-calibration": 5, "failure-coverage": 4,
}

# 阈值（threshold-calibration：这些是默认值，应随实际 judge variance 校准——
# 若多轮 variance 普遍 > REGRESSION_DROP，说明阈值淹没在噪声里，需调大或增 judge）
KEEP_MIN_GAIN_BASE = 1.0  # 基线增益阈值；实际阈值随 baseline 动态缩放
REGRESSION_DROP = 2.0     # 任一非目标 cluster 维度跌幅超此值 → regression，建议 revert
HIGH_VARIANCE = 2.0       # 某维度 judge 间 variance（样本标准差）超此值 → 判分不可信


def dynamic_keep_threshold(base_total):
    """根据 baseline 总分动态计算 keep 阈值。

    高 baseline（≥90）的 skill 改进空间小，阈值应更宽松；
    低 baseline（<80）的 skill 改进空间大，阈值保持严格。

    公式：threshold = KEEP_MIN_GAIN_BASE * max(0.3, 1 - (base_total - 70) / 60)
    - baseline=70 → threshold=1.0（满空间，严格）
    - baseline=85 → threshold=0.625
    - baseline=95 → threshold=0.3（接近天花板，宽容）
    - baseline≥100 → threshold=0.3（下限）
    """
    scale = max(0.3, 1 - (base_total - 70) / 60)
    return round(KEEP_MIN_GAIN_BASE * scale, 2)


def normalize_judge_json(raw):
    """把各种非标 judge JSON 格式统一为平铺 dict：{dimension: {score, reason}}。

    处理：嵌套 dimensions、extra 字段、list 格式、未转义中文引号。
    """
    if isinstance(raw, list):
        # list of {dimension, score, ...} → 提取为 dict
        for item in raw:
            if isinstance(item, dict) and "dimension" in item:
                dim = item["dimension"]
                if dim in RUBRIC_MAX:
                    raw = {i["dimension"]: {"score": i["score"], "reason": i.get("reason", "")}
                           for i in raw if isinstance(i, dict) and i.get("dimension") in RUBRIC_MAX}
                    break
        else:
            return raw  # 无法转换

    if isinstance(raw, dict):
        # 嵌套在 "dimensions" 下 → 展平
        if "dimensions" in raw and isinstance(raw["dimensions"], dict):
            raw = raw["dimensions"]
        # 去掉非 rubric 字段
        raw = {k: v for k, v in raw.items() if k in RUBRIC_MAX}

    return raw


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        sys.exit(f"ERROR: 文件不存在 {path}（判分必须基于真实产出，不能跳过）")

    # 先尝试直接解析
    try:
        data = json.loads(content)
        return normalize_judge_json(data)
    except json.JSONDecodeError:
        pass

    # 尝试修复未转义的中文引号
    fixed = content
    fixed = re.sub(r'(?<=[^\x00-\x7f\\])"([^"]{1,40})"(?=[^\x00-\x7f\\])', r'\\"\1\\"', fixed)
    fixed = re.sub(r'(?<=[。！？；])"([^"]{1,40})"(?=[。，；\s])', r'\\"\1\\"', fixed)
    fixed = re.sub(r'(?<=[\s])"([^"]{1,40})"(?=[。，；])', r'\\"\1\\"', fixed)

    try:
        data = json.loads(fixed)
        return normalize_judge_json(data)
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: {path} 不是合法 JSON（修复后仍失败：{e}）")


def validate_judge(path, data):
    missing = [d for d in RUBRIC_MAX if d not in data]
    if missing:
        sys.exit(f"ERROR: {path} 缺维度 {missing}（judge 必须覆盖全部 rubric 维度）")
    for dim, entry in data.items():
        if dim not in RUBRIC_MAX:
            sys.exit(f"ERROR: {path} 含未知维度 {dim}")
        score = entry.get("score")
        if not isinstance(score, (int, float)):
            sys.exit(f"ERROR: {path}.{dim}.score 非数值")
        if not 0 <= score <= RUBRIC_MAX[dim]:
            sys.exit(f"ERROR: {path}.{dim}.score={score} 超出 [0,{RUBRIC_MAX[dim]}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judges", nargs="+", required=True, help="本轮各 judge 的评分 JSON")
    ap.add_argument("--baseline", help="上一轮 --emit 输出，用于对比；首轮可省略")
    ap.add_argument("--target-cluster", nargs="*", default=[],
                    help="本轮意图改进的 dimension cluster，这些维度不受 regression guard 约束")
    ap.add_argument("--emit", help="把本轮聚合结果写到该路径，作为下一轮 baseline")
    args = ap.parse_args()

    if len(args.judges) < 3 or len(args.judges) % 2 == 0:
        sys.exit(f"ERROR: judge 数={len(args.judges)}，需奇数且 ≥3（奇数使 median 唯一）")

    judges = []
    for p in args.judges:
        d = load_json(p)
        validate_judge(p, d)
        judges.append(d)

    medians, variances = {}, {}
    for dim in RUBRIC_MAX:
        scores = [j[dim]["score"] for j in judges]
        medians[dim] = statistics.median(scores)
        variances[dim] = statistics.pstdev(scores) if len(scores) > 1 else 0.0
    total = round(sum(medians.values()), 2)

    print(f"== 本轮聚合（{len(judges)} judge）==")
    noisy = []
    for dim in RUBRIC_MAX:
        flag = ""
        if variances[dim] > HIGH_VARIANCE:
            flag = f"  ⚠ variance={variances[dim]:.2f} 偏高，判分不可信"
            noisy.append(dim)
        print(f"  {dim:24} median={medians[dim]:<5} (max {RUBRIC_MAX[dim]}){flag}")
    print(f"  {'TOTAL':24} {total}")

    verdict = "KEEP"
    reasons = []
    if args.baseline:
        base = load_json(args.baseline)
        base_med = base.get("dimension_medians", {})
        base_total = base.get("total", 0)
        gain = round(total - base_total, 2)
        threshold = dynamic_keep_threshold(base_total)
        print(f"\n== 对比 baseline（{base_total} → {total}，gain={gain:+}，threshold={threshold}）==")

        regressions = []
        for dim in RUBRIC_MAX:
            if dim in args.target_cluster:
                continue
            drop = base_med.get(dim, medians[dim]) - medians[dim]
            if drop > REGRESSION_DROP:
                regressions.append(f"{dim} 跌 {drop:.1f}")
        if regressions:
            verdict = "REVERT"
            reasons.append("regression guard 触发：" + "；".join(regressions))
        if gain < threshold:
            reasons.append(f"gain {gain:+} < {threshold}（early-stop 信号，baseline={base_total}）")
            if verdict != "REVERT":
                verdict = "REVERT"
        if noisy:
            reasons.append(f"高 variance 维度 {noisy}，建议增 judge 复核而非直接 keep")
    else:
        print("\n（无 baseline，作为首轮基线）")

    print(f"\n建议：{verdict}")
    for r in reasons:
        print(f"  - {r}")

    if args.emit:
        with open(args.emit, "w", encoding="utf-8") as f:
            json.dump({"dimension_medians": medians, "total": total}, f,
                      ensure_ascii=False, indent=2)
        print(f"\n已写出 baseline → {args.emit}")


if __name__ == "__main__":
    main()
