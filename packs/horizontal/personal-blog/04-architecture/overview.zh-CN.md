# 04 · 架构概览

## 架构风格

**静态公开 / 薄动态边缘**：公开站点是一组预构建的静态制品，完全由 CDN/对象
存储提供；唯一的服务端运行时是一个极小且隔离的*创作与接入服务*（内容 API +
Webmention 端点 + 定时器），背后由一个即使没有该服务也依然可读的内容仓库
支撑。

这一形态背后的决策记录在：
[ADR-0001](./adr/0001-static-first.md) ·
[ADR-0002](./adr/0002-git-as-source-of-truth.md) ·
[ADR-0003](./adr/0003-webmention.md) ·
[ADR-0004](./adr/0004-client-side-search.md)。

## 组件视图

```mermaid
flowchart TB
    subgraph authoring[创作区 — 已认证]
        E[编辑器 / 管理界面<br/>静态 SPA] -->|HTTPS + OAuth 令牌| CAPI[内容 API<br/>草稿、媒体、定时、审核]
    end

    CAPI --> CR[内容仓库<br/>Git：markdown + frontmatter + 媒体]
    CAPI --> DB[(运行库数据库<br/>修订日志、提及、审计)]
    SCH[定时器 worker] --> CAPI

    CR -->|push/触发| B[构建器<br/>渲染、a11y + 链接检查、订阅源/站点地图/索引]
    B --> REL[Release 存储<br/>不可变制品版本]
    REL -->|原子切换| CDN[CDN / 静态托管]

    subgraph public[公开区 — 无机密、无写入]
        R[读者] --> CDN
        CRAWL[爬虫 / 订阅阅读器] --> CDN
    end

    subgraph edge[接入边缘 — 不可信]
        WM[Webmention 端点] -->|验证、清洗| DB
        COM[评论端点<br/>可选]|-->|速率限制 + 垃圾评分| DB
    end
    EXTSITE[外部站点] --> WM
    R --> WM
```

## 部署视图

```
Region A（此规模下单区域即可）
├── CDN 边缘：当前 Release 的全球缓存（公开页面、订阅源、媒体）
├── 源站：存放 Release 版本的对象存储桶（私有前缀）
│    + current-release 指针；原子晋升 = 指针更新
├── 创作服务：1 个小容器/函数，自动伸缩 0..2
│    + 托管的关系型/KV 存储（提及、会话）
│    + 定时器：每分钟 cron/函数调用
└── 备份：内容仓库远程镜像 + 每日加密数据库快照（跨区域桶）
```

静态失败：创作服务宕机时，公开站点继续原样提供上一个 Release（NFR-004）。作者
也可以直接用 Git 推送内容——仓库始终是一条有效的人工通道。

## 关键流程与组件的对应

| 流程 | 路径 |
|---|---|
| 写作与发布（BP-01） | 编辑器 → 内容 API → 仓库 + 修订记录 → 构建器 → Release → CDN |
| 定时发布（FR-009） | 定时器 → 内容 API 在 T+0/60s 发布；3 次尝试后仍失败则告警 |
| 阅读（BP-04） | 读者 → 仅 CDN 缓存；仅在缓存冷时回源 |
| 回应（BP-02） | 外部站点 → Webmention 端点 → 验证 → 数据库 PENDING → 管理界面审核 → 构建器重建受影响页面 |
| 退出（BP-05） | 内容 API 导出 → 仓库归档 + 提及转储 → ExportBundle |

## 多租户

无。单一作者（可选的第二位可信编辑者是未来的、非 MVP 身份）。这消除了一整
类隔离方面的顾虑，也是一个明确的范围决策（见方案包 README 的不在范围部分）。
