# 03-domain / Glossary

> **Purpose of this file at L1.** The pack's `AGENTS.md` requires the Chinese
> approval vocabulary to be *defined explicitly* rather than used as labels,
> because BPMN 2.0 defines none of it. This glossary is where those semantics
> are stated. A term defined here is used with exactly one meaning across the
> pack; no synonyms are introduced later.
>
> `Source` column records the basis: **[BPMN]** the OMG notation (cited),
> **[PACK]** a definition this pack contributes because no public standard
> defines it, **[STAT]** a statutory instrument, **[ENG]** a convention common
> to engines but not standardised. Anything not marked `[PACK]` and not cited
> is an assumption and must say so.

## 1. Core process objects

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Process definition** | 流程定义 | The versioned, published artefact describing how instances of one procedure advance. Not the running thing. | [PACK] |
| **Process instance** | 流程实例 | One execution of a process definition, with its own data, identity and history. | [BPMN] |
| **Token** | 令牌 | The abstract marker of position within an instance's control flow. Used here to reason about semantics; not necessarily an implementation choice. | [BPMN] |
| **Activity** | 活动 | A unit of work in a flow: task, sub-process, call activity. | [BPMN] |
| **Task** | 任务/待办 | A work item assigned to a participant. Distinct from BPMN *user task* — here, "task" is generic, "user task" is the human kind. | [PACK] |
| **Gateway** | 网关 | A point where the flow branches or merges: exclusive, inclusive, parallel, event-based, complex. | [BPMN] |
| **Event** | 事件 | Something that happens at a point in time: start, intermediate (message/timer/signal/error), end. | [BPMN] |
| **Sub-process** | 子流程 | An activity that is itself a process, embedded (shares parent scope) or reusable (independent). | [BPMN] |
| **Lane / participant** | 泳道/参与者 | The partition of a process by organisational role or system. | [BPMN] |
| **Multi-instance activity** | 多实例活动 | An activity repeated for a set of participants or items, with a completion condition. | [BPMN] |

## 2. Task vocabulary — the terms BPMN does not define

These six are the ones every Chinese OA deployment uses and every vendor
defines differently. **Each is defined here, in terms of the task's state
machine, so a specification is unambiguous.**

| Term | 中文 | Definition (state-machine level) | Source |
|---|---|---|---|
| **Assign** | 指派/分发 | A task is created **already owned** by a specific participant; it appears in their inbox and must not be claimed by another without transfer or re-assignment. | [PACK] |
| **Claim** | 签收/认领 | A task is created **unowned** (offered to a pool or group); a participant takes ownership. Ownership is exclusive once claimed. | [PACK] |
| **Transfer** | 转办 | A participant **relinquishes** the task to another, permanently. The original owner no longer holds it and cannot act on it afterwards. The transfer is an auditable event naming both parties. | [PACK] |
| **Delegate** | 代办/委托 | A participant **grants** another the right to act on a task **they still own**. The grant is bounded (scope and expiry). Actions taken by the delegate are recorded against the delegate *and* attributed to the delegating owner. | [PACK] |
| **Countersign** | 会签 | A group of participants must **all** act on the same work item for it to complete. "All act" is itself a policy: unanimous approval vs. all-responded (a rejection ends it). Multiple completion policies exist; the pack does not assume one. | [PACK] |
| **Or-sign** | 或签 | A work item completes when **any one** of a group acts. The others' tasks are cancelled or simply never become actionable — which of the two is a policy that must be stated, not assumed. | [PACK] |
| **Add-sign** | 加签 | A participant **inserts an additional approver** into an in-flight flow, before their own approval. The added approver acts after the insertion and before the original sequence continues. | [PACK] |
| **Return for rework** | 退回 | The flow moves **backwards** to a previous activity or to the applicant. Two distinct semantics exist and must never be conflated: **reject** (terminates the instance) vs. **rework** (returns to the applicant, may be resubmitted). | [PACK] |
| **Withdraw** | 撤回 | The **applicant** retracts the instance before a terminal decision. Only the applicant (or the process owner) may withdraw, and only while no binding decision has been recorded. | [PACK] |
| **Add-comment** | 加签意见/批注 | A non-binding annotation attached to the instance or a task. Never changes control flow. | [PACK] |

> ⚠️ ASSUMPTION: several of these terms (会签/或签/加签 in particular) are in
> wide daily use but have **no standard definition** — not in BPMN, not in
> DMN. The definitions above are this pack's contribution and are labelled as
> such. A reader who needs the semantics a *specific product* implements must
> check that product's documentation; the pack's job is to state semantics
> precisely enough that a product can be measured against it.

## 3. Approval, routing & time

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Approval condition** | 审批条件 | The predicate deciding whether a given approver must act on a given instance (amount, type, department, risk). | [PACK] |
| **Approval chain** | 审批链 | The ordered sequence of approvers an instance must pass. | [PACK] |
| **Escalation** | 催办/升级 | Automatic action when a task outlives its timer: remind, reassign, or route to a superior. The trigger, the action and the authority to authorise it are three separate decisions. | [PACK] |
| **Business calendar** | 工作日历 | The calendar against which SLA durations are measured (working days, holidays, working hours). | [PACK] |
| **SLA / deadline** | 办理时限 | The committed completion window for an instance or task, measured on the business calendar. | [PACK] |
| **Timer event** | 定时事件 | An event that fires on a schedule or after a duration; drives reminders, deadlines, auto-approval (where permitted). | [BPMN] |
| **Auto-approval on timeout** | 超时自动通过 | Terminal automatic approval when a timer expires. **Highly contentious**: permitted only by explicit policy, never as a default, because it converts a human control into an implicit consent. | [PACK] |
| **SoD constraint** | 职责分离约束 | A rule preventing one participant from holding two roles that must not combine (e.g. applicant and seal custodian). The rule source is the IAM pack; this pack consumes it. | [PACK] |

## 4. Documents, 公文 and records

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Official document (公文)** | 公文 | A document issued under the authority of an organisation, in a prescribed format, carrying institutional weight. | [STAT] |
| **公文 format** | 公文格式 | The layout rules for an official document: paper, elements, pagination, specific formats. | [STAT] GB/T 9704-2012 |
| **Electronic 公文 structure** | 电子公文结构 | The structural model for a digital official document — the more relevant standard for a digital flow than the paper-era format. | [STAT] GB/T 33476.1-2016 (candidate) |
| **Document number (文号)** | 发文字号/文号 | The identifier allocated to an official document, unique within its issuing authority and sequence. Allocation must be gapless, non-reusable and auditable. | [PACK] |
| **Draft / review / issue (核稿/签发)** | 拟稿/核稿/签发 | The drafting circulation of a 公文 before issuance: drafting, review for correctness, and final authorisation to issue. | [PACK] |
| **Archive (归档)** | 归档 | The transfer of a completed record into long-term retention under a records authority. | [PACK] |
| **Retention schedule** | 保管期限 | How long a record class must be kept, and what happens at expiry (disposal requires authority). | [PACK] |
| **Electronic signature** | 电子签名 | Data attached to or contained in a data message, identifying the signer and indicating their recognition of its content. | [STAT] 电子签名法 第二条 |
| **Reliable electronic signature** | 可靠的电子签名 | One whose creation data is exclusive to the signer, controlled by them at signing, and where later alteration of either the signature or the message is detectable — and which therefore has the same legal effect as handwriting or a seal. | [STAT] 电子签名法 第十三条、第十四条 |
| **Data message (数据电文)** | 数据电文 | Information generated, sent, received or stored by electronic, optical or similar means. | [STAT] 电子签名法 第二条 |
| **Electronic seal (电子签章)** | 电子签章 | The institutional counterpart of a signature: a seal applied in electronic form. Standards and providers are deliberately not named at L1. | [PACK] |
| **Integrity verification** | 完整性校验 | The ability to *detect* alteration of a stored document or signature — not merely to detect loss. This is a legal requirement, not a feature. | [STAT] 电子签名法 第十三条 |

## 5. Audit, replay & operations

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Event** | 事件 | An immutable record that something happened: type, actor, timestamp, instance, payload reference. | [PACK] |
| **Audit trail** | 审计轨迹 | The ordered, append-only record of all events for an instance. Never updated, never deleted, only superseded by compensating events. | [PACK] |
| **Replay** | 重放 | Reconstructing an instance's history — or re-executing it — from its event log. Two distinct meanings: **reconstruction** (read-only, for audit) and **re-execution** (rebuild state from events). The pack requires the first, and treats the second as a design option. | [PACK] |
| **Tamper evidence** | 防篡改 | Alteration of the trail is detectable, not merely prevented. Detection is what an audit can rely on. | [PACK] |
| **Compensating event** | 补偿事件 | An event recorded to correct or reverse a prior one. The prior event is never edited. | [BPMN]/[PACK] |
| **Event log export** | 事件日志导出 | The bulk export of the trail for analysis. The interchange format is deliberately unspecified at L1. | [PACK] |

## 6. Conventions

- **"must not" vs. "should"**: this pack uses them with their ordinary
  engineering force — *must not* marks a rule whose violation is a defect.
- **Bilingual terms**: Chinese terms are authoritative for the Chinese
  approval vocabulary (section 2) because that is where ambiguity lives;
  English terms are authoritative for BPMN notation concepts.
- **No synonyms**: once a term is defined here, later chapters use it
  verbatim. If a chapter needs a different distinction, it defines a new term
  rather than stretching an existing one.
