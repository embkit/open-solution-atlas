# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| Warehouse operator / 3PL (仓储运营方) | Runs the facility, labor, equipment | Owns/operates WMS |
| Goods owner / 货主 (in 3PL) | Owns stock; defines SOPs, strategies, SLA | Configured as owner; receives stock reports/bills |
| Procurement / suppliers (供应商) | Deliver against PO; provide ASN | ASN/EDI source |
| Customers / consignees (收货方) | Receive shipments | ASN/label/EDI recipient |
| Carrier / 3PL transport (承运商) | Transport, manifests, tracking | Label/manifest/track integration |
| QC / quality organization | Accept/reject incoming, release holds | Drives quarantine & disposition |
| Finance / inventory control | Reconcile physical vs. ledger, approve adjustments | Consumes adjustment/report events |
| Production planning (manufacturing) | Requests material staging, reports FG | Integration with MES/ERP |
| IT / automation engineering | Operates WCS/WES/devices, interfaces | Equipment boundary owner |
| Regulators / auditors | GMP, customs, food/cold-chain audits | Read-only evidence/e-records |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Warehouse manager | 仓储经理 | layout, strategy config, KPIs, approve adjustments, override limits |
| Shift supervisor / 班组长 | 主管 | wave release, task reassignment, exception handling, counts approval |
| Inbound operator / receiver | 收货员 | dock, receive, count, label, QC-pending handoff |
| Putaway operator | 上架员 | execute putaway tasks, confirm bin/lot |
| Picker | 拣货员 | execute pick tasks, scan verify, short-pick report |
| Packer | 复核包装员 | pack verification, cartonization, label, VAS |
| Shipping / loader | 发货/装车员 | load, seal, manifest, ship confirm |
| Inventory controller | 库存管理员 | holds, cycle counts, adjustment requests/approvals |
| QC inspector | 质检 | accept/reject, disposition, lot release |
| Forklift/AGV operator | 叉车/设备操作员 | move/transport tasks; automation monitoring |
| Owner portal user (3PL) | 货主门户用户 | view own stock/orders, reports (RLS by owner) |
| System integration / admin | 系统管理员/接口 | master data, interfaces, users, audit config |
| Automation system (WCS/WES) | 设备控制系统 | non-human actor: receives tasks, reports events |

## 3. External / upstream-downstream systems as actors

- **ERP**: PO, STO, sales orders, material/valuation master; consumes goods
  receipt/issue and adjustment events.
- **OMS/e-commerce**: order source, cutoffs, promises.
- **MES (manufacturing)**: staging requests, material consumption, FG receipt
  (boundary aligned with the `mes` pack — see open question on staging truth).
- **TMS/carrier platforms**: tender, manifests, parcel labels, tracking.
- **WCS/WES, AS-RS, conveyor/sorter, AGV/AMR, scales, printers, RFID gates**.
- **Yard management / dock door scheduling** (may be module or external).

## 4. Actor goals (top)

- Picker: minimal walking, unambiguous task, no "stock missing at bin".
- Supervisor: keep waves meeting carrier cutoff; absorb exceptions fast.
- Inventory controller: zero unexplained variance; every adjustment has a
  reason, approver, and audit trail.
- Goods owner: accurate, owner-isolated visibility and proof of handling.
- Manager: throughput per labor-hour, space utilization, accuracy targets.
