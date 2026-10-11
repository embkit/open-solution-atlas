# SOURCES — Workflow, BPM & Office Automation Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Process modeling vocabulary (flow, gateway, timers, signals; instance/task lifecycle) | OMG | BPMN 2.0.2 — https://www.omg.org/spec/BPMN/2.0.2/ | Pack anchors modeling vocab here; conformance depth is an open question |
| Decision / rule modeling (approval conditions, gateways) | OMG | DMN — https://www.omg.org/spec/DMN/ | Candidate for approval-rule semantics at L2 |
| Document & records management (公文/DMS, templates, retention) | OASIS | CMIS 1.1 — https://docs.oasis-open.org/cmis/CMIS/v1.1/ | Candidate for the document-management chapter |
| Verifiable credentials for e-seal / signature attestation | W3C | Verifiable Credentials Data Model — https://www.w3.org/TR/vc-data-model/ | CN e-seal specifics belong in a variant |
| ISMS controls (audit, access control) | ISO/IEC | ISO/IEC 27001 — https://www.iso.org/standard/27001 | Clause mapping to confirm |
| CN graded protection overlay | — | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | Standard number; mapping to confirm |
| CN electronic signature | — | 中华人民共和国电子签名法 | Statute (2004, amended); article-level mapping to confirm |
| 公文格式 (official-document format) | — | GB/T 9704 党政机关公文格式 | Candidate standard for 公文 layout; version/article to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Service callbacks / process data API over HTTP | IETF | RFC 9110 (HTTP Semantics) — https://www.rfc-editor.org/rfc/rfc9110 | Applies once the API chapter exists (L2/L3) |
| Signed process callbacks / webhook authenticity | IETF | RFC 7515 (JWS) / RFC 7519 (JWT) — https://www.rfc-editor.org/rfc/rfc7519 | Candidate mechanism; not yet specified |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| BPMN engine (execution semantics) | Camunda 7 / Zeebe (Camunda 8) | https://camunda.com/ | Reference for engine + external-task pattern |
| BPMN engine | Flowable | https://www.flowable.com/ | |
| BPMN engine | Activiti | https://www.activiti.org/ | |
| BPMN / jBPM | jBPM | https://www.jbpm.org/ | |
| Dynamic forms + JSON schema | Form.io | https://www.form.io/ | Form-engine reference |
| Enterprise document/content management | Alfresco | https://www.alfresco.com/ | DMS/records reference |
| CN open-source OA platform | RuoYi (若依) | https://gitee.com/y_project/RuoYi | Illustrative CN OA patterns (variant-scope) |

## 4. Uncited specifics to resolve

Still open (each blocks `source-checked`):

- **Chinese approval semantics** — 会签/或签/加签/转办/退回. Not defined by
  BPMN 2.0. Now **defined at L1** in `03-domain/glossary.md` §2 as this pack's
  contribution, and labelled `[PACK]` because no public standard defines them.
  Still open: the completion policies (does 会签 end on any rejection? does
  或签 cancel the other tasks or merely never surface them?) — these are
  decisions to make at L2, not lookups.
- **BPMN conformance depth** — full execution semantics vs. a pragmatic subset
  remains an open question (§Open questions #1); no conformance class/target
  is stated, and this pack deliberately claims none.
- **公文/文号管理** — drafting/核稿/签发/文号/归档 rules are CN-specific.
  GB/T 9704-2012 (paper layout) and GB/T 33476.1-2016 (electronic structure,
  scope/clauses not yet verified) are now cited in
  `00-context/regulatory-landscape.md`. Still open: 文号 allocation rules
  (gapless? reusable? per-authority sequence?) — a policy decision.
- **电子签章 integration** — article-level obligations from 《电子签名法》 are
  now cited in `00-context/regulatory-landscape.md` §2 (arts. 3, 4, 5, 6, 13,
  14; 2004/2015/2019 versions, re-confirmed current in the 2026-10 citation
  audit). **Updated:** the *governing rule* for seals is 《电子印章管理办法》
  (国办发〔2025〕33号, effective on promulgation 2025-09-27) — arts. 5, 16, 17,
  21, 22, 23 are now cited, covering legal effect, certificate-validity bounds,
  the mandatory **seal status query service**, "谁所有、谁控制，谁签章、谁负责",
  sealing-process record retention, and point-in-time validity verification.
  Still open: the **technical standard number** for the seal data format and
  interface — 第十六条 defers to "国家有关标准规范" without naming one, so none is
  cited.
- **Auditability & replay** — the AGENTS.md rule now has definitions in
  `03-domain/glossary.md` §5 (audit trail, replay-as-reconstruction vs.
  re-execution, tamper evidence, compensating events). Still open: measurable
  targets — retention period, ordering guarantee, integrity mechanism.
- **Approval analytics / process mining** — depth undecided; no event-log
  interchange standard confirmed (IEEE 1849 XES is a candidate; standard
  number to be verified before any conformance claim).
- **SLA / timeout / escalation** — terms defined in `03-domain/glossary.md`
  §3; still open: thresholds, business-calendar semantics, pause/resume
  behaviour, and whether auto-approval-on-timeout is permitted at all
  (this pack's position: only by explicit policy, never by default).
- **SoD constraints** — the rule source is the IAM pack; this pack consumes it.
  No rule specifics here, by design.
- **Form-engine validation / conditional visibility** — no schema standard or
  expression language chosen; deferred to L2.
