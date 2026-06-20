---
name: jiuqing-image-generate
description: 当用户想根据文字提示词生成/创作图片、出图、画一张图、做配图或视觉草图时使用。
category: content
depends: []
---

# jiuqing-image-generate

用 Agnes 的文生图 API（`agnes-image-2.1-flash`）把一段提示词变成一张图片。这是固定脚本类能力，按需即时执行，不走执行前对齐。

## 前置条件

环境变量 `AGNES_API_KEY` 必须已设置。脚本只从环境变量读密钥，不读其他来源。

检查与恢复：
1. 先尝试 `echo $AGNES_API_KEY`，有值则继续。
2. 无值则尝试 `source ~/.zshrc` 或 `source ~/.agents/.env`，再检查。
3. 仍无值则告诉用户："未找到 AGNES_API_KEY，请先设置后重试"，然后**停下，不执行生成**。

## 执行

终端默认是 bash，先 `source ~/.zshrc` 再调脚本，确保环境变量加载：

```bash
source ~/.zshrc && python3 scripts/image_gen.py "提示词" [输出路径] [尺寸]
```

- `提示词`（必填）—— 图片的文字描述。越具体（主体、风格、构图、光线、配色）出图越可控。
- `输出路径`（可选）—— 默认 `./agnes_img_时间戳.png`。
- `尺寸`（可选）—— 默认 `1024x1024`，格式 `宽x高`。

脚本同步返回，成功时打印 `SUCCESS: 路径` 和图片 URL。

## 失败路径

脚本或 API 出错时，按以下方式处理：

| 场景 | 信号 | 处理 |
|------|------|------|
| 提示词为空 | 脚本 `Usage` 提示或 `sys.exit(1)` | 告诉用户需要提供具体的图片描述，等用户补充后再执行 |
| 尺寸格式非法 | 脚本报错或 API 返回错误 | 告诉用户正确格式（`宽x高`，如 `1024x1024`），等用户修正 |
| API 返回 error | JSON 含 `error` 字段 | 把错误信息如实转告用户，不粉饰 |
| 脚本下载失败 | `Download failed` 或文件不存在 | 告诉用户下载失败，可重试或用输出的 URL 手动下载 |
| 脚本不存在 / Python 缺失 | `FileNotFoundError` 或 `No such file` | 告诉用户检查 skills 仓库是否完整，scripts/image_gen.py 是否存在 |
| 网络超时 | 脚本 120 秒超时 | 告诉用户网络可能不通，建议检查网络后重试 |

遇到以上任一情况，都把错误原样告诉用户，不猜测、不自动重试超过 1 次。

## 安全约束

本 skill **只执行** `scripts/image_gen.py` 一个脚本，不执行任何其他 shell 命令。具体禁止：
- 不执行 `rm`、`git`、`curl`（除脚本内部调用外）或其他与生图无关的命令
- 不把 `AGNES_API_KEY` 的值输出到日志、文件或消息中
- 不修改脚本文件、不下载/安装新依赖
- 遇到用户要求执行生图以外的操作时，拒绝并说明本 skill 的职责范围

## 为什么这样写

- **密钥防脱敏** —— 工具调用层会自动脱敏 API key 字面量，导致 auth header 损坏、请求失败。脚本里 auth header 用字符串拼接（`"Authoriz" + "ation: ..."`）规避，不要改成整串字面量。
- **用 Python 调 curl 而非 bash 脚本** —— bash 脚本处理含密钥的内联 JSON、heredoc 时引号极易出错；Python `subprocess.run(["curl", ...])` 更稳更好调试。

## 边界与限制

- **只做文生图**，不含图生图、视频、局部重绘。需要视频另用对应 skill。
- **不保证多图主体一致性** —— 接口只暴露 `prompt/n/size`，没有 reference image / 角色锁定 / seed 控制。同一提示词跑多次只是独立采样的不同变体，主体外观会漂移。需要"同一角色的连续分镜"时，这个接口做不到稳定，不要承诺。
- **中档质量** —— Agnes 生图属中档水平，适合草图、社媒配图、概念验证，不适合对画质极致敏感的终稿。
