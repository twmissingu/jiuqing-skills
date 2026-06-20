# 中英文 README 模板与写作指南

供 SKILL.md 第 5 阶段查阅。英文版 `README.md` 是事实标准，优先完成；`README_zh.md` 与之结构、顺序完全一致，仅语言不同。

## README.md（英文，主版本）

文件开头加中英文互链 badge：

```markdown
[![English](https://img.shields.io/badge/English-blue.svg)](README.md)
[![中文](https://img.shields.io/badge/中文-red.svg)](README_zh.md)

---

# Project Name

[One-line tagline] — 让读者 5 秒内明白为什么值得关注。

## Why This Project?

[2-3 段：解决什么问题，为什么比现有方案好]

## Features

- ✨ Feature 1
- 🚀 Feature 2
- 🔒 Feature 3

## Quick Start

### Prerequisites
[前置条件与最低版本]

### Installation
[安装命令]

### Usage
[基本使用示例，给能跑的真实代码]

## For AI Agents

This project is designed for seamless AI agent interaction:

1. **Clone and install**
   ```bash
   git clone <repo-url>
   cd <project-name>
   # npm install / pip install / cargo build
   ```
2. **Configure**
   ```bash
   # copy .env.example, set keys
   ```
3. **Run**
   ```bash
   # start command
   ```

## Contributing
[简短贡献指南]

## License
[Your License]
```

## README_zh.md（中文版）

内容与英文版完全一致，结构、顺序相同，仅语言不同。同样在开头加互链 badge。

## 写作指南

**吸引人类**：

- 第一行 tagline 在 5 秒内传达价值
- 用结果说话，别罗列"我们用了什么技术"
- 给能跑的真实代码，不留 placeholder
- 适度 emoji（5-8 个）

**AI Agent 指南**：

- 零猜测——agent 能完整执行每一步
- 完整链路：克隆 → 安装 → 配置 → 运行
- 用具体命令替代描述性文字
- 版本明确：最低 Node/Python/Rust/Go 版本
- 展示 `.env.example` 或 `config.example`

## tagline 示例

| 项目类型 | 示例 |
|---------|------|
| CLI 工具 | "Ship production-grade CLI tools in hours, not days" |
| Web 框架 | "The framework that gets out of your way" |
| AI 库 | "LLM-powered [X] without the boilerplate" |
| 开发者工具 | "Write less boilerplate. Ship more features." |
