# 05 · 数据流

## DF-1 创作 → 公开（写入路径）

```
editor autosave (≤1s)
   ├──▶ staging workspace (unsaved buffer, debounce 5s)
   └────commit──▶ content repo (new revision row + sha)
                        │
   publish action ──────┴──▶ release job:
                                  1. 同步仓库到该 commit
                                  2. 校验 frontmatter、链接、a11y、订阅源模式
                                  3. 渲染页面、索引、订阅源、站点地图、检索索引
                                  4. 上传制品到 prefix/<sha>
                                  5. 原子指针晋升 → current=<sha>
                                  6. CDN 刷新（文章、索引、订阅源、站点地图）
                                  7. 标记 release 为 DEPLOYED；否则 FAILED，旧的 current 保持完好
```

## DF-2 读取路径

```
request ─▶ CDN ──命中──▶ 制品（不回源，除边缘聚合外无日志）
              └─未命中─▶ 对象存储（不可变前缀）──▶ 填充缓存
草稿在这条路径上根本不存在（BR-14）：构建器会排除它们。
```

## DF-3 接入路径（提及）

```
endpoint ─▶ 作业队列 ─▶ 出站抓取来源 ─▶ 解析+验证 ─▶ 清洗
   ─▶ 运行库存储（PENDING）──▶ 审核 ─▶ 已通过的行被纳入
目标文章页的下一次 release 重建。
```
提及在**构建期**被渲染成静态 HTML——公开站点依然没有任何运行时数据库依赖。

## DF-4 定时发布

```
cron/函数（1 分钟）──▶ 到期的定时项（run_at ≤ now，文章为 SCHEDULED）
   ─▶ 调用同一条发布流水线 ─▶ attempts++ ─▶ 3 次失败 ⇒ 告警（FR-009）
```

## DF-5 备份与导出

```
content repo ──镜像──▶ 远程 git（持续）
运行库数据库 ──快照──▶ 加密的跨区域桶（每日，30 天留存）
                            └─ 恢复演练每周一次（见 08-quality/failure-and-dr.md）
导出动作 ─▶ 仓库归档 + 提及/评论/重定向/分类体系（JSON/CSV）
                 + manifest.json（格式版本）= ExportBundle（不含 IP/日志 —— BR-13）
```

## 一致性规则

1. 订阅源 GUID ⇒ 正本 URL（永不复用）。
2. 站点地图、检索索引、标签页、文章页都在同一个 Release 中生成——制品之间
   不可能互相矛盾。
3. 重定向表由构建器与边缘配置共同求值；410/301 即使在 CDN 层也存在，因此
   被移除的页面绝不会落到 404（BR-06）。
