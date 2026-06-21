[![English](https://img.shields.io/badge/English-blue.svg)](README.md)
[![中文](https://img.shields.io/badge/中文-red.svg)](README_zh.md)

---

# Skills

面向 AI agent 的跨平台技能库 —— 一处编写，处处可用。

## 为什么做这个项目？

AI 编码 agent（Codex、Claude Code、OpenCode 等）各自扫描自己的扁平 `skills/` 目录。为每个平台单独维护同一份能力既繁琐，又容易彼此走样。

本仓库是 skill 的**唯一真身**。每个 skill 是一个自包含的 `SKILL.md`；各平台通过软链指回这里，从而一处维护、多平台生效。技能之间通过 `depends` 字段声明依赖，运行时由 agent 按需加载依赖链。

## 特性

- 🧩 **可组合** —— 技能间通过 `depends` 互相引用，基础能力被复用而非复制
- 🔗 **唯一真身** —— 单一仓库，软链进每个平台的 skill 目录
- 🗂️ **三大领域** —— `core`（基础）、`dev`（开发）、`content`（内容）
- ✅ **执行前对齐** —— `jiuqing-idea-grill` 在任何不可逆动作前先拷问方案
- 🔒 **密钥安全** —— 生成脚本只从环境变量读密钥，绝不硬编码

## 技能目录

技能采用 `jiuqing-名词-动词` 的英文命名：固定前缀 `jiuqing` + 名词 + 动词，单词之间用连字符连接，全部小写，不使用缩写。目录名与 frontmatter 的 `name` 字段保持一致。

### core —— 基础能力

| 技能 | 功能 |
|------|------|
| `jiuqing-idea-grill` | 逐项拷问方案 / 需求 / 意图，对齐后再动手 —— 可直接调用，也可被其他 skill 通过 `depends` 引用作为执行前对齐环节 |
| `jiuqing-roles-debate` | 从多角色 / 多视角对产出物（文档、项目、代码、设计）多轮评审推演，直到得出共识结论 |
| `jiuqing-session-handoff` | 把当前会话压缩成交接文档，用于切换模型 / agent 平台或开新会话接力 |
| `jiuqing-skill-create` | 按标准格式新建一个 skill |
| `jiuqing-skill-evolve` | 基于评分反馈迭代改进、进化已有 skill |

### dev —— 开发能力

| 技能 | 功能 |
|------|------|
| `jiuqing-agents-inject` | 向项目的 AGENTS.md 注入 / 初始化 agent 行为规则 |
| `jiuqing-bug-diagnose` | 系统化定位与诊断顽固 bug 及性能回归 |
| `jiuqing-context-sync` | 提取领域概念，整理术语表 / CONTEXT.md，统一项目术语 |
| `jiuqing-goal-set` | 设定上线导向的项目目标，产出给 agent 的目标提示词 |
| `jiuqing-prd-write` | 把讨论落成 PRD / 产品需求文档 |
| `jiuqing-product-polish` | 自主迭代打磨项目，逼近可交付状态 |
| `jiuqing-project-ship` | 发版前全流程把关（安全、法律、质量、版本、文档） |

### content —— 内容能力

| 技能 | 功能 |
|------|------|
| `jiuqing-image-generate` | 根据文字提示词生成图片 |
| `jiuqing-video-generate` | 根据文字提示词生成视频片段 |
| `jiuqing-prompt-refine` | 把简短想法打磨成专业的图像 / 视频生成提示词 |

## 目录结构

```
skills/
├── core/       # 基础领域 — 通用能力，其他领域可组合调用
├── dev/        # 开发领域 — 需求分析、代码审查、发布检查等
├── content/    # 内容领域 — 提示词打磨、图片生成、视频生成等
├── scripts/    # 工具脚本（如 sync.sh 多平台软链）
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## SKILL.md 标准

每个 skill 必须遵循以下 frontmatter 格式：

```yaml
---
name: jiuqing-名词-动词
description: 一句话描述技能用途
category: core | dev | content
depends: []    # 可选，引用其他 skill 的 name
---
```

正文部分为 agent 执行的行为规范。

## 组合规则

- `core/` 下的 skill 是基础能力，其他领域可通过 `depends` 引用
- 组合 skill 在正文中显式说明调用了哪些基础 skill 的能力
- agent 运行时根据 `depends` 自行决定是否加载基础 skill

## 执行前对齐

`core/jiuqing-idea-grill` 提供"执行前先对齐信息"的能力：像面试一样逐个拷问方案与需求，达成共识后再动手。需要这一环节的 skill 在 `depends` 中声明 `jiuqing-idea-grill` 即可；不声明的固定脚本类 skill 直接执行，不触发对齐。

## 快速开始

### 前置条件

- `bash` 与 `git`
- 一个带扁平 `skills/` 目录的 agent 平台（Claude Code、Codex、OpenCode）

### 安装

```bash
git clone git@github.com:twmissingu/jiuqing-skills.git
cd jiuqing-skills
./scripts/sync.sh            # 为每个 skill 在各平台目录建软链
./scripts/sync.sh --dry-run  # 只预览将要做什么，不实际改动
```

脚本会软链到以下已存在的平台目录（不存在的自动跳过）：

| 平台 | 目录 |
|------|------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenCode | `~/.config/opencode/skills/` |

同名冲突时脚本只跳过并警告，绝不覆盖既有内容；重复运行幂等。

> zcode 走插件市场机制（非本地扁平目录），暂不通过软链纳入，需另行打包为插件。

### 保持最新

- **更新已有 skill 内容**：在本仓库 `git pull` 即可。软链指向真身，各平台自动用到最新。
- **新增 skill**：`git pull` 后重跑 `./scripts/sync.sh` 补上新软链。

## 给 AI Agent

1. **克隆并软链**
   ```bash
   git clone git@github.com:twmissingu/jiuqing-skills.git
   cd jiuqing-skills
   ./scripts/sync.sh
   ```
2. **发现** —— 技能位于 `core/`、`dev/`、`content/`，每个目录内含一个 `SKILL.md`，目录名即技能名。
3. **按需加载** —— 读 skill 的 frontmatter；若 `depends` 非空，先加载被引用的基础 skill。

注意：`jiuqing-image-generate` 与 `jiuqing-video-generate` 需要环境变量 `AGNES_API_KEY`。脚本只从环境变量读密钥，绝不从文件或参数读取。

## 贡献

用 `jiuqing-skill-create` 按标准格式新建 skill，再运行 `./scripts/sync.sh`。每个含义只在一处定义，遵循 [AGENTS.md](AGENTS.md) 的写作原则。

## License

[MIT](LICENSE)
