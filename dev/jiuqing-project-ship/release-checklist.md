# 发版核对清单（法律 / 代码质量 / 版本 / 总核对）

供 SKILL.md 第 2、3、4、6 阶段查阅。

## 法律与许可证（阶段 2）

- [ ] `LICENSE` 文件存在（MIT / Apache 2.0 / GPL / BSD 等 OSI 认证许可证）
- [ ] 许可证与项目依赖兼容
- [ ] 非代码资源（图片、字体等）有分发权限

许可证兼容性速查：

| 项目许可证 | 可用依赖 | 注意 |
|-----------|---------|------|
| MIT | 几乎所有 | 无 |
| Apache 2.0 | 几乎所有 | 注意专利条款 |
| GPL | GPL / AGPL / LGPL | 不能引入仅 MIT 的不兼容场景需逐案判断 |
| BSD | 几乎所有 | 无 |

```bash
ls -la LICENSE* LICENCE* 2>/dev/null
```

## 代码质量（阶段 3）

- [ ] 测试全部通过
- [ ] 编译/构建无错误
- [ ] 无残留调试代码（console.log / print / debugger 等）
- [ ] 代码风格统一（lint/format 通过）

命令按语言栈选用，失败要如实报告：

```bash
# 测试
npm test 2>/dev/null || pytest 2>/dev/null || cargo test 2>/dev/null || go test ./... 2>/dev/null

# 构建
npm run build 2>/dev/null || cargo build --release 2>/dev/null || go build ./... 2>/dev/null

# 查残留调试代码
grep -rn 'console\.\|debugger' --include='*.js' --include='*.ts' --exclude-dir=node_modules --exclude-dir=dist . 2>/dev/null
```

## 版本与 CHANGELOG（阶段 4）

**Semantic Versioning（MAJOR.MINOR.PATCH）**：

- **MAJOR** —— 不兼容的 API 变更（递增时 MINOR、PATCH 归零）
- **MINOR** —— 向后兼容的新功能（递增时 PATCH 归零；公共 API 标记弃用时也要升 MINOR）
- **PATCH** —— 向后兼容的 bug 修复
- `0.y.z` 为初期开发，API 不视为稳定；`1.0.0` 起定义稳定公共 API
- 预发布：`1.0.0-alpha.1`（precedence 低于正式版）；构建元数据：`1.0.0+build.5`（不参与 precedence）

待更新的版本文件（按语言栈）：`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` 等。

**CHANGELOG.md 写法**（[keepachangelog](https://keepachangelog.com/)）：日志是给人看的、每个版本一条、最新在最上、日期用 `YYYY-MM-DD`、同类变更归组。

变更分类：Added（新功能）/ Changed（已有功能变化）/ Deprecated（即将移除）/ Removed（已移除）/ Fixed（修复）/ Security（安全）。

```markdown
## [1.0.0] - YYYY-MM-DD

### Added
- 新功能

### Fixed
- 修复的 bug
```

**生成给用户执行的命令**（本 skill 不自动执行）：

```bash
# 由用户确认后自行执行
git add -A
git commit -m "Release v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0
```

## 总核对表（阶段 6）

| 类别 | 检查项 | 状态 |
|------|--------|------|
| 安全 | `.gitignore` 完整 | ☐ |
| 安全 | 无 secret 泄露 | ☐ |
| 法律 | LICENSE 存在且兼容 | ☐ |
| 代码 | 测试通过 | ☐ |
| 代码 | 构建成功 | ☐ |
| 代码 | 无残留调试代码 | ☐ |
| 版本 | 版本号按 semver 更新 | ☐ |
| 版本 | CHANGELOG 更新 | ☐ |
| 文档 | README.md / README_zh.md | ☐ |
| 文档 | AGENTS.md（如需，用 jiuqing-agents-inject） | ☐ |
| 发布 | tag/commit/push 命令已生成待用户执行 | ☐ |
