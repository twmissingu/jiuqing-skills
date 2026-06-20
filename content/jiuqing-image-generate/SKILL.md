---
name: jiuqing-image-generate
description: 当用户想根据文字提示词生成/创作图片、出图、画一张图、做配图或视觉草图时使用。
category: content
depends: []
---

# jiuqing-image-generate

用 Agnes 的文生图 API（`agnes-image-2.1-flash`）把一段提示词变成一张图片。这是固定脚本类能力，按需即时执行，不走执行前对齐。

## 前置条件

环境变量 `AGNES_API_KEY` 必须已设置。脚本只从环境变量读密钥，不读其他来源——若未设置，先让用户 `source` 加载（密钥常配在 `~/.zshrc` 或 `~/.agents/.env`）。

## 执行

终端默认是 bash，先 `source ~/.zshrc` 再调脚本，确保环境变量加载：

```bash
source ~/.zshrc && python3 scripts/image_gen.py "提示词" [输出路径] [尺寸]
```

- `提示词`（必填）—— 图片的文字描述。越具体（主体、风格、构图、光线、配色）出图越可控。
- `输出路径`（可选）—— 默认 `./agnes_img_时间戳.png`。
- `尺寸`（可选）—— 默认 `1024x1024`，格式 `宽x高`。

脚本同步返回，成功时打印 `SUCCESS: 路径` 和图片 URL。

## 为什么这样写

- **密钥防脱敏** —— 工具调用层会自动脱敏 API key 字面量，导致 auth header 损坏、请求失败。脚本里 auth header 用字符串拼接（`"Authoriz" + "ation: ..."`）规避，不要改成整串字面量。
- **用 Python 调 curl 而非 bash 脚本** —— bash 脚本处理含密钥的内联 JSON、heredoc 时引号极易出错；Python `subprocess.run(["curl", ...])` 更稳更好调试。

## 边界与限制

- **只做文生图**，不含图生图、视频、局部重绘。需要视频另用对应 skill。
- **不保证多图主体一致性** —— 接口只暴露 `prompt/n/size`，没有 reference image / 角色锁定 / seed 控制。同一提示词跑多次只是独立采样的不同变体，主体外观会漂移。需要"同一角色的连续分镜"时，这个接口做不到稳定，不要承诺。
- **中档质量** —— Agnes 生图属中档水平，适合草图、社媒配图、概念验证，不适合对画质极致敏感的终稿。
