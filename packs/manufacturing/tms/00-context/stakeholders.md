# 00 · Stakeholders

| Stakeholder | Interest in the system | Primary touchpoints |
|---|---|---|
| Shipper (货主) logistics manager | Plans moves, chooses carriers, owns cost & service | Order intake, load planning, dispatch |
| Dispatcher / planner | Daily execution: routes, tenders, exceptions | Routing, tendering, exception console |
| Carrier / subcontractor | Accepts tenders, reports milestones, gets paid | Tender/EDI/API, milestone feed, invoice |
| Driver (own fleet) | Executes stops, captures POD | Mobile app / telematics integration |
| Warehouse (WMS) counterpart | Hands off staged goods at dock; receives returns | Load-verified hand-off events, ASN |
| Finance / accounts payable | Pays freight only when audited | Invoice audit, settlement runs, disputes |
| Customer / consignee | Wants ETA and delivery confirmation | EPCIS event sharing, portal |
| Compliance officer (DG, security) | Ensures DG & security rules hold; audit trail | DG validation gates, ISO 28000 controls |
| Fleet/asset manager (own fleet) | Vehicle capacity, eligibility, maintenance windows | Vehicle master, capacity model |
| Carrier scorecard owner | Measures carrier performance | Milestone punctuality, claims rate |

## Notes

- "Carrier" covers both contracted 3PLs and own fleet; own-fleet adds vehicle
  & driver masters but does not change the execution model (ADR-0001 keeps
  telematics hardware out of scope — it is an integration *source*).
- Customer-facing visibility is deliberately event-publication based (EPCIS,
  FR-021) rather than portal-only, so partners integrate on a standard.
