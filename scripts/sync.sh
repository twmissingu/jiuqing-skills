#!/usr/bin/env bash
#
# sync.sh —— 把本仓库的 skill 软链到各 agent 平台的 skills 目录。
#
# 真身是本仓库（core/ dev/ content/ 下的每个 skill）。各平台扫描自己的扁平
# skills 目录，本脚本为每个 skill 在那里建一个软链指回仓库。
#
#   - 内容更新：在仓库 git pull 即可，软链指向真身，自动最新。
#   - 新增 skill：重跑本脚本补软链。
#
# 冲突处理：目标已存在同名项时——若已是指向本仓库的软链则跳过（幂等）；
# 否则跳过并警告，绝不覆盖（可能是其他来源的同名 skill）。
#
# 用法：
#   ./scripts/sync.sh            # 软链到所有已存在的平台目录
#   ./scripts/sync.sh --dry-run  # 只打印将要做什么，不实际操作

set -euo pipefail

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

# 仓库根目录（脚本在 scripts/ 下，根目录是其上一级）
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 各平台的扁平 skills 目录。不存在的平台会自动跳过。
TARGETS=(
  "$HOME/.claude/skills"          # Claude Code
  "$HOME/.codex/skills"           # Codex
  "$HOME/.config/opencode/skills" # OpenCode
)

# 收集仓库内所有 skill（含 SKILL.md 的目录），分类层 core/dev/content 下一级。
skill_dirs=()
for category in core dev content; do
  cat_dir="$REPO_ROOT/$category"
  [[ -d "$cat_dir" ]] || continue
  for d in "$cat_dir"/*/; do
    [[ -f "${d}SKILL.md" ]] || continue
    skill_dirs+=("${d%/}")
  done
done

if [[ ${#skill_dirs[@]} -eq 0 ]]; then
  echo "没有找到任何 skill（core/ dev/ content/ 下均无含 SKILL.md 的目录）。"
  exit 0
fi

linked=0; skipped=0; warned=0

for target in "${TARGETS[@]}"; do
  if [[ ! -d "$target" ]]; then
    echo "跳过不存在的平台目录：$target"
    continue
  fi
  echo "== 平台目录：$target =="
  for src in "${skill_dirs[@]}"; do
    name="$(basename "$src")"
    dest="$target/$name"

    if [[ -L "$dest" ]]; then
      # 已是软链——若指向本仓库则幂等跳过，否则警告不覆盖。
      current="$(readlink "$dest")"
      if [[ "$current" == "$src" ]]; then
        skipped=$((skipped+1))
        continue
      else
        echo "  ⚠ 跳过 ${name}：已有软链指向别处（${current}），不覆盖"
        warned=$((warned+1))
        continue
      fi
    elif [[ -e "$dest" ]]; then
      echo "  ⚠ 跳过 ${name}：目标已是真目录/文件（可能是别处来源的同名 skill），不覆盖"
      warned=$((warned+1))
      continue
    fi

    if [[ $DRY_RUN -eq 1 ]]; then
      echo "  [dry-run] 将软链 $name -> $src"
    else
      ln -s "$src" "$dest"
      echo "  ✓ 软链 $name -> $src"
    fi
    linked=$((linked+1))
  done
done

echo
echo "完成：新建软链 ${linked}，已存在跳过 ${skipped}，冲突警告 ${warned}。"
[[ $DRY_RUN -eq 1 ]] && echo "（dry-run，未实际改动）"
