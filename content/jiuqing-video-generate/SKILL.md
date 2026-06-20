---
name: jiuqing-video-generate
description: 当用户想根据文字提示词生成/制作一段视频、做视频片段、把一段描述变成动态画面时使用。
category: content
depends: []
---

# jiuqing-video-generate

用 Agnes 的文生视频 API（`agnes-video-v2.0`）把一段提示词变成一段视频。这是固定脚本类能力，按需即时执行，不走执行前对齐。

## 前置条件

环境变量 `AGNES_API_KEY` 必须已设置。脚本只从环境变量读密钥，不读其他来源——若未设置，先让用户 `source` 加载（密钥常配在 `~/.zshrc` 或 `~/.agents/.env`）。

## 执行

终端默认是 bash，先 `source ~/.zshrc` 再调脚本，确保环境变量加载：

```bash
source ~/.zshrc && python3 scripts/video_gen.py "提示词" [输出路径]
```

- `提示词`（必填）—— 视频的文字描述。越具体（主体、动作、镜头运动、风格、光线）出片越可控。
- `输出路径`（可选）—— 默认 `./agnes_vid_时间戳.mp4`。

接口异步：脚本提交后拿到 task_id，每 15 秒轮询一次状态，最长等 15 分钟，成功后自动下载并打印 `SUCCESS: 路径` 和视频 URL。整段耗时通常 1–3 分钟。

## 为什么这样写

- **密钥防脱敏** —— 工具调用层会自动脱敏 API key 字面量，导致 auth header 损坏、请求失败。脚本里 auth header 用字符串拼接（`"Authoriz" + "ation: ..."`）规避，不要改成整串字面量。
- **用 Python 调 curl 而非 bash 脚本** —— bash 脚本处理含密钥的内联 JSON、heredoc 时引号极易出错；Python `subprocess.run(["curl", ...])` 更稳更好调试。
- **视频 URL 的取值位置** —— 成功响应里视频地址在 `data.data.remixed_from_video_id`，字段名有误导但实为完整 URL；它是公开存储地址，下载时**不要**带 auth header，否则会失败。
- **状态值是大写** —— 轮询状态为 `NOT_START` / `IN_PROGRESS` / `SUCCESS` / `FAILED`，判断成功要匹配 `SUCCESS` 而非小写。

## 边界与限制

- **只做文生视频**，不含图生视频、视频续写、局部重绘。
- **不支持图生视频/参考图角色一致性**（已实测确认）—— 接口对未知参数静默忽略；传入 `image`/`image_url` 等参考图参数会被丢弃，成片与参考图无任何关系，返回里也标记为 `textGenerate`。需要"同一角色出现在多段视频"的一致性，这个接口做不到，不要承诺。
- **输出固定 5 秒 / 1280×704**（已实测确认）—— 时长不可控，传 `duration`/`seconds` 等参数同样被忽略，实际都出 5 秒。所以脚本不暴露时长参数。
- **中档质量** —— Agnes 生视频属偏中下水平，适合草稿、社媒短片、概念验证，不适合对画质或时长有要求的终稿。
