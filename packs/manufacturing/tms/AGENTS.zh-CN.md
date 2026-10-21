# AGENTS.md — TMS（L3）

L3 智能体就绪的方案包。阅读顺序：`00-context/` → `01-business/` →
`02-requirements/` → `03-domain/` → `04-architecture/` → `05-data/` →
`06-contracts/` → `08-quality/acceptance-criteria.md` → `09-delivery/`。
按 `09-delivery/milestones.md` 的里程碑顺序 M0→M7 构建，每次从
`09-delivery/task-map.md` 取一个任务（`T-xx`），并且**不要跳过任何验证
钩子**；一个任务只有在其 AC 全部通过后才算完成。
验证状态：`source-checked`，未经过现场验证——信任
[`SOURCES.md`](./SOURCES.md) 而非记忆；数值目标是假设（`(A)`），要被实测值
替换，绝不当作事实呈现。

承重不变量：

- WMS 拥有仓库执行，TMS 拥有运输执行（规划/派车/结算），ERP 拥有商业订单与
  账务；运输单/运输订单 ID 在三者之间可追溯（ADR-0001、BR-01、FR-020）。
- 计划与实际是明确对账的两个不同状态；实际里程碑仅可追加，计划修订创建新版本
  ——历史绝不被改写（ADR-0005、BR-02、BR-11）。
- 接单冻结费率快照；最终的运费发票是对照该快照的一次已匹配、已审计的配对
  （ADR-0004、BR-04、BR-05）。
- 以 GS1 EPCIS 2.0 / CBV 2.0 词汇发布运输事件（FR-021）。
- 危险品约束是针对带版本法规数据的校验（ADR 2025 / IMDG 2024 / IATA DGR 67 /
  JT/T 617 + GB 6944），绝不是对法律的重新实现；在生效版本未加载时派车被
  拒绝（ADR-0003、BR-07、NFR-010）。
- 任何与环境相关的内容 → `> ⚠️ ASSUMPTION:`；供应商选择只在
  `SOURCES.md` 第 3 节；求解器与车载终端在内核之外（ADR-0002、ADR-0001）。
