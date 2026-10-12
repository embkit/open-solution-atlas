# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. Payment data: the scope boundary is architectural (CTL-01)

Card data exists in exactly one place: the PSP's hosted fields.

- The platform never receives a primary account number (PAN) — not on checkout,
  not from a channel adapter, not from a marketplace feed that reports one.
- The platform stores **tokens** only.
- Every channel that takes payment must present hosted fields; a channel that
  cannot is blocked or carries an explicit exception (FR-026).
- The evidence of the claim (that no core component can receive a PAN) is
  **maintained and re-demonstrated per channel** (NFR-011, CTL-08).

> A scope exclusion is a claim about the *system*, and every new channel is a
> new counter-example waiting to happen. That is why evidence completeness is a
> measured NFR rather than a one-time assertion.

## 2. Identity and access

| Concern | Control |
|---|---|
| **Customer identity** | resolved by the identity provider; the platform stores a reference, not credentials |
| **Staff authority** | role-based; **money-authority is separated** from fulfilment and service-view roles (FR-027) |
| **Break-glass** | permitted for refunds above threshold by an authorised approver, with the action recorded and the record reviewed |
| **Channel identity** | an adapter presents the channel's identity model, mapped to the platform's customer reference |

## 3. Data protection (CTL-02, CTL-05)

- **Purpose separation**: transaction necessity and marketing are separate,
  separately recorded purposes. Consent state is enforced before any customer
  data leaves for a campaign or marketplace feed.
- **Retention classes**: customer master, order records, pricing snapshots,
  ledger entries and behavioural data each carry a declared retention period.
- **Erasure propagation**: an erasure request reaches derived records —
  snapshots referencing the customer, care cases and behavioural traces.

> ⚠️ ASSUMPTION — the tension between retaining snapshots and ledger entries
  (needed to reproduce and defend money) and erasure obligations is real and
> is **not** resolved here. The mechanism is a per-class retention policy with a
> declared regeneration window; the window is a business decision.

## 4. Inventory and pricing integrity

- Availability is assigned in exactly one place (Inventory). A second assignor
  is an oversell.
- Pricing snapshots are append-only and immutable (BR-06, NFR-004). A mutable
  snapshot destroys the ability to defend a charge.
- Ledger entries are append-only; a correction is a new entry (BR-13).

## 5. Fraud and risk

- Risk is evaluated **at checkout, before authorisation** (I-09).
- The failure mode is **fail-closed**: an unavailable risk service blocks capture
  rather than bypassing, because a bypass converts the control into decoration.

## 6. Secrets and keys

- PSP credentials are held by the payment service and not exposed to any other
  component.
- Idempotency keys are platform-issued records, not secrets, and are retained
  for the audit window.

## 7. Audit evidence (CTL-07)

Every money movement and every inventory consumption is attributable: actor,
channel, timestamp, idempotency key, and the snapshot or reading it derived from.
This is what makes a dispute resolvable and an audit passable, and it is the
reason the ledger is a separate append-only store rather than a report.