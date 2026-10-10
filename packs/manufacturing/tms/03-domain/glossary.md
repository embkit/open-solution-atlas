# 03 · Glossary

> Bilingual key terms. Terms marked **std** trace to a cited standard;
> others are pack usage.

| Term | 中文 | Definition |
|---|---|---|
| Transport order | 运输订单 | Demand for movement derived from ERP/WMS; never exceeds source demand (BR-01) |
| Shipment | 发运单 | Consolidation unit of one or more order lines moving together |
| Leg | 运输段 | One carrier/mode segment of a shipment; unit of tender, tracking, settlement |
| Tender | 咨价/发包 | Offer of a leg to a carrier; outcomes ACCEPTED / REJECTED / TIMEOUT (FR-009) |
| Rate snapshot | 运价快照 | Immutable copy of the applicable rate version frozen at tender acceptance (BR-04) |
| Milestone event | 里程碑事件 | Append-only fact about leg execution (departure, arrival, status…) (BR-11) |
| POD (proof of delivery) | 回单/签收单 | Evidence of delivery required before DELIVERED (BR-06) |
| Three-way match | 三单匹配 | Order/tender ↔ execution ↔ invoice audit before payment (BR-05) |
| DG declaration | 危险品申报 | UN number/PSN/class/packing group/qty validated against a regulation edition (FR-017) |
| Regulation edition | 法规版本 | Versioned data table set (ADR/IMDG/IATA DGR/JT/T 617) loaded for validation (NFR-010) |
| EPCIS business step | EPCIS 业务步骤 | **std** CBV 2.0 vocabulary value classifying a visibility event (e.g. shipping, receiving) |
| EPCIS disposition | EPCIS 处置 | **std** CBV 2.0 vocabulary value describing event outcome (e.g. in_progress, delivered) |
| Incoterms® rule | 贸易术语 | **std** ICC 2020 three-letter term allocating cost/risk/obligations (BR-12) |
| Proper shipping name (PSN) | 正式运输名称 | **std** Regulated name of a dangerous good (ADR/JT/T 617/IMDG/IATA DGR) |
| UN number | 联合国编号 | **std** Four-digit dangerous-goods identifier from the UN Model Regulations family |
