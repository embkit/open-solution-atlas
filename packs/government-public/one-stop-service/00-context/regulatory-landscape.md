# 00-context / Regulatory Landscape

> Obligations are stated at the level a builder can act on, each with its
> engineering consequence, quoting the instrument. Where a mapping is unverified
> it is marked rather than asserted — per the pack standard §5.
> `verification: unverified`; this is **not** compliance advice.

## 1. Instruments in scope

| Instrument | Jurisdiction | What it governs here |
|---|---|---|
| **《国务院关于在线政务服务的若干规定》** (国务院令第716号) | CN | The platform's founding obligation: what must be online, what must be published, what must not be asked twice, and the legal effect of electronic seals, licences and archives |
| **《国务院关于加快推进政务服务标准化规范化便利化的指导意见》** (国发〔2022〕5号) | CN | Mandatory integration; no parallel system building; integration as a project approval/acceptance condition |
| **GB/T 36901–36906-2018 电子证照六项国家标准** | CN | E-licence architecture, catalogue, metadata, identifier, file format and sharing interface — the **integration contract** |
| **GB/T 22239-2019《网络安全等级保护基本要求》** | CN | Graded-protection baseline for the platform itself |
| **《中华人民共和国网络安全法》** (2017-06-01 施行) | CN | Network operator duties; personal information in logs and sessions |
| **《中华人民共和国数据安全法》** (2021-09-01 施行) | CN | Data classification grading; risk management |
| **《中华人民共和国个人信息保护法》** (2021-11-01 施行) | CN | Lawful basis, minimisation, consent, deletion — across every cross-department call |

## 2. What 国务院令第716号 actually requires

The regulation is short and unusually concrete. Its operative provisions, and
what each one demands of a platform.

### 第四条 — 事项 must be on the platform

> 除法律、法规另有规定或者涉及国家秘密等情形外，政务服务事项应当按照国务院
> 确定的步骤，纳入一体化在线平台办理。政务服务事项包括**行政权力事项**和
> **公共服务事项**。

> Engineering consequence: the platform's catalogue root has **two top-level
> kinds** (行政权力事项 — where an administrative power is exercised and a
> 决定 is issued — and 公共服务事项 — a service). They have different legal
> shapes: only the first produces a 决定书 with review/appeal rights. A single
> undifferentiated "matter" type would model them wrongly.
>
> Note also the two carve-outs (law otherwise provides; state secrets). They
> are the platform's legitimate boundary cases and must be representable.

### 第五条 — one authentication

> 国家政务服务平台基于自然人身份信息、法人单位信息等资源，建设**全国统一
> 身份认证系统**…实现**一次认证、全网通办**。

> Engineering consequence: the platform **integrates** the national unified
> authentication service and holds no competing citizen identity (`AGENTS.md`:
> dependencies are never re-implemented). Re-implementing citizen identity would
> duplicate a national service and create a second identity to reconcile.

### 第六条 — the published 办事指南

> 政务服务机构应当按照规范化、标准化要求编制**办事指南**，明确政务服务事项的
> **受理条件、办事材料、办理流程**等信息。办事指南应当在政务服务平台**公布**。

> Engineering consequence: these three are **mandatory structural elements** of
> a 事项, not optional documentation:
> - 受理条件 — the acceptance predicate, and therefore the material list can be
>   *derived* from it rather than hand-maintained;
> - 办事材料 — the material checklist, with its data-sharing status;
> - 办理流程 — the approval lifecycle and its steps.
>
> Because it is **published**, the guide is the public contract. The platform
> must version it, and an applicant relying on a superseded guide is a legal
> problem, not a UX problem.

### 第七条 — the anti-double-submission rule

> 行政相对人在线办理政务服务事项，应当提交真实、有效的办事材料；**政务服务
> 机构通过数据共享能够获得的信息，不得要求行政相对人另行提供。**

> Engineering consequence — the platform's defining technical constraint:
> - every form field must be classified as **obtainable by sharing** or not;
> - a field obtainable by sharing must **not** be a required input, and is
>   instead pre-filled or used as verification;
> - the exemption must be **auditable**: for a given 事项 and date, one must be
>   able to show which materials were *not* demanded and why.
>
> This is why the `data-exchange` pack is a dependency rather than a nice-to-have,
> and why a shared-data lookup failing must **degrade** (fall back to a permitted
> alternative) rather than silently re-asking the applicant.

### 第九条 / 第十条 / 第十一条 — electronic artefacts carry legal effect

> **第九条** 国家建立权威、规范、可信的**统一电子印章系统**…**电子印章与实物
> 印章具有同等法律效力**，加盖电子印章的电子材料合法有效。
>
> **第十条** 国家建立**电子证照共享服务系统**，实现电子证照跨地区、跨部门共享
> 和全国范围内互信互认…电子证照**采用标准版式文档格式**。**电子证照与纸质
> 证照具有同等法律效力**。
>
> **第十一条** 除法律、行政法规另有规定外，电子证照和加盖电子印章的电子
> 材料**可以作为办理政务服务事项的依据**。

> Engineering consequence: the platform is an **integrator** of two national
> services — the unified seal system and the e-licence sharing service — and
> consumes them through the GB/T 369xx interfaces. It does not mint seals, and it
> does not define its own licence format. 第九条/第十条 give an e-licence the
> status of a *primary* basis for proceeding, which is why "scan the paper
> licence" workflows are a regression rather than a fallback.

### 第十二条 — electronic archiving

> 政务服务机构应当对履行职责过程中形成的**电子文件**进行规范管理，按照档案
> 管理要求**及时以电子形式归档**并向档案部门移交。除法律、行政法规另有规定
> 外，电子文件**不再以纸质形式归档和移交**。符合档案管理要求的**电子档案与
> 纸质档案具有同等法律效力**。

> Engineering consequence: archival is an **electronic** obligation and the
> platform's case record is the archival object. The application data model,
> not the department's filing system, is therefore the record of truth for the
> process. Retention, format integrity and transfer to the archives authority
> are first-class capabilities, not an afterthought.

### 第十五条 — the definitions the platform must not reinterpret

> 电子签名 / 电子印章（基于可信密码技术生成身份标识，以电子数据图形表现的印章）/
> 电子证照（由计算机等电子设备形成、传输和存储的证件、执照等电子文件）/
> 电子档案（具有凭证、查考和保存价值并归档保存的电子文件）。

> Engineering consequence: these four terms carry statutory force in this
> domain. Using them loosely in a product UI or data model creates a
> mis-description of a legally defined artefact. The glossary uses them exactly.

## 3. Integration, not duplication (国发〔2022〕5号)

The guidance states that departments able to rely on the national integrated
platform **不再单独建设相关业务系统**, and that systems which must still be built
must make **integration and data sharing a condition of project approval and
acceptance**; local platforms should be coordinated at provincial level.

> Engineering consequence: the platform's design must assume coexistence with
> departmental systems, and must expose stable published interfaces — because
> that is what other projects will be required to integrate against. An
> interface designed only for today's callers will not survive the acceptance
> conditions of tomorrow's projects.

## 4. The e-licence standards are an interface contract

GB/T 36901–36906-2018 (published 2018-11-15, effective 2019-01-01, 现行,
归口 国家密码局) define the e-licence system: architecture, catalogue
information, metadata, identifier, file technical requirements, and the sharing
service interface.

> Engineering consequence: GB/T **36906 共享服务接口规范** is the integration
> point the platform calls; **36905 文件技术要求** constrains the artefact it
> stores. `AGENTS.md` requires these to be consumed, never re-implemented.

> ⚠️ ASSUMPTION: **the platform's internal 事项 catalogue is not automatically
> a GB/T 36902/36903 catalogue.** Those standards describe the *electronic
> licence* catalogue; a service-item catalogue is a different object. Whether the
> platform aligns its internal model to that structure is an L2 decision and is
> deliberately not settled here.

## 5. Personal information across every call

PIPL governs the applicant's data. `AGENTS.md` requires that **every
cross-department data call carries consent and audit** — and PIPL makes that a
legal duty rather than good practice.

> Engineering consequence: the shared-data verifier must, per call, record the
> lawful basis/consent, the source authority, the fields returned and the
> purpose. A call without a recorded basis is both a compliance defect and, under
> 第七条, evidence that the platform is over-collecting.

## 6. Graded protection

GB/T 22239-2019 sets the platform's baseline controls; the level is assigned
externally.

> ⚠️ ASSUMPTION: `README.md` records 等保**三级** as the typical baseline for this
> platform class. That is a working assumption, **not** a citation and not an
> assigned grading. The deployment must use the level actually assigned to it,
> and this pack maps no specific control clauses.

## 7. What would make this pack `source-checked`

1. Confirm 国令第716号 article text against the 司法部 国家行政法规库 entry
   (retrieved and quoted here; re-verify before a compliance argument).
2. Retrieve and cite GB/T 36901–36906 clause-level requirements, not just titles.
3. Retrieve the **统一电子印章** technical standard. 国务院令第716号 第九条
   mandates a national unified seal system but names no standard number, and
   this pack deliberately names none either. Which specification the platform
   must comply with has to be established — guessing it is exactly the error
   the standard's "cite or qualify" rule forbids.
4. Map the assigned 等保 level to GB/T 22239-2019 control clauses.
5. Confirm whether sector-specific rules (不动产登记、社保、医保) override the
   generic lifecycle terms used here.

Until those close, `verification` stays `unverified`.