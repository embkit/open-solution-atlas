# 03 · Glossary

Use these exact terms in every chapter; synonyms are listed only to help
translation, never to introduce a second term.

| Term (en) | 中文 | Definition |
|---|---|---|
| Post | 文章 | The core publishable unit; has one canonical URL and a lifecycle (SM-01) |
| Draft | 草稿 | A Post not yet PUBLISHED; never appears in any public artifact (BR-14) |
| Revision | 修订版本 | Append-only immutable snapshot of a Post's Markdown + metadata |
| Slug | 短标识 | URL path component of a Post; kebab-case, unique, immutable post-publish |
| MediaAsset | 媒体资产 | An uploaded binary (image) with alt text or decorative flag |
| Tag / Category / Series | 标签/分类/系列 | Taxonomy: many-to-many tags; optional single category; ordered series |
| Release | 发布版本 | Atomic build+deploy unit; readers see exactly one Release at a time |
| Redirect | 重定向规则 | 301 (moved/merged) or 410 (gone) record guarding an old post URL |
| Mention | 提及 | A verified Webmention pointing at a Post; moderated before display |
| Webmention | — | W3C protocol: a site notifies another that it linked to it |
| POSSE | 自有先行再分发 | Publish (on) Own Site, Syndicate Elsewhere |
| Canonical URL | 规范链接 | The single authoritative URL of a Post |
| Feed | 订阅源 | RSS 2.0 / Atom 1.0 XML listing of latest posts |
| SearchIndex | 搜索索引 | Client-side static index over published Posts only |
| Release atomicity | 发布原子性 | Readers see previous complete site or new complete site, never a mix |
| Scheduling tolerance | 定时容差 | Allowed delay between `publishedAt` and actual publication (≤ 60 s) |
| ExportBundle | 导出包 | Single open-format archive of all owned content (FR-017) |
| Audit log | 审计日志 | Append-only record of author/moderation actions (CTL-010) |

## Conventions

- Status names use UPPERCASE enum tokens exactly as in state machines.
- "delete" in the UI copy means the lifecycle action UNPUBLISH for published
  posts; hard removal exists only for DRAFTs.
- "reader" always means an unauthenticated public visitor; there is no reader
  account concept.
