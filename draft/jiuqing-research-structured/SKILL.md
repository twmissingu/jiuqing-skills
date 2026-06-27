---
name: jiuqing-research-structured
category: content
depends: [jiuqing-idea-grill]
description: 当用户说"帮我调研一下""查一下资料""做点研究""收集素材"时使用
---

# 结构化调研技能

## 流程

**Step 1 — 对齐目标**：调用 jiuqing-idea-grill 明确调研目标——要验证什么假设？最终要回答什么问题？

**完成标志**：输出一句话调研目标（如"验证X是否优于Y"或"回答X领域Y问题"），用户确认方向。

**Step 2 — 多渠道收集**：至少 3 个信源，组合使用 `web_search`、`web_extract`、站内搜索。

**完成标志**：收集到至少 3 个独立信源的信息，每个信源标注标题、来源类型、关键信息摘要。

**Step 3 — 事实交叉验证**：同一事实来自不同信源 → 可信度高；存在对立说法 → 标记为"矛盾"，列出双方出处，不下结论。

**完成标志**：每个核心发现标注可信度标记（🟢/🟡/🔴/⚠️），矛盾项列出双方出处。

**Step 4 — 存档**：按下方格式写入 `research-notes/`（agent 在项目根目录创建）。

**完成标志**：文件写入成功，输出存档路径。

## 输出结构

```
## 调研目标
一句话概括要回答的问题

## 核心发现（3–5 条）
1. **发现一**（出处：源A、源B）🟢
2. **发现二**（出处：源C）🟡
3. **发现三**（源D 说 X，源E 说 Y）⚠️矛盾

## 可信度总评
- 高：多源交叉验证一致 / 中：单源但可信 / 低：孤证、自媒体

## 未解决的问题 / 待验证

## 原文片段（可引用）
> "……" — 源A

## 原始链接
- [标题](url)
```

## 可信度标记

| 标记 | 含义 |
|------|------|
| 🟢 | 多源交叉验证一致 |
| 🟡 | 单源但可信 |
| 🔴 | 孤证 / 未核实 |
| ⚠️ | 不同来源说法冲突 |

## 存档 & 多轮调研

存档格式：`research-notes/YYYY-MM-DD-主题.md`。用户对任一发现追问"展开"时，进入该方向第二轮搜索，追加内容到同一文件，新增二级标题 `## 第二轮：<子方向>`。

## 边界

只做调研和整理（不做内容创作、不发布、不投稿），不替用户下结论——呈现事实与矛盾，让用户自己判断。
- 不做内容创作或文章撰写
- 不做发布或投稿
- 不替用户下结论或做决策
- 效果承诺禁止——不保证"调研结果100%准确"或"覆盖所有重要信源"

## 失败路径表

| 情况 | 信号 | 处理 |
|------|------|------|
| 调研范围过于宽泛 | 如"AI的未来""科技趋势"无具体方向 | 调用 idea-grill 收窄调研目标，明确要回答的具体问题后再执行 |
| 信源不足3个 | web_search 返回结果稀少或重复 | 如实报告当前信源数量和可信度限制，标注为🔴孤证，不捏造信源 |
| 信源间存在严重矛盾 | 多个权威来源给出对立结论 | 标记为⚠️矛盾，列出双方出处和依据，不下结论；在"未解决问题"中建议用户进一步验证 |
| 用户要求下结论或做推荐 | 出现"你觉得该选哪个""给个建议""下结论" | 拒绝——呈现事实与矛盾让用户自己判断，这是核心边界 |
| 用户要求写成文章发表 | 出现"写篇文章""整理成报告发表" | 拒绝内容创作和发布，只做调研存档 |
| idea-grill 对齐失败 | 依赖调用超时或报错 | 降级处理：从用户原始输入提取关键词作为调研方向，直接进入 Step 2 |

## 示例

用户请求："调研 Cursor 和 Claude Code 对比"。存档 `research-notes/2026-06-28-Cursor-vs-Claude-Code.md`：

```
## 调研目标
Cursor 和 Claude Code 在编码体验上的核心差异及各自适用场景

## 核心发现
1. **Cursor 是 IDE（VS Code 分支），Claude Code 是终端 Agent** — Cursor 提供完整 GUI，Claude Code 是 CLI 工具。🟢（Cursor官网、Anthropic 官方博客）
2. **Cursor 支持多模型切换**，Claude Code 固定使用 Claude 模型。🟢（双方文档）
3. **Claude Code 擅长深度 Agentic 任务**，Cursor Tab 补全更注重逐行体验。🟢（评测 A、B）
4. **价格差异大** — Cursor Pro $20/月，Claude Code 按 API 用量。🟡（官方定价页）

## 可信度总评
高 — 官方文档和多家独立评测交叉验证一致

## 未解决的问题
- 大规模 monorepo 下哪个更流畅？
- Claude Code long-running 稳定性如何？

## 原文片段
> "Cursor is an AI-first code editor built from VS Code…" — cursor.com
> "Claude Code is an agentic coding tool that lives in your terminal…" — docs.anthropic.com

## 原始链接
- https://cursor.com
- https://docs.anthropic.com/en/docs/claude-code/overview
- https://example.com/cursor-vs-claude-code-review
```
