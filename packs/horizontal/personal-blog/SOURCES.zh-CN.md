# SOURCES — 个人博客与内容发布

> 来源台账。把承重的论断映射到公开、可核查的来源；无法追溯的内容列在第 4 节，
> 并在各章中标注 `> ⚠️ ASSUMPTION:`。
>
> **状态：`source-checked`**（2026-10-09）。来源性质：`llm-drafted`。
> 验证状态：`source-checked` — **未**经现场验证。见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。
>
> 来源核对于 2026-10-09。结果：(a) LCP ≤ 2.5 秒追溯到 Core Web Vitals 指南
> （本方案包的 CLS ≤ 0.05 比公开的 0.1 更严格，因此仍是假设）；(b) EN 301 549
> 锁定到协调版本 v3.2.1（2021-08-18）；(c) ICP 备案与 DMCA 安全港说明给出
> 工具级引用；(d) PIPL 锁定到 2021 年法案。其余全部数值目标仍是已声明的
> 假设（第 4 节）。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| Markdown 创作格式（BR-02、NFR-011） | CommonMark | CommonMark 规范 — https://spec.commonmark.org/ | 规定语法；不强制编辑器/自动保存行为 |
| Webmention 接收/验证/发送（BR-09、FR-013/FR-014、AC-013/AC-014） | W3C | Webmention（W3C 建议标准，2017）— https://www.w3.org/TR/webmention/ | 按 `(source, target)` 幂等是本方案包的规则，规范本身并不要求 |
| 提及/回复所用的微格式2 标记 | Microformats | microformats2 — https://microformats.org/wiki/microformats2 | |
| 联邦协议（未来变体，ADR-0003） | W3C | ActivityPub（W3C 建议标准）— https://www.w3.org/TR/activitypub/ | 延后到变体，不属内核 |
| RSS 2.0 订阅源（FR-011、NFR-010、AC-011） | RSS 顾问委员会 | RSS 2.0 规范 — https://www.rssboard.org/rss-specification | |
| 订阅源校验（AC-011） | W3C | W3C Feed Validator — https://validator.w3.org/feed/ | 是工具，不是规范 |
| 站点地图（FR-012、AC-012） | sitemaps.org | 站点地图协议 — https://www.sitemaps.org/protocol.html | |
| 社交/正本预览元数据（FR-012） | Open Graph | The Open Graph protocol — https://ogp.me/ | |
| JSON-LD `Article` 结构化数据（AC-012） | schema.org | schema.org/Article — https://schema.org/Article | |
| 可选的替代订阅源 | JSON Feed | JSON Feed 1.1 — https://www.jsonfeed.org/version/1.1/ | 本方案包不要求 |
| 发布方推送通知（可选） | W3C | WebSub — https://www.w3.org/TR/websub/ | |
| 公开页面的可访问性（NFR-009、BR-10、CTL） | W3C | WCAG 2.1 — https://www.w3.org/TR/WCAG21/ ；非文本内容义务：SC **1.1.1**（A 级）；本方案包目标为 AA 级 | 方案包中标明了 AA 级 |
| 可访问性采购（面向公共部门） | ETSI/CEN/CENELEC | **EN 301 549 v3.2.1**，依据欧盟《无障碍指令》2021-08-18 协调 — https://digital-strategy.ec.europa.eu/en/policies/web-accessibility-directive-standards-and-harmonisation | v2.1.2（2018）已被取代；条款级映射仍待完成（第 4 节） |
| 加载性能阈值（NFR-001、AC-N01） | Google web.dev | **Core Web Vitals**：LCP ≤ 2.5 秒、CLS ≤ 0.1（「良好」阈值；≥ 75 % 访问）— https://web.dev/vitals/ | 本方案包从此指南采用 LCP 2.5 秒；方案包的 CLS ≤ 0.05 比 0.1 **更严格** → 第 4 节假设；TTFB ≤ 200 毫秒没有 CWV 来源 → 第 4 节 |
| 隐私制度（CTL-001……） | 欧盟 | GDPR（欧盟 2016/679）— https://gdpr-info.eu/ | |
| 隐私制度（CCPA/CPRA） | 加州总检察长 | https://oag.ca.gov/privacy/ccpa | |
| 隐私制度（中国） | 全国人民代表大会 | 《中华人民共和国个人信息保护法》(PIPL) — 2021-08-30 通过，2021-11-01 施行；合法性基础**第 13 条**，个人权利**第 44–50 条** | 经人大网获取 URL；条款按条引用 |
| 版权 / 下架联系方式（法规说明） | 美国国会 | **17 U.S.C. §512(c)**（托管安全港；§512(c)(3) 通知、§512(g) 反通知） | 按款引用法规 |
| 中国托管说明（法规环境） | 国务院（中国） | 《互联网信息服务管理办法》(国务院令第292号，2011 修订) **第 4 条** — 非经营性互联网信息服务实行备案制度 (ICP 备案) | 工具级引用；执行实践各地有差异 |

## 2. 规范性文件（RFC / 官方规范）

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| Atom 订阅源（FR-011、NFR-010、AC-011） | IETF | RFC 4287（Atom Syndication Format）— https://www.rfc-editor.org/rfc/rfc4287 | |
| AtomPub（可选的发布 API） | IETF | RFC 5023 — https://www.rfc-editor.org/rfc/rfc5023 | |
| BR-06/AC-003/AC-010/AC-015 的 HTTP 状态语义（301、410、415、413、429） | IETF | RFC 9110（HTTP 语义）— https://www.rfc-editor.org/rfc/rfc9110 | 这些状态码是标准的；本方案包对它们的使用是设计选择 |
| CDN 缓存语义（NFR-001、NFR-003） | IETF | RFC 9111（HTTP 缓存）— https://www.rfc-editor.org/rfc/rfc9111 | |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| 静态站点生成（ADR-0001/0002） | Hugo | https://gohugo.io/ | 静态优先构建/部署的参考 |
| 静态站点生成 | Eleventy (11ty) | https://www.11ty.dev/ | |
| 静态站点生成 | Astro | https://astro.build/ | |
| 静态站点生成 | Jekyll | https://jekyllrb.com/ | |
| 动态 CMS 替代方案 | WordPress | https://wordpress.org/ | 与静态优先立场形成对照 |
| 动态 CMS 替代方案 | Ghost | https://ghost.org/ | |
| 客户端检索（FR-007、AC-007） | Pagefind | https://pagefind.app/ | 本方案包要求无网络的检索 |
| 客户端检索 | Lunr.js | https://lunrjs.com/ | |
| Webmention 端点（FR-013） | webmention.io | https://webmention.io/ | |
| POSSE / 桥接（ADR-0003） | Bridgy | https://brid.gy/ | |
| ActivityPub 参考（变体） | Mastodon | https://joinmastodon.org/ | |
| LCP/CLS 测量（AC-N01） | Chrome Lighthouse | https://developer.chrome.com/docs/lighthouse/overview/ | |
| 结构化数据校验（AC-012） | schema.org Validator | https://validator.schema.org/ | |
| IndieWeb 模式（ADR-0003） | IndieWeb | https://indieweb.org/ | 是社区，不是规范机构 |

## 4. 待厘清的未引用细节

- **NFR-001 / AC-N01** — `TTFB ≤ 200 毫秒（CDN 命中）` 与 `CLS ≤ 0.05` 是
  内部目标：TTFB 没有 Core Web Vitals 来源，CLS 0.05 比公开的 0.1「良好」
  阈值更严格（LCP 2.5 秒*有*来源——见第 1 节 Core Web Vitals 行）。
- **NFR-002 / AC-001 / AC-002** — 编辑器自动保存 `≤ 1 秒 p95`、预览渲染
  `≤ 300 毫秒（2 万字文章）`、自动保存在 `5 秒` 内触发。没有任何基准或来源；
  作为设计目标采纳。
- **NFR-003 / AC-N03** — 「到 100 万次请求/天都不需要容量规划」与「能承受
  100 倍流量尖峰」。这是未经验证的容量论断；完全取决于所选 CDN/托管。
- **NFR-004 / NFR-006** — `99.9 %/月` 可用性、发布延迟 `≤ 60 秒`。是没有
  合同/来源依据的随意目标。
- **NFR-005 / AC-N04** — 内容丢失窗口 `≤ 5 分钟`、镜像到 `≥ 2 个位置`、
  每周恢复演练。备份数字是方案包策略，非来源事实。
- **NFR-008** — 「读者 IP 不存储超过 24 小时」。留存期是策略选择；它不与任何
  规定冲突，但欧盟指南把 IP 视为个人数据（见法规环境）；需针对具体制度确认。
- **NFR-014 / AC-N05** — 基线下的生产成本 `≤ 5 美元/月`。取决于定价（免费
  额度会变）；无法作为常量核验。
- **BR-03 / BR-05** — slug `最长 80 字符`、每篇文章 `最多 8 个标签`。没有
  外部依据的内部卫生限制。
- **BR-10 / AC-003** — 强制的非空替代文本；`6 MB PNG → 413`、非图片上传
  `→ 415`。体积/类型限制是随意的；替代文本要求源自 WCAG（2.1 AA §1.1.1），
  但强制边界是方案包的选择。
- **AC-007** — 在未定义的「参考设备」上，`500 篇文章索引内 ≤ 300 毫秒` 的
  检索。基准未定义也未测量。
- **AC-011** — 订阅源只暴露「最新 20 篇文章」。这是常见做法而非规范要求；
  数字 20 是随意的。
- **可观测性 SLO** — 「发布到可见 ≤ 120 秒（≤ 500 篇时）」、「webmention
  5 分钟内可见」、「3 次尝试失败 → 告警」、「备份超过 36 小时未更新」。这些
  是凭空设定的运行阈值；无来源。
- **NFR-010 / NFR-012** — 「当前版 + 上一大版本」浏览器、`320 像素–2560
  像素`、单命令部署、`≤ 30 分钟` 从零到建站。支持矩阵与上手论断未经核验。
- **EN 301 549 / WCAG / 隐私条款级映射** — 工具与版本已锁定（第 1 节）；
  具体的条款 → 方案包控制项映射仍需在任何合规论断之前写出。
- **ICP 备案与 DMCA 实践** — 工具级引用在第 1 节；属地特定的适用指引是
  部署工作，不是方案包内容。
