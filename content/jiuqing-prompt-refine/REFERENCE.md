# REFERENCE · prompt 打磨参考

对齐时拿不准某维度怎么给推荐、或要组织最终 prompt 时查这里。不必通读。

## 图片 prompt 组件清单（含可选词）

按重要度大致从前到后。组织成自然语言时按这个顺序串。

| 维度 | 常用可选词 |
|---|---|
| 主体 | 谁/什么 + 数量、年龄、材质、服饰、状态 |
| 动作/姿态 | 站立、奔跑、回眸、俯身… |
| 环境/场景 | 地点、背景、时间（清晨/黄昏/夜）、天气 |
| 构图/取景 | wide shot / close-up / portrait / overhead；居中、三分法 |
| 相机/镜头 | 35mm、85mm、f/1.8、shallow depth of field、macro |
| 光影 | golden hour、soft diffused light、rim light、neon、backlit、chiaroscuro、studio softbox |
| 色彩 | teal-and-orange、pastel、monochrome、warm/cool tones |
| 风格/媒介 | photo、oil painting、3D render、anime、watercolor、in the style of [流派] |
| 氛围 | serene、ominous、whimsical、cinematic |
| 比例 | 1:1、16:9、9:16、4:3 |
| 文字 | 要在画面里渲染的文字用双引号包住 |

## 视频 prompt 组件清单（在图片基础上加时间维度）

| 维度 | 常用可选词 |
|---|---|
| 景别/镜头类型 | establishing/wide、medium、close-up、extreme close-up、over-the-shoulder |
| 相机角度 | eye level、high angle、low angle、worm's-eye、top-down |
| 运镜 | dolly in/out、push-in、pull-out、pan、tilt、tracking shot、zoom、crane、orbit、whip pan、locked/static |
| 镜头/焦点 | shallow/deep focus、soft focus、macro lens、wide-angle、dolly zoom |
| 运动 | 谁在动、怎么动 + 强度词（slowly→faster、crashing with force） |
| 时序/节奏 | 多段落用时间码标注；推进顺序常用 wide→medium→close-up |
| 音频（支持原生音频的模型） | dialogue、ambient sound、sound effects、music，分层描述 |
| 时长/技术 | 时长、分辨率、宽高比 |

### 时间码写法（多段落视频）

```
[0-4s]: wide establishing shot, static camera, misty bamboo forest at dawn
[4-9s]: medium shot, slow push-in, the fighter steps forward
[9-15s]: close-up, orbit shot, the fighter strikes, slow motion
```

镜头切换用明确措辞：hard cut to、seamless morph into。

## 通用最佳实践

- **具体胜过含糊，但别过载** —— prompt 越长越复杂，模型越容易丢掉部分元素。每个维度给到位即停，聚焦核心。
- **质量词增益弱** —— "8k / masterpiece / highly detailed" 对现代模型几乎不起作用，别靠它们凑数；把 token 花在具体的光影、构图、风格上。
- **正向描述优于否定** —— 多数自然语言型模型对"不要/没有"理解不稳，描述你**想要**的，而非排除你不要的。
- **属性别串味** —— 多个对象时把各自属性说清楚，避免颜色/材质在对象间错配。
- **视频默认静止** —— 不写运镜很多模型就是固定机位；要动就明确写出运镜。
- **图生视频只写"变化"** —— 若从一张静图生成视频，保留原构图，只描述什么在动。
- **英文优先** —— 多数主流模型对英文遵从度更高；中文模型在文字渲染上对中日韩支持更好。

## 正反例

**反例（关键词堆叠 + 空泛质量词）：**
```
girl, dress, park, beautiful, highly detailed, 8k, masterpiece, best quality
```

**正例（结构化自然语言，维度补齐）：**
```
A young woman in a flowing lavender dress walking through a sunlit park in early
autumn, soft golden-hour backlight filtering through the trees, shallow depth of
field with a warm bokeh background, shot on 85mm, gentle and serene mood,
impressionist painting style, 3:2.
```
中文说明示例：补全了光影（黄金时刻逆光）、构图（85mm 浅景深）、风格（印象派）与比例，去掉了无效质量词。
