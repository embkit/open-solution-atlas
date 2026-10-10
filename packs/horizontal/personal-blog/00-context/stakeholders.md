# 00 · Stakeholders

| Actor | Role | Goals | Constraints / concerns |
|---|---|---|---|
| **Author / Owner** | Sole content owner; usually also operator | Write comfortably; publish reliably; keep ownership and audience; low operating cost; minimal maintenance | Non-expert in ops; may go months without touching the system |
| **Reader (anonymous)** | Public visitor | Read fast on any device/network; find old posts; subscribe | Expects instant load; no mandatory login; hostile to intrusive tracking |
| **Reader (commenting)** | Interacting visitor | Leave a reply without creating an account | Spam exposure; may comment from their own site (Webmention) instead |
| **RSS/Atom subscriber** | Machine actor (feed reader) | Reliable, valid feed with stable GUIDs and sane update semantics | Broken feed = silent audience loss |
| **Search crawler** | Machine actor | Discover content; understand canonical URLs | Sitemap validity, metadata correctness |
| **External platforms** | Syndication targets (social, aggregators) | Receive canonical links, send mentions back | APIs change; treated as optional, replaceable |
| **Author's future self / migration target** | Maintenance actor | Export everything in a portable format with zero lock-in | Must work without the original software running |

## Trust boundaries (summary; detail in 04-architecture/security.md)

- **Public zone**: static pages, feeds, sitemap — no secrets, no write paths.
- **Authoring zone**: draft editing, media upload, publish actions — single
  authenticated identity, every action attributable.
- **Ingestion edge**: incoming Webmentions — untrusted external input;
  verified, queued, moderated, never rendered raw.
