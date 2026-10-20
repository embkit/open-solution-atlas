# 03 · 领域模型

## 限界上下文

| 上下文 | 职责 | 拥有的类型 |
|---|---|---|
| **创作** | 草稿、修订、媒体、元数据编辑 | Post（草稿）、Revision、MediaAsset |
| **发布** | 构建、发布版本、URL 治理、定时 | Release、Redirect、Post（已发布投影） |
| **目录** | 分类体系、索引、检索索引 | Tag、Series、SearchIndex |
| **联合发布** | 订阅源、站点地图、SEO 制品 | FeedItem（投影）、SitemapEntry |
| **互动** | Webmention、评论、审核、垃圾内容 | Mention、Comment、ModerationAction |
| **洞察** | 聚合的匿名分析 | PageViewEvent → 仅聚合统计 |
| **主权保障** | 上述一切的导出/恢复 | ExportBundle |

互动与洞察绝不回流到创作内容中；它们是纯下游上下文（防止读者数据超出已通过
的提及而泄漏进内容导出，BR-13）。

## 核心聚合

### Post（聚合根）

```
Post
├── identity: id (uuid), slug (unique, immutable post-publish)
├── content: title, summary, bodyMarkdown, bodyHtml (rendered projection)
├── classification: Tag[*], Category?, Series? (+ position)
├── media: MediaAsset[*] (ordered embeds, each alt-text or decorative flag)
├── licensing: licenseId
├── lifecycle: status, createdAt, publishedAt?, updatedAt, revisedAt
├── seo: canonicalUrl, ogImage?, metaDescription?
└── invariants (enforced by aggregate, not by UI)
    • DRAFT 可被删除；PUBLISHED 只能被取消发布（410），绝不被静默硬删除
    • PUBLISHED 状态下更改 slug，仅在与一个 Redirect（301）同时发生时才合法
    • 发布要求元数据完整（FR-004）与图片可访问性（FR-003）
    • 对公众可见 ⇔ status=PUBLISHED ∧ publishedAt ≤ now (BR-07)
```

### Revision
`(postId, revisionNo, snapshotMarkdown+frontmatter, author, createdAt,
note?)` — 仅追加；恢复会创建一个**新**修订，绝不回退。

### MediaAsset
`id, originalFilename, contentType (allowlist), bytes (≤5MB), sha256,
altText|null, decorative:bool, storageKey, width, height`。sha256 用于对相同
二进制去重，而嵌入点可以携带不同的替代文本。

### Release
`id, contentTree hash, includedPostIds[], feedVersion, sitemapVersion,
status (BUILDING|READY|DEPLOYED|FAILED), createdAt, deployedAt?`。
发布的原子单元（NFR-015）：Release 就是读者看到的东西，要么全有要么全无。

### Redirect
`fromPath, toPostId|toUrl, type (301|410), createdAt, reason`。受管不变量：
不形成链（重定向一跳解析）、不成环。

### Mention（Webmention）
`id, sourceUrl, targetPostId, type (REPLY|LIKE|REPOST|BOOKMARK|MENTION),
authorName?, authorUrl?, contentHtml (sanitized), receivedAt,
verifiedAt?, status (PENDING|APPROVED|REJECTED|BLOCKED)`。
幂等键：唯一 `(sourceUrl, targetPostId)`（BR-09）。

### Comment（可选聚合）
镜像 Mention，带 `name, url?, markdownBody, htmlSanitized, spamScore`。

## 关系（逻辑 ER）

```
Post 1──* Revision
Post *──* Tag          (normalized; post max 8)
Post ?──1 Series       (ordered position within series)
Post 1──* MediaAsset   (via ordered embeds)
Post 1──* Mention      (only verified ones approved)
Post 1──* Comment      (when native comments enabled)
Post 1──* FeedItem     (projection, GUID = canonicalUrl)
Release *──* Post      (posts included in a published tree)
Post 1──? Redirect     (when slug retired/merged)
```
