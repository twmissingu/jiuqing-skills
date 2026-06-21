# Changelog

本项目所有重要变更都记录在此文件。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-06-21

首个公开版本。一套跨平台（Codex、Claude Code、OpenCode 等）的 agent 通用技能库，按 core / dev / content 三大领域组织，技能间通过 `depends` 字段声明依赖、组合调用。

### Added

- **基础领域（core）**
  - `jiuqing-idea-grill` —— 执行前逐项拷问方案与需求，对齐后再动手；可被其他 skill 通过 `depends` 引用
  - `jiuqing-roles-debate` —— 多角色辩论推演
  - `jiuqing-session-handoff` —— 生成会话交接文档，支持切换模型 / 开新会话接力
  - `jiuqing-skill-create` —— 按标准格式新建 skill
  - `jiuqing-skill-evolve` —— 基于评分反馈迭代进化 skill
- **开发领域（dev）**
  - `jiuqing-agents-inject` —— 向项目注入 AGENTS.md 行为规范
  - `jiuqing-bug-diagnose` —— 系统化定位与诊断 bug
  - `jiuqing-context-sync` —— 同步项目上下文
  - `jiuqing-goal-set` —— 上线导向地设定项目目标
  - `jiuqing-prd-write` —— 撰写 PRD
  - `jiuqing-product-polish` —— 产品打磨与多维度审查
  - `jiuqing-project-ship` —— 发版前全流程把关（安全 / 法律 / 质量 / 版本 / 文档）
- **内容领域（content）**
  - `jiuqing-image-generate` —— AI 生图（密钥仅从环境变量 `AGNES_API_KEY` 读取）
  - `jiuqing-video-generate` —— AI 生视频（密钥仅从环境变量读取）
  - `jiuqing-prompt-refine` —— 打磨图像 / 视频生成提示词
- **基础设施**
  - `scripts/sync.sh` —— 为各 agent 平台目录建立软链，一处维护、多平台生效，幂等且不覆盖既有内容
  - `AGENTS.md` —— 仓库级 skill 写作原则与行为规范
  - MIT License

[0.1.0]: https://github.com/twmissingu/jiuqing-skills/releases/tag/v0.1.0
