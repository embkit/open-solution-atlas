# 01-business / Processes

> Process definitions for the government data sharing & exchange platform. Each
> names its trigger, its steps, and the rules that constrain its steps. Rules live
> in `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. The 国发〔2016〕51号 办法
> supplies the domain's principles and share-type definitions; it does not supply
> these processes.

## P-01 — Register

| | |
|---|---|
| **Trigger** | a provider registers a data resource |
| **Outcome** | a **catalog entry** — the root object |

1. Create the catalog entry linking provider, resource, classification grade and
   share type (BR-01).
2. Record metadata, owner and update obligation (BR-02).
3. A **not-shareable** classification must carry its legal basis (BR-03).

> BR-01: the catalog entry is the root object. Authorization has nothing to
> authorise against without it, and a share that is not in the catalog is invisible
> to the very process that governs it.

## P-02 — Classify

| | |
|---|---|
| **Trigger** | a resource is onboarded or reclassified |
| **Outcome** | a classification grade that **drives** masking and access rules |

1. Assign the classification grade per the national method (BR-04).
2. Derive the masking and access rules from the grade — per class, not per dataset
   (BR-04).
3. A grade change re-derives the rules, never patches them (BR-04).

> BR-04: classification is a policy input, not a label. A grade recorded but not
> enforced is documentation rather than control.

## P-03 — Request

| | |
|---|---|
| **Trigger** | a consumer department requests a resource |
| **Outcome** | a request carrying a **declared purpose** |

1. State the purpose, scope and duration (BR-05).
2. Identify the sharing type of the resource (unconditional / conditional /
   not-shareable).
3. For **unconditional**, proceed without per-consumer negotiation — still
   recorded (BR-06).

## P-04 — Approve

| | |
|---|---|
| **Trigger** | a conditional share request |
| **Outcome** | an **approval**, or a refusal **with a basis** |

1. The provider approves within delegated authority.
2. A refusal records its basis — and where the resource is not-shareable, the
   legal basis is required (BR-03).
3. The approval creates the grant.

## P-05 — Grant

| | |
|---|---|
| **Trigger** | an approval |
| **Outcome** a **recorded, revocable grant** |

1. Create the grant: who, what resource, which purpose, which scope, which
   duration (BR-05).
2. The grant is **revocable by design** (BR-07).
3. **No data transfer exists without a grant** — recorded, not merely permitted
   (BR-08).

> BR-08 is `AGENTS.md`'s closed-loop rule. A transfer without a grant is a
> participation in the loop that cannot be audited, which is to say an
> unaccountable transfer.

## P-06 — Exchange

| | |
|---|---|
| **Trigger** | a granted request is fulfilled |
| **Outcome** | data moved over a channel, with masking applied |

1. Select the channel: table-to-table, file, or interface (BR-09).
2. Apply classification-driven masking before release (BR-04).
3. Record the transfer against the grant (BR-08).

## P-07 — Revoke

| | |
|---|---|
| **Trigger** | a grant expires, a purpose lapses, or an authority revokes |
| **Outcome** | access actually removed, with a measured lead time |

1. Revoke the grant.
2. Remove the consumer's access at the platform.
3. Record the revocation and its completion time (BR-07).

> BR-07: revocation's value is the **lead time** until access is actually removed,
> not the act of recording it. A grant that is revoked but still usable is a
> revocation in name only.

## P-08 — Govern & open

| | |
|---|---|
| **Trigger** | scheduled governance, or an open-data publication |
| **Outcome** | catalog currency maintained; open-data datasets published with DCAT metadata |

1. Review catalog currency against the update obligation (BR-02).
2. Detect staleness and route to the provider (BR-10).
3. For open data, produce the dataset and describe it with **W3C DCAT**
   metadata (BR-11).
4. Reconcile what providers hold against what was delivered (BR-12).

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 catalog entry is the root object | P-01 |
| BR-02 catalog currency | P-01, P-08 |
| BR-03 refusal requires a basis | P-01, P-04 |
| BR-04 classification drives rules | P-02, P-06 |
| BR-05 grant records purpose, scope, duration | P-03, P-05 |
| BR-06 unconditional share needs no negotiation | P-03 |
| BR-07 revocation lead time | P-07 |
| BR-08 no transfer without a grant | P-05, P-06 |
| BR-09 all channels declared | P-06 |
| BR-10 staleness has an owner | P-08 |
| BR-11 open data follows DCAT | P-08 |
| BR-12 two-way reconciliation | P-08 |