# 00 · Industry Brief — Personal Publishing

## What business this system serves

An individual creator publishes long-form writing on their own domain and
keeps durable ownership of it. This is the smallest member of the *content
publishing* family; its larger relatives are headless CMS, newsroom
platforms, and multi-tenant SaaS blog hosts (all out of scope here).

The business model is typically indirect: the blog supports the author's
reputation, consulting, products, or recruiting — it is not itself a
transaction system.

## Value chain

```
author ──writes──▶ draft ──review/publish──▶ public page ──distribution──▶ reader
                                          │                    ├─ search
                                          │                    ├─ RSS reader
                                          │                    ├─ social/webmention
                                          │                    └─ inbound link
                                          └──◀── feedback: comments / mentions / analytics
```

## Market realities that shape the design

1. **Platform risk is the primary risk.** Writers who publish only on
   third-party platforms face account lockout, algorithm change, and URL
   loss. Own URL + full export is therefore a core capability, not a nice-to
   have.
2. **Traffic is spiky and low in aggregate.** Hundreds to low tens-of-
   thousands of monthly visits, with occasional spikes from external links.
   Peak throughput requirements are trivial; cost floor and durability
   matter more.
3. **The author is usually the sole operator.** There is no on-call team.
   The system must survive months of neglect and still be secure: immutable
   public artifacts, minimal server surface, automated TLS.
4. **The IndieWeb / POSSE model** (Publish on Own Site, Syndicate Elsewhere)
   is the established open practice: own canonical content, repost links to
   external networks, receive replies via Webmention.
5. **Durable authoring format.** Markdown in plain files has outlived a
   generation of CMS databases. Content must remain readable without the
   publishing software.

## Typical deployment contexts

| Context | Variant note |
|---|---|
| Static hosting + CDN (global) | default target; lowest cost & attack surface |
| Origin server with reverse proxy | where author wants fully self-hosted |
| Mainland China hosting | requires ICP filing; analytics/comment services chosen accordingly — see `variants/` (planned) |

## Sources

- IndieWeb wiki — <https://indieweb.org/> (POSSE, Webmention, Micropub)
- W3C Webmention Recommendation — <https://www.w3.org/TR/webmention/>
- W3C ActivityPub — <https://www.w3.org/TR/activitypub/>
