# Skills

Agent 通用技能库。

## 设计理念

每个 skill 是一个独立的 `SKILL.md` 文件，可跨平台使用（Codex、Claude Code、OpenCode 等）。技能之间通过 `depends` 字段声明依赖关系，组合调用时由 agent 自行加载。

## 命名规则

技能采用 `jiuqing-名词-动词` 的英文命名：固定前缀 `jiuqing` + 名词 + 动词，单词之间用连字符连接，全部小写，不使用缩写。目录名与 frontmatter 的 `name` 字段保持一致。

| 命名 | 功能 |
|------|------|
| `jiuqing-idea-grill` | 执行前拷问方案 / 信息对齐 |
| `jiuqing-image-generate` | AI 生图 |
| `jiuqing-video-generate` | AI 生视频 |
| `jiuqing-question-deepen` | 追问 / 深度分析 |
| `jiuqing-character-simulate` | 角色模拟 |

## 目录结构

```
skills/
├── core/       # 基础领域 — 通用能力，其他领域可组合调用
├── dev/        # 开发领域 — 需求分析、代码审查、发布检查等
├── content/    # 内容领域 — 文案审核、图片生成、视频生成等
├── scripts/    # 工具脚本（如 sync.sh 多平台软链）
├── AGENTS.md
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

## 使用方式

本仓库是 skill 的**唯一真身**。各 agent 平台扫描自己的扁平 `skills/` 目录，通过软链指回本仓库，从而一处维护、多平台生效。

### 安装到各平台

```bash
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

## License

[MIT](LICENSE)
