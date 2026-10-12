# 02 · Compliance Controls

> Controls traced to instruments. Per this repository's scope decision, legal
> accuracy matters only where it changes what the software must do — so each
> instrument appears as a **designation** with the control it forces. **No clause
> numbers are cited and no currency is tracked.**
>
> `verification: unverified`. Not compliance advice.

## Traceability

| Control | Instrument (designation) | Capability | Rule | Requirement |
|---|---|---|---|---|
| **CTL-01** — Payment scope exclusion | PCI DSS (`pci-dss`) | CAP-03 | BR-10 | FR-007, FR-026 |
| **CTL-02** — Buyer data consent & purpose | PIPL / 《个人信息保护法》 (`pipl`) | CAP-03, CAP-09 | BR-14 | FR-025 |
| **CTL-03** — Price transparency & record retention | 《电子商务法》 (`e-commerce-law`) | CAP-02 | BR-06 | FR-005, FR-028 |
| **CTL-04** — Consumer cancellation & return rights | 《电子商务法》 (`e-commerce-law`) | CAP-07, CAP-08 | BR-09, BR-11 | FR-017, FR-021 |
| **CTL-05** — Data protection over order and customer data | PIPL (`pipl`) | CAP-01, CAP-10 | — | FR-001, FR-028 |
| **CTL-06** — Tariff/destination declaration | not in manifest | CAP-09 | BR-14 | FR-025 |
| **CTL-07** — Audit evidence of money movements | PCI DSS (`pci-dss`), PIPL (`pipl`) | CAP-10 | BR-13 | FR-023, FR-024 |
| **CTL-08** — Evidence that scope claims hold | PCI DSS (`pci-dss`) | CAP-09, CAP-10 | BR-10 | FR-026, NFR-011 |

## Control detail

### CTL-01 — Payment scope exclusion
- **Instrument**: PCI DSS (designation).
- **Forces**: card data must be demonstrably outside the platform's processes.
- **Control**: PSP-hosted fields (FR-007); tokens only; every enabled channel
  carries a current evidence record (NFR-011, FR-026).
- **Why it is here and not in `00-context`**: this control changes *architecture*
  — where card data is allowed to be — and that must be a design decision taken
  once, because a in-scope platform cannot be retrofitted out of scope.

### CTL-02 — Buyer data consent and purpose
- **Instrument**: PIPL (designation).
- **Forces**: consent and purpose-bound use of buyer data, gathered at checkout
  and used at activation.
- **Control**: purpose recorded per order; marketing consent a distinct,
  separately recorded purpose from transaction necessity; consent state enforced
  before any customer data leaves for a campaign or marketplace feed (FR-025).

### CTL-03 — Price transparency and record retention
- **Instrument**: 《电子商务法》 (designation).
- **Forces**: what the customer was shown becomes a record.
- **Control**: the pricing snapshot is retained (FR-028), which the pack already
  requires for capture stability. The transparency obligation is the reason
  retention is **not optional** — a discarded snapshot cannot answer "was this
  really the price?".

### CTL-04 — Consumer cancellation and return rights
- **Instrument**: 《电子商务法》 (designation).
- **Forces**: cancellation and return paths that the customer can exercise.
- **Control**: defined cancellation points (BR-03); per-line fulfilment state so a
  partial return is representable (BR-11); refunds as distinct money operations
  reachable from any cause (FR-021).

### CTL-05 — Data protection over order and customer data
- **Instrument**: PIPL (designation).
- **Forces**: purpose limitation and retention limits over the master data.
- **Control**: retention classes over customer master, order records and
  behavioural data; erasure propagated to derived records.

### CTL-06 — Destination / jurisdiction declaration
- **Instrument**: not in the manifest.
- **Forces**: a cross-border sale creates a declared destination and
  jurisdiction per order.
- **Control**: destination recorded on the order; used by tax and pricing
  resolution rather than inferred.

### CTL-07 — Audit evidence of money movements
- **Instruments**: PCI DSS and PIPL (designations).
- **Forces**: money movements are attributable and retained.
- **Control**: the immutable ledger (FR-023) with operation, key, actor, channel,
  timestamp and derivation reference.

### CTL-08 — Evidence that scope claims hold
- **Instrument**: PCI DSS (designation).
- **Forces**: the exclusion claim must be re-demonstrable as channels are added.
- **Control**: NFR-011 measures evidence completeness across enabled channels;
  FR-026 blocks or exception-records a channel that cannot host fields.

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-007, FR-026 | NFR-011 |
| CTL-02 | FR-025 | — |
| CTL-03 | FR-005, FR-028 | NFR-007 (indirect) |
| CTL-04 | FR-017, FR-021 | NFR-008 |
| CTL-05 | FR-001, FR-028 | — |
| CTL-06 | FR-025 | — |
| CTL-07 | FR-023 | NFR-009 |
| CTL-08 | FR-026 | NFR-011 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed.