---
name: jiuqing-project-ship
description: 当用户说"准备发版""发布前检查""项目要上线/开源到 GitHub""出个 release""帮我做发版前的最后检查""更新版本号和 CHANGELOG 准备发布"时使用，对项目做发版前的全流程把关与准备。
category: dev
depends: [jiuqing-idea-grill]
---

# jiuqing-project-ship

把项目带到"可以安全、专业地发版"的状态。发版是不可逆、对外的动作——一旦推上去，泄露的 secret 会被缓存索引、错误的版本号会误导依赖方。所以本 skill 的价值是**在按下发布键之前，按固定顺序逐项把关**，把高风险项挡在前面，再做面向人和 agent 的文档打磨。

本 skill 只做**检查**和**生成命令/草稿**：所有 `git commit`、`git tag`、`git push`、创建 GitHub Release 等动作都交给用户执行，遵循仓库"提交推送前先经用户同意"的规范。把要执行的命令清楚列给用户，由他确认后自己跑。

## 执行前对齐

本 skill 在 `depends` 中声明 `jiuqing-idea-grill`。进入流程前先走一遍对齐，用下面的**对齐要点**逐条问清楚，一次只问一个、带推荐答案、能查项目就别问。对齐后复述共识再开始。

对齐要点：

- **发版形态** —— 开源到 GitHub？内部发版？仅打 tag？这决定文档打磨与 Release 步骤是否需要。
- **版本与语言栈** —— 当前版本号、本次是 major/minor/patch、项目用什么语言（决定测试/构建命令）。从 `package.json`/`pyproject.toml`/`Cargo.toml` 等先自查，查不到再问。
- **范围裁剪** —— 是否需要中英文 README、AGENTS.md、CHANGELOG。已有的就更新，没有且用户需要才新建。

## 执行流程

按顺序执行，每一阶段以可检验的结论收尾再进入下一阶段。高风险项（安全、法律）在前，文档打磨在后。

### 1. 安全审查（最高优先级，不通过就停）

防止 secret/key/token 泄露到远端。读 `security-checks.md`，按其中的命令逐项扫描。**发现敏感数据立即停止流程**，先和用户处理（替换 placeholder、清历史、补 `.gitignore`），确认干净再继续。

### 2. 法律与许可证

确认 `LICENSE` 存在且与依赖兼容，非代码资源有分发权限。具体兼容性表见 `release-checklist.md`。

### 3. 代码质量

跑测试与构建、查残留调试代码、确认代码风格统一。命令模板见 `release-checklist.md`。测试或构建失败要如实报告失败点，不粉饰、不跳过。

### 4. 版本与 CHANGELOG

按 semver 确认版本号（major=不兼容变更 / minor=向后兼容新功能 / patch=向后兼容修复），更新各语言的版本文件与 `CHANGELOG.md`。版本规则与 CHANGELOG 写法见 `release-checklist.md`。生成（而非执行）打 tag、提交、推送的命令清单交给用户。

### 5. 文档打磨

让项目对人类和 AI agent 都友好。读 `readme-templates.md` 获取中英文 README 模板与写作指南：英文版 `README.md` 为事实标准优先完成，`README_zh.md` 结构与之完全一致。AGENTS.md 的注入不在本 skill 重复实现——若需要写入 agent 行为规范，提示用户用 `jiuqing-agents-inject`。

### 6. 最终核对与总结

对照 `release-checklist.md` 的总核对表逐项确认，输出一份发版准备总结：已完成项、待用户执行的命令（tag/commit/push/创建 Release）、项目核心亮点。让用户能据此一键完成发布。

## 边界

- 不替用户执行任何 git 写操作或对外发布动作，只生成命令与草稿。
- 不顺手改与发版无关的源码或配置。
- 安全审查发现风险时不"先发了再说"，必须先停下处理。
