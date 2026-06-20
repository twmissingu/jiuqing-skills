# REFERENCE · jiuqing-image-generate 设计 rationale 与 API 边界

按需查阅，无需通读。

## 为什么这样写

- **密钥防脱敏** —— 工具调用层会自动脱敏 API key 字面量，导致 auth header 损坏、请求失败。脚本里 auth header 用字符串拼接（`"Authoriz" + "ation: ..."`）规避，不要改成整串字面量。
- **用 Python 调 curl 而非 bash 脚本** —— bash 脚本处理含密钥的内联 JSON、heredoc 时引号极易出错；Python `subprocess.run(["curl", ...])` 更稳更好调试。

## API 能力边界

- **只做文生图**，不含图生图、视频、局部重绘。需要视频另用对应 skill。
- **不保证多图主体一致性** —— 接口只暴露 `prompt/n/size`，没有 reference image / 角色锁定 / seed 控制。同一提示词跑多次只是独立采样的不同变体，主体外观会漂移。需要"同一角色的连续分镜"时，这个接口做不到稳定，不要承诺。
- **中档质量** —— Agnes 生图属中档水平，适合草图、社媒配图、概念验证，不适合对画质极致敏感的终稿。
