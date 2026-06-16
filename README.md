# Skills

基于中国神话体系的 Agent 通用技能库。

## 设计理念

每个 skill 是一个独立的 `SKILL.md` 文件，可跨平台使用（Codex、Claude Code、OpenCode 等）。技能之间通过 `depends` 字段声明依赖关系，组合调用时由 agent 自行加载。

## 命名体系

以山海经和中国神话为灵感，两字命名，有意象，能暗示功能。

| 命名 | 含义 | 功能 |
|------|------|------|
| 烛龙 | 睁眼为昼闭眼为夜，照亮真相 | 追问 / 深度分析 |
| 丹青 | 丹砂与青雘，绘画的代称 | AI 生图 |
| 流光 | 流动的光影 | AI 生视频 |
| 化形 | 万物化形，变化形态 | 角色模拟 |

## 目录结构

```
skills/
├── core/       # 基础领域 — 通用能力，其他领域可组合调用
├── dev/        # 开发领域 — 需求分析、代码审查、发布检查等
├── content/    # 内容领域 — 文案审核、图片生成、视频生成等
├── AGENTS.md
├── LICENSE
└── README.md
```

## SKILL.md 标准

每个 skill 必须遵循以下 frontmatter 格式：

```yaml
---
name: 中文名
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

## 使用方式

将此仓库路径添加到 agent 的 skill 搜索路径中即可。

## License

[MIT](LICENSE)
