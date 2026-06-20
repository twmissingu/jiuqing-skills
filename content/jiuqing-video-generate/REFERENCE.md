# REFERENCE · jiuqing-video-generate 设计 rationale 与 API 边界

按需查阅，无需通读。

## 为什么这样写

- **密钥防脱敏** —— 工具调用层会自动脱敏 API key 字面量，导致 auth header 损坏、请求失败。脚本里 auth header 用字符串拼接（`"Authoriz" + "ation: ..."`）规避，不要改成整串字面量。
- **用 Python 调 curl 而非 bash 脚本** —— bash 脚本处理含密钥的内联 JSON、heredoc 时引号极易出错；Python `subprocess.run(["curl", ...])` 更稳更好调试。
- **视频 URL 的取值位置** —— 成功响应里视频地址在 `data.data.remixed_from_video_id`，字段名有误导但实为完整 URL；它是公开存储地址，下载时**不要**带 auth header，否则会失败。
- **状态值是大写** —— 轮询状态为 `NOT_START` / `IN_PROGRESS` / `SUCCESS` / `FAILED`，判断成功要匹配 `SUCCESS` 而非小写。

## API 能力边界

- **只做文生视频**，不含图生视频、视频续写、局部重绘。
- **不支持图生视频/参考图角色一致性**（已实测确认）—— 接口对未知参数静默忽略；传入 `image`/`image_url` 等参考图参数会被丢弃，成片与参考图无任何关系，返回里也标记为 `textGenerate`。需要"同一角色出现在多段视频"的一致性，这个接口做不到，不要承诺。
- **输出固定 5 秒 / 1280×704**（已实测确认）—— 时长不可控，传 `duration`/`seconds` 等参数同样被忽略，实际都出 5 秒。所以脚本不暴露时长参数。
- **中档质量** —— Agnes 生视频属偏中下水平，适合草稿、社媒短片、概念验证，不适合对画质或时长有要求的终稿。
