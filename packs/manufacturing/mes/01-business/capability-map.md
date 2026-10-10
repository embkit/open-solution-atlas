# 01 · Business Capability Map

```
MANUFACTURING EXECUTION (ISA-95 Level 3)
├── CAP-01 Manufacturing Model 制造模型
│   ├── CAP-01.1 Plant / line / work-center / equipment registry
│   ├── CAP-01.2 Material, BOM & routing (operations), effective-dated
│   └── CAP-01.3 Personnel, skills & shift calendar
│
├── CAP-02 Planning Handoff 计划承接
│   ├── CAP-02.1 Production-order intake (ERP) & work-order derivation
│   ├── CAP-02.2 Dispatch to lines/work centers (finite queues)
│   └── CAP-02.3 Release gating (materials staged, routing valid, no holds)
│
├── CAP-03 Execution & Data Collection 执行与采集
│   ├── CAP-03.1 Station terminal operations (start/pause/complete, quantities)
│   ├── CAP-03.2 Event capture (counts, params, labor, entity links)
│   └── CAP-03.3 Andon exception & escalation
│
├── CAP-04 Material & Genealogy 物料与谱系
│   ├── CAP-04.1 Staging & verification (right material, right lot)
│   ├── CAP-04.2 Consumption recording (actual / backflush variant)
│   ├── CAP-04.3 Lot & serial genealogy (forward / backward)
│   └── CAP-04.4 WIP status & location tracking
│
├── CAP-05 Quality Execution 质量执行
│   ├── CAP-05.1 In-process inspection plans & results
│   ├── CAP-05.2 SPC monitoring & out-of-control alerts
│   ├── CAP-05.3 NCR: quarantine → disposition → release
│   └── CAP-05.4 eDHR / eBR (regulated variant)
│
├── CAP-06 Equipment & OEE 设备与效率
│   ├── CAP-06.1 Equipment state & downtime coding
│   ├── CAP-06.2 OEE computation & analysis (formula-exact, BR-09)
│   └── CAP-06.3 Tooling / mold lifecycle counters
│
└── CAP-07 Visibility & Reporting 可视化与报告
    ├── CAP-07.1 Line boards & shift dashboards
    ├── CAP-07.2 Output / yield / cycle-time reports
    └── CAP-07.3 Traceability dossier export
```

## Capability priorities

| Must (core) | Variant / later (L3+ or variants/) |
|---|---|
| CAP-01, CAP-02, CAP-03, CAP-04, CAP-05.1, CAP-05.3, CAP-06.1, CAP-06.2, CAP-07 | CAP-05.2 SPC depth, CAP-05.4 eDHR/eBR, CAP-06.3 tooling, APS optimization, COA integration |
