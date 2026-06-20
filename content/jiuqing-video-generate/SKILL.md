---
name: jiuqing-video-generate
description: 当用户想根据文字提示词生成/制作一段视频、做视频片段、把一段描述变成动态画面时使用。
category: content
depends: []
---

# jiuqing-video-generate

用 Agnes 的文生视频 API（`agnes-video-v2.0`）把一段提示词变成一段视频。这是固定脚本类能力，按需即时执行，不走执行前对齐。

## 前置条件

环境变量 `AGNES_API_KEY` 必须已设置。脚本只从环境变量读密钥，不读其他来源。

检查与恢复：
1. 先尝试 `echo $AGNES_API_KEY`，有值则继续。
2. 无值则尝试 `source ~/.zshrc` 或 `source ~/.agents/.env`，再检查。
3. 仍无值则告诉用户："未找到 AGNES_API_KEY，请先设置后重试"，然后**停下，不执行生成**。

## 执行

终端默认是 bash，先 `source ~/.zshrc` 再调脚本，确保环境变量加载：

```bash
source ~/.zshrc && python3 scripts/video_gen.py "提示词" [输出路径]
```

- `提示词`（必填）—— 视频的文字描述。越具体（主体、动作、镜头运动、风格、光线）出片越可控。
- `输出路径`（可选）—— 默认 `./agnes_vid_时间戳.mp4`。

接口异步：脚本提交后拿到 task_id，每 15 秒轮询一次状态，最长等 15 分钟，成功后自动下载并打印 `SUCCESS: 路径` 和视频 URL。整段耗时通常 1–3 分钟。

## 失败路径

| 场景 | 信号 | 处理 |
|------|------|------|
| 提示词为空 | 脚本 `Usage` 提示或 `sys.exit(1)` | 告诉用户需要提供具体的视频描述，等用户补充 |
| API 返回 error | JSON 含 `error` 字段 | 把错误信息如实转告用户 |
| 生成失败 | 状态为 `FAILED`，含 `fail_reason` | 把 fail_reason 告诉用户 |
| 轮询超时 | 60 次轮询后仍无终态 | 告诉用户生成可能仍在进行，可稍后用 task_id 查询 |
| 下载失败 | 文件不存在或 <1KB | 告诉用户下载失败，可用输出的 URL 手动下载 |
| 脚本不存在 / Python 缺失 | `FileNotFoundError` | 告诉用户检查 skills 仓库完整性 |
| 网络超时 | 脚本 120 秒超时 | 告诉用户检查网络后重试 |

遇到以上任一情况，把错误原样告诉用户，不猜测。

## 安全约束

本 skill **只执行** `scripts/video_gen.py` 一个脚本，不执行任何其他 shell 命令。具体禁止：
- 不执行 `rm`、`git`、`curl`（除脚本内部调用外）或其他与生视频无关的命令
- 不把 `AGNES_API_KEY` 的值输出到日志、文件或消息中
- 不修改脚本文件、不下载/安装新依赖
- 遇到用户要求执行生视频以外的操作时，拒绝并说明本 skill 的职责范围

设计 rationale（密钥防脱敏、视频 URL 取值、状态大写）与 API 能力边界见同目录 `REFERENCE.md`，按需查阅。
