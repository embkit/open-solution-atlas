# 01 · Business Capability Map

Level-1 capabilities with level-2 decomposition. Capability IDs (`CAP-xx`)
are the anchor that functional requirements trace back to.

```
PERSONAL PUBLISHING
├── CAP-01 Authoring 写作
│   ├── CAP-01.1 Markdown editing & live preview
│   ├── CAP-01.2 Draft autosave & revision history
│   ├── CAP-01.3 Media library (upload, alt text, provenance)
│   └── CAP-01.4 Metadata editing (title, slug, tags, summary, license)
│
├── CAP-02 Organization 组织
│   ├── CAP-02.1 Taxonomy (tags / categories / series)
│   ├── CAP-02.2 Archive (date, tag, category index pages)
│   └── CAP-02.3 Site search over published content
│
├── CAP-03 Publishing 发布
│   ├── CAP-03.1 Publish / unpublish workflow
│   ├── CAP-03.2 Scheduled publishing
│   ├── CAP-03.3 Canonical URL & redirect management
│   └── CAP-03.4 Static build & CDN distribution
│
├── CAP-04 Distribution 分发
│   ├── CAP-04.1 RSS/Atom feed
│   ├── CAP-04.2 Sitemap & SEO metadata (OG/Twitter/JSON-LD)
│   ├── CAP-04.3 POSSE syndication links (manual/optional)
│   └── CAP-04.4 Email/newsletter bridge (optional via feed)
│
├── CAP-05 Interaction 互动
│   ├── CAP-05.1 Webmention receiving & verification
│   ├── CAP-05.2 Moderation queue (approve / reject / block)
│   └── CAP-05.3 Native comment form (optional, moderated)
│
├── CAP-06 Insight 洞察
│   ├── CAP-06.1 Privacy-preserving page analytics
│   └── CAP-06.2 Feed subscriber / referrer visibility (coarse)
│
└── CAP-07 Ownership 主权保障
    ├── CAP-07.1 Full content export (Markdown + media + metadata)
    ├── CAP-07.2 Backup / restore
    └── CAP-07.3 Migration-friendly structure (no proprietary format)
```

## Capability priorities

| Must (MVP) | Should | Could |
|---|---|---|
| CAP-01, CAP-02 (tags/archive), CAP-03, CAP-04.1, CAP-04.2, CAP-05.1/05.2, CAP-06.1, CAP-07 | CAP-02.3 search, CAP-03.2 scheduling, CAP-05.3 native comments | CAP-04.3 POSSE automation, CAP-04.4 newsletter bridge |
