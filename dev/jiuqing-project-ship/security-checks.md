# 安全审查（发版前最高优先级）

发版是不可逆的对外动作，secret 一旦推上去会被缓存、被索引，即使后删也可能已被抓取。所以这一关不通过就停下，先和用户处理干净再继续。

## 必须排查的敏感文件类型

- `.env`、`.env.local`、`.env.production`、`.env.*.local`
- `secrets.json`、`credentials.json`、`keys.json`
- `*.pem`、`*.key`、`*.p12`、`*.pfx`
- `config.local.*`、`settings.local.*`
- `openapi.json`（可能内嵌 API key）
- 任何含 `api_key` / `apikey` / `api-key` / `token` / `secret` / `password` / `private_key` 的文件

## 扫描命令（在项目根目录执行）

```bash
# 1. 查看 .gitignore 是否覆盖敏感文件
cat .gitignore

# 2. 检查是否有 .env 类文件被 git 追踪
git ls-files | grep -E '\.env'

# 3. 搜索常见 secret 模式
grep -rE '(api[_-]?key|apikey|api-key|token|secret|password|private[_-]?key)' \
  --include='*.json' --include='*.yaml' --include='*.yml' --include='*.toml' \
  --include='*.env*' --include='*.config*' --include='*.ini' \
  --exclude-dir=node_modules --exclude-dir=.git .

# 4. 可选：深度扫描（如已安装）
gitleaks detect --source . 2>/dev/null || echo "gitleaks 未安装，跳过深度扫描"
```

## 常见风险与处理

| 场景 | 风险 | 处理方式 |
|------|------|----------|
| `.env` 已被提交 | API key 暴露 | 用 `git filter-repo` 或 BFG 清历史 |
| 示例文件含真实 key | 误导/泄露 | 替换为 `YOUR_API_KEY_HERE` |
| 源码硬编码 secret | 永久泄露 | 迁移到环境变量 |
| `.gitignore` 不全 | 后续误提交 | 补全规则后再发版 |

## 发现敏感数据时的处置

1. **立即停止发版流程**，先和用户对齐。
2. 把明文 secret 替换为 placeholder。
3. 已进入 git 历史的，用 `git filter-repo` 或 BFG Repo-Cleaner 清除（并提醒用户轮换已泄露的凭证）。
4. 补全/收紧 `.gitignore`。
5. 重新跑一遍扫描命令，确认干净再继续后续阶段。
