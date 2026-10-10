# One-Stop Government Service Platform / 政务服务一网通办平台

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | government-public / government-services |
| Stack stance | Vendor-neutral |
| Regulatory context | 网络安全法、数据安全法、个人信息保护法; 等保2.0（三级基线典型）; 政务服务相关行政法规与电子证照/电子签章国家标准 |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The integrated service portal and approval backbone of a digital government:
citizens and enterprises handle affairs ("一件事") on one website/app instead
of visiting departments. It unifies service guides, online application,
cross-department data sharing and verification, approval workflow, electronic
licenses/seals, payment of administrative fees, progress tracking, and
"好差评" satisfaction feedback, while satisfying classified-protection and
government cloud deployment requirements.

## In scope

- Unified service catalog: 事项管理, guide elements (受理条件/材料/流程/
  时限), region/department ownership, item versioning
- Personal & corporate space: unified real-name identity (对接政务实名),
  my applications, my licenses, message center
- Application: smart forms, material upload with OCR/电子证照免提交,
  prefill via data sharing, 一件事一次办 orchestrated packages
- Approval backbone: department task routing, acceptance (受理) → review
  (审查) → decision (决定) → issuance (出件), SLA timers, 限时办结,
  supplement-once (一次性告知) rules
- Inter-department verification: data sharing request/response gateway,
  interface catalog, consent/authorization records, call audit
- Electronic results: e-license (电子证照) issuance/verification, e-seal,
  certificate verification QR
- Payment & logistics: administrative fee payment gateway, document mailing
- Supervision & feedback: 好差评, complaint handling, oversight dashboards,
  full business audit (电子监察)
- Deployment: government-cloud zones, network segmentation, level-3 MLPS

## Out of scope (explicitly)

- Department-internal professional systems (业务审批专网系统) — they are
  connected as approving nodes, not rebuilt here
- Government OA/internal office (sibling workflow pack pattern)
- Public data open portal (sibling data-exchange pack candidate)

## Open questions

1. Cross-region/跨层级 (省–市–区–街道) routing model depth.
2. Interface-sharing gateway vs. data-exchange platform boundary.
3. 电子证照库 treated as external platform dependency with standard
   integration contract.

## Maturity roadmap

- [x] L1 — Brief
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven
