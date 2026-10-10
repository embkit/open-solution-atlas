# 03 · Glossary

> Bilingual key terms. **std** marks terms defined by a cited standard;
> others are pack usage.

| Term | 中文 | Definition |
|---|---|---|
| Ticket | 工单 | The single record of one work item (incident or request); the backbone object (BR-01) |
| Incident | 事件 (故障) | Unplanned interruption/degradation; type on the ticket core (**std** outcome set: ISO/IEC 20000-1 cl. 8.6.1) |
| Service request | 服务请求 | Pre-defined ask fulfilled from the catalog (**std** cl. 8.6.2) |
| Problem | 问题 | Record of root-cause work on recurrence/major incidents (**std** cl. 8.6.3) |
| Known error | 已知错误 | Documented cause + workaround awaiting fix (pack usage; ITIL vocabulary) |
| RFC (request for change) | 变更申请 | Change proposal with risk class and evidence (CTL-04) |
| CAB | 变更顾问委员会 | Assessment/approval body for normal changes (pack usage) |
| CI (configuration item) | 配置项 | Typed asset/element tracked with relationships (ADR-0004) |
| SLA | 服务级别协议 | Agreement target per service (**std** obligation: ISO/IEC 20000-1 cl. 8.3) |
| SLA clock | SLA 时钟 | Event-sourced response/resolution timer with pause/resume (BR-04, NFR-002) |
| Business calendar | 业务日历 | Effective-dated service hours/holidays per service (BR-05) |
| Escalation | 升级 | Functional (skill) or hierarchical (role) reassignment event (BR-06) |
| Entitlement | 可见/可操作范围 | Scope deciding who sees/acts on a ticket or article (BR-11, CTL-03) |
| KEDB | 知识库(已知错误库) | Known-error repository exposed to agents (FR-011) |
| Rule trace | 规则执行痕迹 | Stamp of rule id+version applied to a ticket (BR-14) |
| Drift | 配置漂移 | Discrepancy between observed and recorded CI state (FR-016) |
| MTTR | 平均修复时间 | Mean resolve duration per the report's stated start point (formulas in `non-functional.md`, FR-019) |
