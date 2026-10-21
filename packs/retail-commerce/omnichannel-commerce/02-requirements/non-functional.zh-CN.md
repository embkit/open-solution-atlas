# 02 · 非功能需求

> 可度量的目标。**标记为 `(A)` 的数值目标属于策略性假设，而非
> 事实**——在此记录这些目标，以便对其进行明确设定、讨论和变更，
> 其依据见 [`../SOURCES.md` §4](../SOURCES.md)。
>
> 公式均已固定，以便任何一方进行测量时都能得出相同数值。没有
> 公式的目标只是一种愿景。
>
> `verification: unverified` — 这些目标属于方案包设计。

## NFR-001 — 超卖率
- **目标 (A)**：测量窗口内，没有超卖触达客户。
- **公式**：`count(orders where consumed quantity exceeded available at consume time) / count(orders consuming inventory)`.
- **依据**：`AGENTS.md` 将超卖列为头号大忌，因此目标定为零；该测量是防线，而不是可以牺牲的指标。

## NFR-002 — 可用库存准确性
- **目标 (A)**：在每次日度盘点时，系统可用库存与实物可用库存的差异在容差范围内的最小存货单位-渠道-来源组合占比 ≥ 99%。
- **公式**：`1 - count(mismatches beyond tolerance) / count(combinations counted)`.

## NFR-003 — 预留过期准时性
- **目标 (A)**：所有即将到期的预留中，在到期后 60 秒内释放的比例 ≥ 99.9%（p99）。
- **公式**：在所有已释放预留中，`release_ts - expiry_ts` 的 p99。
- **依据**：BR-02 将过期设为结构性要求；本指标衡量该结构性属性能否在负载下实际成立。

## NFR-004 — 价格快照完整性
- **目标**：100%。任何快照在创建后均不得被修改。
- **公式**：`count(snapshots modified after creation) = 0`.
- **依据**：这是正确性不变量，而非服务级别。参见 BR-06。

## NFR-005 — 资金操作幂等性
- **目标**：100%。重试使用同一键时，不得产生重复的资金影响。
- **公式**：`count(duplicate money effects sharing an idempotency key) = 0`.
- **依据**：这同样是一项不变量（BR-07），之所以持续测量，是因为这种故障在客户遭到重复扣款之前并不可见。

## NFR-006 — 结算延迟
- **目标 (A)**：请款路径的 p95 ≤ 800 ms、p99 ≤ 2 s，不含 PSP 响应时间；按渠道测量。
- **依据**：PSP 对尾部延迟起主导作用；平台目标衡量的是平台能够控制的部分。

## NFR-007 — 订单承诺偏差
- **目标 (A)**：最终扣款总额与请款时价格快照总额一致的订单占比 ≥ 99%。
- **公式**：`count(orders with charged total == snapshot total) / count(orders)`.
- **依据**：衡量快照保证是否在整个售后路径中始终成立。

## NFR-008 — 退款周期时长
- **目标 (A)**：退款从授权到资金流转完成的 p95 ≤ 24 h。
- **公式**：`refund_completed_ts - return_authorised_ts` 的 p95。

## NFR-009 — 对账差异存续时长
- **目标 (A)**：对账差异存续时长的 p95 ≤ 48 h；不得存在存续超过 7 天且未指定升级处理负责人的差异。
- **公式**：`now - gap_opened_ts` 的 p95，另加存续超过 7 天且无负责人的差异数量。

## NFR-010 — 跨渠道订单可见性延迟
- **目标 (A)**：从订单状态变更到其余所有渠道可见的延迟 p95 ≤ 5 s。
- **依据**：BR-14 将各渠道定义为变体；渠道分叉最初表现为可见性延迟，并最终成为永久性延迟。

## NFR-011 — 支付合规范围证据完整性
- **目标**：每个已启用渠道都有当前有效且有证据支撑的支付合规范围判定。
- **公式**：`count(channels with current evidence) / count(enabled channels)`.
- **依据**：BR-10 要求提供证明；本指标衡量每个渠道是否都具备该证明。

## NFR-012 — 渠道接入周期时长
- **目标 (A)**：从声明渠道到启用该渠道的周期 ≤ 5 个工作日，不计外部 PSP/第三方平台的前置周期。
- **依据**：本方案包将渠道视为变体；如果接入成本接近渠道分叉级别，则说明实践中违反了 BR-14。

## 固定公式（共享）

| 量化项 | 定义 |
|---|---|
| **可用库存** | `physical - held_reservations - in_flight_commitments`，按最小存货单位-渠道-来源计算 |
| **快照总额** | `sum(line_total) - sum(line_discount_contribution) + tax(line_total)` |
| **订单派生状态** | `fold over per-line fulfilment states`——绝不使用独立的订单级标志 |
| **幂等范围** | 平台签发的键；相同键 + 相同载荷 ⇒ 相同结果，不产生新的影响 |
| **差异存续时长** | `now - gap_opened_ts`，其中 `gap_opened_ts` 表示首次计算出差异的时间 |

> ⚠️ ASSUMPTION — 每个 `(A)` 目标均属于策略。仓库并不声称
> 这些目标来自基准、法规或实际部署。