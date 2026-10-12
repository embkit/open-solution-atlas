# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs they
> measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **transfer_without_grant** | NFR-001 | **sev-1** — an unaccountable transfer |
| **share_trace_half_closed** | NFR-002 | **sev-1** — a transfer nobody can attribute to a decision |
| **ungranted_read_on_channel** | NFR-001, NFR-011 | **sev-1** — the loop has a hole at a channel |
| **classification_not_enforced_on_path** | NFR-005 | **sev-1** — the control is for one consumer only |
| **not_shareable_without_basis** | CTL-03 | **sev-1** — a control implemented as its easiest part |
| **grant_without_structured_purpose** | NFR-008 | **sev-1** — the obligation cannot be checked |
| **revocation_recorded_access_live** | NFR-003 | **sev-1** — a revocation in name only |
| **catalog_currency_gap** | NFR-006 | sev-2 |
| **staleness_age** | NFR-007 | sev-2 |
| **grant_expiry_not_enforced** | NFR-009 | sev-2 |
| **exchange_latency / failure** | NFR-010 | sev-3 |
| **channel_auditability_variance** | NFR-011 | sev-2 |
| **open_data_undescribed** | NFR-012 | sev-2 |
| **provider_consumer_divergence** | NFR-013 | sev-2 |

## The seven invariants that are never traded

`transfer_without_grant`, `share_trace_half_closed`, `ungranted_read_on_channel`,
`classification_not_enforced_on_path`, `not_shareable_without_basis`,
`grant_without_structured_purpose` and `revocation_recorded_access_live` must be
**zero**.

Seven, and the reason is that this platform is an **accountability system**: it
exists because government departments cannot move each other's data without a
record of who permitted it. Each of these failures is a case where a transfer
occurred and nobody can say who authorised it, on what basis, or whether it was
revoked.

> The seventh is the one that looks like a latency signal and is not. A revocation
> that is recorded while access persists is a control failure whose duration is
> exactly the window in which a revoked consumer still reads — and every one of
> those reads is unattributable.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Who authorised this transfer?" | the share trace, closing to an approval with its basis |
| "Was this consumer permitted for this purpose?" | the grant's structured purpose and its live state |
| "Was access actually removed, and how long did it take?" | the revocation record with its completion time |
| "Was this dataset controlled, or excepted?" | the grade and its derived rules |
| "Did the consumer stay within the declared purpose?" | the purpose-conformance report |
| "Is the catalog current?" | staleness raised against the recorded update obligation |

> Each is answerable from the platform's own record. The purpose-conformance
> question is the one that most often requires the purpose to have been structured
> at grant time — which is why NFR-008 comes before NFR-013 in the measurement
> order.

## Traces and correlation

- A **request** trace spans: request (with structured purpose) → approval (with
  basis, or refusal with basis) → grant → transfer (channel, masking applied) →
  share trace closing to the catalogue entry.
- A **revocation** trace spans: revocation recorded → access removal per channel →
  completion timestamp, so the lead time is a measurement rather than an
  assumption.
- A **governance** trace spans: staleness raised → provider routed → resolved, or
  reconciliation run → gap → provider routed.

## Alerting policy

- **Page** on any invariant breach, and on a grant-expiry job failure.
- **Ticket** on catalog currency gaps, staleness age, channel auditability
  variance and provider/consumer divergence.
- **Review** two trends weekly because their *direction* means more than their
  value: catalog currency falling means the update obligation is not being
  operationalised, and the duty can no longer be demonstrated; and unenforced-path
  findings rising means a new consumer surface has appeared that the
  classification policy does not reach — which is the normal way a control
  decays rather than being removed.