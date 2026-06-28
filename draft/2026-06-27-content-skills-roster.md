# content/ 技能清单扩充

> 调研基础：三参考仓库
> - [huashu-skills](https://github.com/alchaincyf/huashu-skills) — 花叔，21 个 skill，写作/选题/视频/配图全覆盖
> - [baoyu-skills](https://github.com/JimLiu/baoyu-skills) — 宝玉，配图/发布/抓取最强，20+ skill
> - [kangarooking-skills](https://github.com/kangarooking/kangarooking-skills) — 袋鼠，选题/标题/多平台
>
> 创建日期：2026-06-27
> 状态：草案

## 仓库已有 content/（3 个，不动）

| Skill | 类型 |
|-------|------|
| jiuqing-image-generate | 文生图（Agnes API，固定脚本） |
| jiuqing-video-generate | 文生视频（Agnes API，固定脚本） |
| jiuqing-prompt-refine | 提示词打磨（depends: jiuqing-idea-grill） |

## 设计决策

| 设计点 | 决策 |
|--------|------|
| text-humanize 引用 humanizer-zh | "AI 痕迹扫描"遍加载 humanizer-zh 作为检查清单，不复刻规则（单一信息源） |
| title-craft 自进化标题库 | 暂不内置，退化为纯生成；进化留给 skill-evolve 迭代 |
| research-structured 存档落点 | 项目工作目录下 `research-notes/`，skill 不存储状态 |

## 最终纳入清单（14 个）

### 第一梯队：写作核心组（4 个）

| # | 拟命名 | 解决的痛点 | 参考对标 | depends |
|---|--------|-----------|---------|---------|
| 1 | jiuqing-article-edit | 编辑截断丢进度、版本混乱 | huashu-article-edit | jiuqing-idea-grill |
| 2 | jiuqing-text-humanize | AI 味重没人味 | huashu-proofreading + humanizer-zh | jiuqing-idea-grill |
| 3 | jiuqing-article-rewrite | 长文→短平台转换低效 | huashu-article-to-x | jiuqing-idea-grill |
| 4 | jiuqing-title-craft | 标题平庸 CTR 低 | kangaroo-viral-title | jiuqing-idea-grill |

### 第一梯队：选题调研组（2 个）

| # | 拟命名 | 解决的痛点 | 参考对标 | depends |
|---|--------|-----------|---------|---------|
| 5 | jiuqing-topic-generate | "今天写什么"选题焦虑 | huashu-topic-gen + kangaroo-viral-topic | jiuqing-idea-grill |
| 6 | jiuqing-research-structured | 调研散乱无法复用 | huashu-info-search | jiuqing-idea-grill |

### 第一梯队：配图组（3 个）

| # | 拟命名 | 解决的痛点 | 参考对标 | depends |
|---|--------|-----------|---------|---------|
| 7 | jiuqing-infographic-make | 文字转信息图无框架 | baoyu-infographic | jiuqing-prompt-refine |
| 8 | jiuqing-cover-design | 封面缺乏系统控制 | baoyu-cover-image | jiuqing-prompt-refine |
| 9 | jiuqing-diagram-draw | 技术图解手动画慢 | baoyu-diagram | 无 |

### 第二梯队：发布前门户（P0 新增，2 个）

| # | 拟命名 | 解决的痛点 | 参考对标 | depends |
|---|--------|-----------|---------|---------|
| 10 | jiuqing-hook-craft | 开头 3 秒留不住人 | baoyu-hook-generator + kangaroo-viral-title hook 策略 | jiuqing-idea-grill |
| 11 | jiuqing-content-audit | 发布后才发现问题 | baoyu-content-qa + huashu-proofreading 第三遍 | 无 |

### 第三梯队：效率提升（P1/P2 新增，3 个）

| # | 拟命名 | 解决的痛点 | 参考对标 | depends |
|---|--------|-----------|---------|---------|
| 12 | jiuqing-crossplatform-convert | 一稿多发手动逐改 | baoyu 多平台能力 + kangaroo 路由模式 | jiuqing-idea-grill |
| 13 | jiuqing-content-summarize | 长文/报告消化慢 | baoyu-xhs-images 隐含拆解能力 | 无 |
| 14 | jiuqing-newsletter-curate | 资讯策展无标准化 | kangaroo-viral-topic 路由设计 | jiuqing-idea-grill |

## 明确不纳入及理由

| 能力域 | 理由 |
|--------|------|
| 视频脚本组（outline/script-spoken/hook-check） | 用户选不纳入 |
| PPT/PDF（slides/md-to-pdf） | 本地已有 pptx-generator、minimax-pdf |
| 抓取转换（url-to-markdown/video-transcript） | 本地已有 firecrawl/defuddle/kimi-webbridge |
| 发布上传（post-wechat/image-upload） | 违反"不硬编码平台工具"约束 |
| 素材/元能力（material-search/prompt-save） | 偏个人知识管理 |

## 执行顺序

```
优先级
│
├─ 🔴 第一梯队：写作核心组
│   ├─ 1. jiuqing-article-edit
│   ├─ 2. jiuqing-text-humanize
│   ├─ 3. jiuqing-article-rewrite
│   └─ 4. jiuqing-title-craft
│
├─ 🔴 选题调研组
│   ├─ 5. jiuqing-topic-generate
│   └─ 6. jiuqing-research-structured
│
├─ 🔴 配图组
│   ├─ 7. jiuqing-infographic-make
│   ├─ 8. jiuqing-cover-design
│   └─ 9. jiuqing-diagram-draw
│
├─ 🔴 P0 新增
│   ├─ 10. jiuqing-hook-craft
│   └─ 11. jiuqing-content-audit
│
└─ 🟡 P1/P2 新增
    ├─ 12. jiuqing-crossplatform-convert
    ├─ 13. jiuqing-content-summarize
    └─ 14. jiuqing-newsletter-curate
```

最独立可先做：`jiuqing-diagram-draw`（无依赖、纯 SVG）和 `jiuqing-content-audit`（独立检查点）。
