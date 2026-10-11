# 00-context / Industry Brief — One-Stop Government Service Platform (一网通办)

## 1. What this system is in the value chain

A citizen or a business should not have to learn which department owns their
problem. A **一网通办** (integrated online government service) platform is the
system that makes one matter — **一件事** — a single, trackable, online
affair, regardless of how many departments must act on it.

It is the **front door**. The `data-exchange` sibling pack is its data
substrate; this pack is what the citizen and the enterprise actually touch:

```
   政务部门 (providers)                  行政相对人 (citizens & enterprises)
   ─────────────────────                 ──────────────────────────────────
   service catalogue (事项)      ┌──────────────────────────┐
   approval back-office  ───────▶│  一体化在线政务服务平台   │
   e-licence / e-seal    ───────▶│  (one-stop service)       │
   fee payment           ───────▶│                           │
   supervision (监管)     ───────▶│  submit · track · sign   │
   archives              ───────▶│  pay · rate (好差评)      │
                                    └──────────────────────────┘
                                             │  ▲
                                             ▼  │
                    shared data (population, licence, credit, …)
                    national unified identity (一次认证)
                    e-licence & e-seal shared services
```

The structural commitment is in 《国务院关于在线政务服务的若干规定》
(国务院令第716号): except where law provides otherwise or state secrets are
involved, 政务服务事项 **shall** be handled on the integrated platform
(第四条). This is not a convenience programme — it is an obligation, and it is
why the platform is the root of a department's digital service delivery.

## 2. The catalog root: 事项 (the service item)

The pack's `AGENTS.md` names the **事项 as the catalog root**, and this is the
single most consequential modelling decision in the system. Almost everything
else hangs off it:

```
   事项 (service item)  ── the root object
   │
   ├── 办事指南 (service guide): 受理条件 · 办事材料 · 办理流程   ← 国令716号 第六条
   ├── form(s)              ── what the applicant fills
   ├── materials (材料清单)  ── what must be uploaded, and which are exempt
   ├── approval lifecycle   ── 受理 → 审查 → 决定 → 出件
   ├── SLA (办理时限)       ── 限时办结
   ├── fee items (收费项目)  ── if any
   ├── result artefact      ── 决定书 / 电子证照
   ├── licence templates    ── if the result is a 证照
   └── evidence & archive   ── 电子文件归档
```

Because 第六条 requires the guide to declare 受理条件、办事材料、办理流程, the
事项 is not a catalogue label — it is the unit that *drives* form generation,
material requirements, routing and deadlines. A platform where the 事项 is one
object and the form is another will drift, and the two will contradict.

## 3. The provision that defines the platform's value

第七条 is the clause that gives 一网通办 its purpose:

> 政务服务机构通过数据共享能够获得的信息，不得要求行政相对人另行提供。

**Information the agency can already obtain through data sharing must not be
demanded from the applicant a second time.**

> This is the anti-double-submission rule, and it is a hard constraint on the
> system, not a service aspiration. It means a form field is not a UI decision:
> every field that duplicates a shared data source is a compliance defect if it
> is *required*. The `data-exchange` pack is what makes the rule satisfiable;
> this pack must be built so that the exception is auditable rather than silent.

## 4. Core flows (L1 view)

1. **Find** — the applicant searches the catalogue and reads the published
   办事指南 (第六条: the guide **shall** be published on the platform).
2. **Authenticate once** — 一次认证、全网通办 via the national unified
   authentication system (第五条).
3. **Pre-fill / verify** — data obtained through sharing is used to pre-fill and
   to verify, instead of being requested (第七条). Cross-department calls are
   consented and audited (`AGENTS.md`).
4. **Submit** — forms, materials, consent statements; the instance (办件) is
   created and tracked.
5. **Accept or 一次性告知** — the agency either 受理, or gives a **一次性告知**
   listing everything missing, once, rather than rejecting piecemeal.
6. **审查 / 决定** — the approval lifecycle runs to a decision within 限时办结.
7. **出件 & sign** — the result is issued; an electronic seal is applied and an
   electronic licence produced where the result is a 证照 (第九条/第十条).
8. **Settle** — administrative fees, where applicable.
9. **Rate** — 好差评 feedback closes the loop.
10. **Archive** — electronic files are archived in electronic form (第十二条).

## 5. Why this system is unusually hard to get right

- **The catalog is the contract with the public.** The 办事指南 is published;
  an applicant is entitled to rely on it. A platform that changes 受理条件
  silently is not merely inconsistent, it is unlawful.
- **"One thing" is a composite, not a copy.** 一件事 spans multiple
  departments, each with its own legal basis, its own decision, and its own
  liability. The platform must present one journey without erasing whose
  decision is whose.
- **The anti-double-submission rule fights the platform's own convenience.**
  Requiring a document is easy; proving it is already available is hard. A
  platform that defaults to asking will look friendlier and be non-compliant.
- **Electronic artefacts carry statutory weight.** 电子印章 and 电子证照 have
  the same legal effect as their paper counterparts (第九条/第十条), and
  electronic archives likewise (第十二条). Integrity, signing and archiving stop
  being engineering preferences.
- **Dependencies are national and external.** Unified identity, the e-seal
  system and the e-licence sharing service are **platforms, not features**
  (`AGENTS.md`): the pack must integrate them via their published standards and
  must never re-implement them. Re-implementing a seal or an identity is both
  non-compliant and a security liability.
- **Legacy processes must survive migration.** 国发〔2022〕5号 makes integration
  and data sharing a condition of project approval and acceptance — so the hard
  problem is usually coexistence, not greenfield.
- **Offline and assisted channels still exist.** Excluding elderly, disabled and
  remote populations is a failure mode the platform is explicitly required to
  avoid, which constrains the channel strategy rather than just the UI.

## 6. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Net-material reduction (materials demanded per 事项 vs. baseline) | whether the anti-double-submission rule is actually working |
| 一次性告知 rate & completeness | whether applicants are told everything missing, once |
| 限时办结 rate per 事项 & per department | whether the committed deadline is met |
| Online completion rate (全流程网上办理) | whether the platform is the real channel, not a front for offline |
| Re-submission rate (补正次数) | whether guides are accurate at first pass |
| Cross-department call latency & consent coverage | whether shared-data verification is fast and lawful |
| Archive completeness (electronic, per 第十二条) | whether records survive in the required form |
| Good/bad rating (好差评) distribution & response | whether feedback changes anything |

## 7. Public materials anchoring the model

**Administrative regulation (cited, article-level):**

- **《国务院关于在线政务服务的若干规定》** (国务院令第716号, 2019-04-26 公布,
  自公布之日起施行) — the platform's founding obligation. Articles used:
  第四条 (事项纳入一体化平台), 第五条 (统一身份认证/一次认证), 第六条
  (办事指南三项要素), **第七条 (不得重复要求提供可共享获得的信息)**,
  第九条 (统一电子印章系统/同等效力), 第十条 (电子证照共享服务系统/同等
  效力), 第十一条 (可作为办理依据), 第十二条 (电子文件归档/电子档案同等
  效力), 第十五条 (电子签名/印章/证照/档案的定义). Official text: 司法部
  国家行政法规库 https://xzfg.moj.gov.cn/front/law/detail?LawID=445 ; 国务院公报
  https://www.gov.cn/gongbao/content/2019/content_5389312.htm
- **《国务院关于加快推进政务服务标准化规范化便利化的指导意见》**
  (国发〔2022〕5号) — mandates that departments able to use the national
  platform stop building separate systems, and makes integration and data
  sharing a condition of project approval and acceptance; provincial
  coordination of local platforms.

**Electronic licence standards (verified: published 2018-11-15, effective
2019-01-01, 现行, 归口 国家密码局):**

- **GB/T 36901-2018《电子证照 总体技术架构》**
- **GB/T 36902-2018《电子证照 目录信息规范》**
- **GB/T 36903-2018《电子证照 元数据规范》**
- **GB/T 36904-2018《电子证照 标识规范》**
- **GB/T 36905-2018《电子证照 文件技术要求》**
- **GB/T 36906-2018《电子证照 共享服务接口规范》**

These six are **integration interfaces**, which is exactly what `AGENTS.md`
requires: the licence capability is consumed, never rebuilt.

**Other instruments in scope (designations stated; clause mapping at L2):**

- **GB/T 22239-2019**《网络安全等级保护基本要求》 — graded-protection baseline;
  level three is the typical assumption for this class (`README.md`).
- **《中华人民共和国网络安全法》** (2017-06-01 施行) · **《数据安全法》**
  (2021-09-01 施行) · **《个人信息保护法》** (2021-11-01 施行).

> ⚠️ ASSUMPTION: 等保**三级** is the pack's stated working assumption for this
> platform class, as recorded in `README.md`. It is **not** a citation and no
> grading has been assigned; the actual level is set externally and the
> deployment must use its own.
>
> ⚠️ ASSUMPTION: GB/T 36903/36904 (metadata and identifier specifications)
> bind the e-licence model **only inside the national e-licence service**. A
> platform's own internal 事项 model is not automatically a GB/T 36903 catalogue.
> Whether to align to that standard internally is an L2 decision.