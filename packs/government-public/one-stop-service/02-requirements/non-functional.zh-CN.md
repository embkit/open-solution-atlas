<<<SOURCE>>>
# 02 · 非功能需求

> 可衡量的目标。标记为 `(A)` 的数值目标是政策假设，而非
> 事实——记录这些目标是为了将其固定、论证和变更；其依据见
> [`../SOURCES.md` §4](../SOURCES.md)。
>
> 公式已固定，任何一方据此计算都应得到相同数值。没有公式的目标只是一种期望。
>
> `verification: unverified`——目标属于方案包设计。

## NFR-001 — 防重复提交合规性
- **目标**：100%。不得要求申请人提供任何可共享获取的字段。
- **公式**：`count(forms where every obtainable field is pre-filled or
  verified rather than asked) / count(forms)`。
- **依据**：一项不变量（BR-05）。这是本方案包的决定性约束，而部署若试图通过额外帮助来满足申请，就会在这项约束上失败。

## NFR-002 — 字段分类完整性
- **目标**：100% 的表单字段均标注有共享获取分类。
- **公式**：`count(classified fields) / count(fields)`。
- **依据**：BR-05——分类以**字段**为单位，而非以表单为单位，因此，未分类字段就是一项未经审查的要求。

## NFR-003 — 豁免可审计性
- **目标**：100% 的豁免均记录理由。
- **公式**：`count(exemptions with reason) / count(exemptions)`。
- **依据**：BR-05、FR-014。未记录的豁免会使该规则从合规属性退化为偏好项。

## NFR-004 — 办事指南符合性
- **目标**：100% 的已发布事项均包含全部三项强制办事指南要素和版本号。
- **公式**：`count(items with complete, versioned guide) / count(published items)`。
- **依据**：BR-02、FR-003、FR-004。

## NFR-005 — 办事指南变更可追溯性
- **目标**：100% 的办事指南变更均记录操作人和日期。
- **公式**：`count(attributed guide changes) / count(guide changes)`。

## NFR-006 — 身份认证集成覆盖率
- **目标**：100% 的渠道均通过国家统一身份认证服务进行身份认证；渠道专用凭据为 0 个。
- **公式**：`count(channels using the national service) / count(channels)`。
- **依据**：BR-03、FR-006、FR-007。逐渠道重新认证无异于设置第二套身份体系。

## NFR-007 — 跨部门调用同意核验覆盖率
- **目标**：100% 的调用均针对其用途核验同意。
- **公式**：`count(consent-checked calls) / count(calls)`。
- **依据**：BR-08。没有依据的调用既是合规缺陷，同时又是过度收集的证据。

## NFR-008 — 调用审计完整性
- **目标**：100% 的调用均记录来源机关、字段和用途。
- **公式**：`count(audited calls) / count(calls)`。

## NFR-009 — 限时办结率
- **目标 (A)**：已受理事项中，≥ 99% 在声明的时限内作出决定。
- **公式**：`count(items decided within limit) / count(accepted items)`。
- **依据**：BR-09。从受理开始计量，因为若从提交开始计量，而义务从受理起计算，就会得出规则意在防止的有利结果。

## NFR-010 — 办结时限起点正确性
- **目标**：100% 的计时器均从受理开始，而绝不从提交开始。
- **公式**：`count(clocks started at acceptance) / count(clocks)`。

## NFR-011 — 一次性告知质量
- **目标 (A)**：首次提交中，≥ 95% 无需第二次告知即可通过。
- **公式**：`count(submissions with no follow-up notice) / count(submissions)`。
- **依据**：BR-07、FR-018。此指标衡量的是办事指南是否准确，而非仅仅完整。

## NFR-012 — 补正率
- **目标 (A)**：按事项跟踪；比率过高表明受理环节正在受理办事指南认定不完整的申请。
- **公式**：`count(补正 issued) / count(accepted items)`。

## NFR-013 — 电子印章与电子证照集成
- **目标**：100% 的印章申请均通过国家统一电子印章系统办理；本地生成印章数量为 0。
- **公式**：`count(applications via national system) / count(applications)`。
- **依据**：一项不变量（BR-10）。

## NFR-014 — 电子档案完整性
- **目标**：100% 的已办结办件均以电子方式归档，并经验证确认完整且可检索。
- **公式**：`count(verified electronic archives) / count(completed items)`。
- **依据**：BR-11、FR-028、FR-029——附加到文档管理系统并不等于归档。

## 固定公式

| 数量 | 定义 |
|---|---|
| **可共享获取** | 机构能够通过数据共享获取、因而不得要求申请人提供的字段 |
| **核验而非要求提供** | 该字段已从共享来源预填或核验，而非要求申请人提供 |
| **允许的替代方案** | 共享查询失败时预先定义的回退方案——绝不再次要求申请人提供 |
| **计时起点** | `受理` 时间戳，而非提交时间戳 |
| **一次性告知** | 在受理前一次性、完整地发出 |
| **补正** | 在受理后针对材料缺失或有瑕疵发出 |
| **经验证的电子档案** | 电子文件完整且可检索，而不仅仅是被附加 |

> ⚠️ ASSUMPTION — 每个 `(A)` 目标均属于政策设定。本仓库不主张这些目标源于基准、法规或实际部署。
<<<END>>>