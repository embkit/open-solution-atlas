# 02 · 非功能需求

> 可度量的目标。**以 `(A)` 标记的数值目标是策略性假设，而非事实**——记录这些目标，是为了锁定其取值、进行论证并作出变更；其依据见 [`../SOURCES.md` §4](../SOURCES.md)。
>
> 公式均已固定，以便任何一方都能复现相同数值。没有公式的目标只是一种愿望。
>
> `verification: unverified`——这些目标属于方案包设计。

## NFR-001 — 计费事件不可变性
- **目标**：100%。任何已生成的计费事件均不得更新或删除。
- **公式**：`count(charge events modified after emission) = 0`。
- **依据**：这是一项正确性不变量（BR-09），而非服务等级。绝不为吞吐量而牺牲。

## NFR-002 — 可追溯性完整性
- **目标 (A)**：≥ 99.5% 的资源订单可从其客户订单追溯到，反向追溯亦然。
- **公式**：`count(resolvable links both ways) / count(resource orders)`。

## NFR-003 — 双向对账覆盖率
- **目标 (A)**：在账期内，≥ 99% 的计费事件与订单完成对账，且 ≥ 98% 与库存使用完成对账。
- **公式**：每一侧均为 `count(reconciled on side X) / count(charge events)`。
- **依据**：两个方向会发现不同的缺陷；合并为单一数字会掩盖失效的是哪一侧。

## NFR-004 — 泄漏检测时延
- **目标 (A)**：自账期结束起 24 h 内，≥ 99% 的“无主使用”和“无费激活”发现项被提出。
- **公式**：已提出发现项的 p99 为 `now - cycle_close_ts`。

## NFR-005 — 发票可重算性
- **目标**：100%。任何发票均可依据其事件和规则版本重现。
- **公式**：`count(invoices regenerated identically) / count(attempted)`。
- **依据**：这正是 BR-11 的核心目的；如果不再能够重算，每项争议都将无法解决。

## NFR-006 — 账期准时性
- **目标 (A)**：≥ 99% 的账期在预定窗口内结束。
- **公式**：`count(cycles closed on time) / count(cycles)`。

## NFR-007 — 跨账期规则变更正确性
- **目标**：0 个账期在生效日期处被错误拆分。
- **公式**：`count(cycles where a period was computed under the wrong rule
  version) = 0`。
- **依据**：BR-08 将这种拆分设为一项需评估的属性；错误拆分会让该账期中每位客户的金额在无人察觉的情况下出错。

## NFR-008 — 调整处理周期
- **目标 (A)**：从提出异常到应用经批准的调整，p95 ≤ 48 h。
- **公式**：p95 为 `adjustment_applied_ts - exception_raised_ts`。
- **依据**：审批工作流是一项财务控制；如果审批速度赶不上操作人员面临的压力，它就会被绕过——而这正是该控制措施旨在防止的失效模式。

## NFR-009 — 护栏合规性
- **目标**：在护栏失败的情况下执行断连的次数为 0。
- **公式**：`count(disconnections with a guardrail failure) = 0`。
- **依据**：这是一项不变量（BR-15），绝不作权衡取舍。

## NFR-010 — 95598 上下文可用性
- **目标 (A)**：在受理案件时呈现账户、计量表、读数历史、支付状态和相关中断的 p95 ≤ 2 s。
- **公式**：p95 为 `context_presented_ts - case_created_ts`。
- **依据**：BR-06；一旦发生转接，这条规则就会形同虚设。

## NFR-011 — 接口可用性
- **目标 (A)**：已声明的 BSS/OSS 接口按月衡量的可用性 ≥ 99.9%。
- **公式**：`1 - (interface downtime) / (period)`。
- **依据**：该接口是双方共同依赖的衔接点；不得将 OSS 侧的降级归因于 BSS 套件，反之亦然。

## NFR-012 — 保留期证据完整性
- **目标**：每个保留类别均声明保留期，并具有可审计的处置记录。
- **公式**：`count(classes with declared period and disposal record) /
  count(declared classes)`。

## 固定公式

| 量化项 | 定义 |
|---|---|
| **按生效日期计费** | `sum over periods of (usage in period × rate of the rule version effective in that period)` |
| **可重算发票** | `f(charge events, rule versions per event, adjustment events)`——具有确定性且可重现 |
| **可归属于订单的计费** | 计费事件链接到资源订单，资源订单链接到业务订单，业务订单链接到 CO |
| **无主使用** | 库存消耗的 RO 链无法解析至带账户的 CO |
| **无费激活** | 资源激活的 RO 链解析至 CO，但不存在计费事件 |
| **跨生效日期的账期拆分** | 按生效日期划分各期间；每个期间均使用当时生效的版本计算 |

> ⚠️ ASSUMPTION — 每个 `(A)` 目标都是策略性设定。本仓库不主张这些目标来自基准、法规或部署。