---
name: jiuqing-diagram-draw
description: "当用户输入文字描述或文章段落，要求生成技术图解（流程图、时序图、架构图、对比图、循环图）时触发"
category: content
depends: []
---

## 何时触发

用户消息含"画图""图解""架构图""流程图""时序图""对比图""循环图""可视化"等意图词，或直接粘贴技术文档要求输出 SVG。

## 执行流程

1. **分析内容**：提取实体（组件、服务、步骤）、关系（流向、依赖、时序、对比维度）。完成标志：输出实体列表+关系列表，实体数 ≤15 可直接画图，>15 则先聚合次要实体。
2. **选择图类型**：在下表"触发特征"列逐一匹配，命中即选定；多命中时选覆盖关系最多的类型。
3. **确定风格**：检查项目已有 SVG 中 `:root` 变量定义，有则沿用其色板和线宽；无则用下方默认规范。用户指定"暗色/dark"则切换暗色变量。
4. **生成 SVG**：手写内联 `<svg>` 代码，所有颜色用 CSS 变量，`<style>` 置于 SVG 内部。
5. **嵌入输出**：用 ````svg` 代码块返回，附一行说明（图类型 + 节点数）。

## 图类型选择标准

| 类型 | 触发特征 | SVG 结构 |
|------|----------|----------|
| 流程图 | 步骤、顺序、分支、决策 | 矩形节点+有向箭头，纵向/横向排列 |
| 时序图 | 消息交互、API 调用、时序 | 竖向生命线+水平消息箭头+序号 |
| 架构图 | 组件、分层、服务拓扑 | 嵌套容器+连接线，按层/域分组 |
| 对比图 | 方案 A/B、优缺点、维度对比 | 对称双列/多列卡片逐行对齐 |
| 循环图 | 迭代、PDCA、反馈回路 | 环形节点+循环箭头 |

## SVG 风格规范

```css
:root {
  --bg: #ffffff; --node-bg: #f0f4f8; --text: #1e293b;
  --border: #cbd5e1; --primary: #2563eb; --accent: #f59e0b;
  --success: #10b981; --danger: #ef4444; --edge: #94a3b8;
}
```

- **字体**：`font-family: system-ui, -apple-system, sans-serif`；标题 16px 加粗，正文 13-14px。
- **间距**：节点内边距 12px，节点间距 ≥40px，边距 ≥20px。
- **圆角**：矩形 `rx="8" ry="8"`。
- **线宽**：连接线 2px，箭头用 `<marker>` 定义标准三角形（10×10）。
- **画布**：宽度 800，高度自适应内容。
- **同一项目**：首张图确定配色后，后续图解沿用相同色板和线宽。

## 暗色模式适配

在 SVG `<style>` 内用 `@media (prefers-color-scheme: dark)` 覆盖变量：

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f172a; --node-bg: #1e293b; --text: #e2e8f0;
    --border: #334155; --primary: #3b82f6; --edge: #64748b;
  }
}
```

所有 `fill`、`stroke`、`color` 必须引用变量，禁止硬编码颜色值。

## 边界

- **禁止**调用外部出图 API（QuickChart、Mermaid 在线服务、GraphViz Online 等）。
- **禁止**生成数据可视化图表（柱状图、折线图、饼图、散点图）→ 引导用户使用 matplotlib。
- 节点超过 **15 个** → 建议用户拆分为多个子图或聚合为容器节点。
- 仅输出纯 SVG 代码，不输出 PNG/JPEG。

## 失败路径

| 情况 | 处理 |
|------|------|
| 描述模糊，提取不到实体关系 | 追问："请补充关键组件和它们之间的关系，例如'前端→网关→服务→数据库'" |
| 无法匹配任何图类型 | 列出可选类型，请用户明确 |
| 节点 >15 个 | 建议拆分："节点较多，建议按模块分组画多个子图" |
| SVG 过长（>2000 字符） | 分段输出，先给核心部分，再补细节 |

## 示例

**输入**："画微服务架构图，包含 API 网关、用户服务、订单服务、库存服务，网关转发请求到各服务。"

**输出片段**：

```svg
<svg viewBox="0 0 800 420" xmlns="http://www.w3.org/2000/svg">
  <style>
    :root{--bg:#fff;--node-bg:#f0f4f8;--text:#1e293b;--border:#cbd5e1;--primary:#2563eb;--edge:#94a3b8}
    @media(prefers-color-scheme:dark){:root{--bg:#0f172a;--node-bg:#1e293b;--text:#e2e8f0;--border:#334155;--edge:#64748b}}
    text{font-family:system-ui,sans-serif;fill:var(--text)}
    .node{fill:var(--node-bg);stroke:var(--border);stroke-width:2;rx:8;ry:8}
    .primary{fill:var(--primary);stroke:var(--primary)}
    .primary text{fill:#fff}
    .edge{fill:none;stroke:var(--edge);stroke-width:2;marker-end:url(#arr)}
  </style>
  <defs><marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3Z" fill="var(--edge)"/></marker></defs>
  <rect width="800" height="420" fill="var(--bg)"/>
  <!-- API 网关 -->
  <rect class="node primary" x="300" y="30" width="200" height="50"/>
  <text x="400" y="60" text-anchor="middle" font-size="15" font-weight="600">API 网关</text>
  <!-- 三个服务 -->
  <rect class="node" x="60" y="180" width="160" height="50"/>
  <text x="140" y="210" text-anchor="middle" font-size="14">用户服务</text>
  <rect class="node" x="320" y="180" width="160" height="50"/>
  <text x="400" y="210" text-anchor="middle" font-size="14">订单服务</text>
  <rect class="node" x="580" y="180" width="160" height="50"/>
  <text x="660" y="210" text-anchor="middle" font-size="14">库存服务</text>
  <!-- 连线 -->
  <path class="edge" d="M350,80 L140,180"/>
  <path class="edge" d="M400,80 L400,180"/>
  <path class="edge" d="M450,80 L660,180"/>
</svg>
```
