# LOG · jiuqing-skill-evolve 进化记录

## 2026-06-20 进化了 jiuqing-image-generate
- 结果：keep 2 轮；baseline 69 → R1 92（+23）→ R2 精简正文（预估 93-94）
- 有效的改法：Round 1 补充 failure-path-encoding（失败路径表 +6 分）、high-risk-blacklist（安全约束 +3 分）、failure-coverage（+1 分）效果最显著；Round 2 下沉参考材料到 REFERENCE.md 改善 info-layering
- 踩的坑：judge 输出格式不统一（有的嵌套 dimensions、有的有 extra total 字段），aggregate.py 校验严格会报错；需要在 judge prompt 中明确指定平铺 JSON 格式
- 对本 skill 的改进线索：judge prompt 应加一句"输出平铺 JSON，不要嵌套在 dimensions 或其他 key 下"；或 aggregate.py 增加 format auto-detection
