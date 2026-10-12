# ADR-0008 — Electronic archiving is a correctness requirement on the platform's model, not a downstream process

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires the platform to retain and archive. The 办法's 第十二条 makes it
an obligation with a specific shape:

> 对履行职责过程中形成的**电子文件**进行规范管理，按照档案管理要求**及时以电子形式
> 归档**并向档案部门移交。除法律、行政法规另有规定外，电子文件**不再以纸质形式归档和
> 移交**。符合档案管理要求的**电子档案与纸质档案具有同等法律效力**。

Three consequences follow, and the second is the one that gets missed.

- Archiving is **electronic**, and paper is no longer the record.
- The **platform's data model** is therefore the archival object — not the
  department's filing system, and not a document management system the files are
  attached to.
- The archive's legal effect is the same as paper, which means completeness and
  retrievability are correctness requirements rather than housekeeping.

## Options considered

1. **Paper retained as the record, with electronic copies** — familiar, and it
   contradicts 第十二条's default. It also means the platform's record is a scan.
2. **Electronic files attached to a document management system, and that counts as
   archiving** — the common implementation. The DMS becomes the record, the
   platform's model becomes a source, and completeness is never verified.
3. **The electronic file is archived, and the archive is verified complete and
   retrievable** — the platform's model is the archival object, and verification is
   a step with a pass condition.

## Decision

Option 3, enforced by BR-11, FR-028, FR-029, and NFR-014, with model constraint 12
and the failure-mode contract making an archive failure a **recorded** condition
rather than a silent one.

The verification is the load-bearing part. An archive marked on the basis of an
attachment is an assertion, and an assertion is what art. 12's "同等法律效力" cannot
rest on.

## Consequences

- Positive: the archive is defensible, because completeness and retrievability are
  verified properties rather than assumptions, and the platform's model is the
  object that carries the record.
- Positive: the "no longer in paper form" default is structural, so a deployment
  cannot quietly retain a paper workflow as the real record.
- Negative: the platform's application data model becomes an archival object, which
> constrains it: a field the model omits is a record that will not exist, and a
> migration that drops one is an archival gap rather than a schema change.