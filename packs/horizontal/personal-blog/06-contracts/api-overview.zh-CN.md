# 06 · API 概览

两个界面：

1. **管理 API**（`/api/v1`，已认证，仅作者）——内容、媒体、定时、审核、
   重定向、导出。
2. **公开接入端点**（未认证、不可信、已加固）——Webmention、可选评论。

公众消费的其他一切都是**静态制品**，不是 API：
`/index.html`、`/posts/<slug>/`、`/feed.xml`（RSS 2.0）、`/atom.xml`、
`/sitemap.xml`、`/robots.txt`、`/search-index.json`（懒加载）。

## 清单

| 契约 | 方法/路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-01 | `GET /api/v1/posts` | bearer | 列出文章（含草稿），支持过滤 | FR-001 |
| C-02 | `POST /api/v1/posts` | bearer | 创建草稿 | FR-001 |
| C-03 | `GET/PATCH/DELETE /api/v1/posts/{id}` | bearer | 读取 / 自动保存更新 / 仅删除草稿 | FR-001/002 |
| C-04 | `POST /api/v1/posts/{id}/revisions` | bearer | 快照修订 | FR-002 |
| C-05 | `POST /api/v1/posts/{id}/publish` | bearer | 立即发布（校验闸门） | FR-004/008 |
| C-06 | `POST /api/v1/posts/{id}/schedule` | bearer | 设置/更改定时时间 | FR-009 |
| C-07 | `POST /api/v1/posts/{id}/unpublish` | bearer | 410 状态转换 | FR-010 |
| C-08 | `POST /api/v1/media` | bearer（multipart） | 图片上传，带替代文本要求 | FR-003 |
| C-09 | `GET/PUT /api/v1/tags`、series、categories | bearer | 分类体系管理 | FR-005 |
| C-10 | `CRUD /api/v1/redirects` | bearer | 301/410 治理 | FR-010 |
| C-11 | `GET /api/v1/mentions` | bearer | 审核队列 | FR-014 |
| C-12 | `POST /api/v1/mentions/{id}:approve|:reject|:block` | bearer | 审核动作 | FR-014 |
| C-13 | `POST /api/v1/export` | bearer | 创建 ExportBundle 作业 | FR-017 |
| C-14 | `POST /webmention` | 无，表单编码 | W3C Webmention 接收器 | FR-013 |
| C-15 | `POST /posts/{slug}/comments` | 无，有速率限制 | 可选的原生评论 | FR-015 |
| C-16 | `GET /api/v1/releases`、`/releases/{id}` | bearer | 发布/可观测性 | NFR-013/015 |

约定：bearer 令牌（短期，OIDC 签发）；JSON；ISO-8601 UTC；发布/定时/导出带
幂等键请求头；错误采用 RFC 9457 problem+json；所有变更都追加审计记录。

完整的 OpenAPI 3.1 契约：[`api/openapi.yaml`](./api/openapi.yaml)。
