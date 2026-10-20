# 01 · 核心业务流程

## BP-01 发布一篇文章（端到端）

```
author creates draft (CAP-01.1)
   │  autosave each edit (CAP-01.2)
   ▼
author attaches media, sets tags/slug/summary/license (CAP-01.3/01.4, CAP-02.1)
   │
   ▼
preview ──不满意──▶ edit loop
   │ satisfied
   ▼
publish now ──or── schedule for future time (CAP-03.1/03.2)
   │
   ▼
build static artifacts → deploy → CDN invalidate (CAP-03.4)
   │
   ├──▶ feed/sitemap regenerated (CAP-04.1/04.2)
   └──▶ optional: author manually syndicates canonical link (CAP-04.3)
```

- 草稿的 slug 可以自由更改；**首次发布之后 slug 即不可变**——改名需要显式的
  重定向（规则 BR-06）。
- 定时发布的文章在声明的容差范围内发布（见 NFR-006），而非精确到秒。

## BP-02 接收并展示一条回应（Webmention）

```
external site posts a response linking to a post
   │  sends Webmention(source, target) to endpoint (CAP-05.1)
   ▼
validate target exists locally; fetch source; verify link-back exists
   │ fail ──▶ reject (4xx), no state persisted
   ▼
classify type (reply / like / repost / bookmark) + store as PENDING
   │
   ▼
moderation queue (CAP-05.2) ──reject──▶ discarded + sender blocked option
   │ approve
   ▼
published mention appears under target post; spam never rendered
```

针对同一 `(source, target)` 的重复 Webmention 会更新既有记录，而不是新建一条
（幂等性，BR-09）。

## BP-03 编辑或撤回已发布内容

```
author edits published post → new revision (CAP-01.2)
   │  republish rebuilds page; feeds contain updated content with same GUID
   ▼
author unpublishes → URL returns 410 Gone with explanation page
   │  (deletion) or 301 redirect (merge/rename) (CAP-03.3, BR-07)
   ▼
search index, sitemap, feeds all consistent with current state
```

## BP-04 读者的发现与回访

```
reader lands from search/referral → post page (SEO metadata, canonical)
   ├──▶ navigates tag/archive/series (CAP-02.1/02.2)
   ├──▶ uses site search (CAP-02.3)
   └──▶ subscribes RSS (CAP-04.1) → reader polls feed → sees new post
```

## BP-05 退出 / 迁移（所有权保障）

```
author triggers full export (CAP-07.1)
   ▼
zip/tar: Markdown files + frontmatter + media + taxonomy + mentions
   │  open formats only; readable without this software
   ▶
restore into a fresh install or a different engine
```
