# 03 · 术语表

> 双语关键术语。标注 **std** 的术语追溯到被引用的标准；其余为本方案包的用法。

| 术语 | 中文 | 定义 |
|---|---|---|
| Transport order | 运输订单 | 由 ERP/WMS 推导出的移动需求；永不超出源需求（BR-01） |
| Shipment | 发运单 | 一条或多条订单行一起移动时的集拼单元 |
| Leg | 运输段 | 一票发运中的一个承运商/运输方式分段；招标、跟踪、结算的单位 |
| Tender | 咨价/发包 | 把一个运输段发包给承运商的出价；结果为 ACCEPTED / REJECTED / TIMEOUT（FR-009） |
| Rate snapshot | 运价快照 | 在接单时冻结的适用费率版本的不可变副本（BR-04） |
| Milestone event | 里程碑事件 | 关于运输段执行情况的仅追加事实（发车、到达、状态……）（BR-11） |
| POD (proof of delivery) | 回单/签收单 | 达到 DELIVERED 前所需的交付证据（BR-06） |
| Three-way match | 三单匹配 | 付款前的订单/招标 ↔ 执行 ↔ 发票审计（BR-05） |
| DG declaration | 危险品申报 | 针对某法规版本校验的 UN 编号/PSN/类别/包装类别/数量（FR-017） |
| Regulation edition | 法规版本 | 为校验而加载的带版本数据表集（ADR/IMDG/IATA DGR/JT/T 617）（NFR-010） |
| EPCIS business step | EPCIS 业务步骤 | **std** CBV 2.0 词汇值，用于对可视化事件分类（如 shipping、receiving） |
| EPCIS disposition | EPCIS 处置 | **std** CBV 2.0 词汇值，用于描述事件结果（如 in_progress、delivered） |
| Incoterms® rule | 贸易术语 | **std** ICC 2020 三字母术语，分配成本/风险/义务（BR-12） |
| Proper shipping name (PSN) | 正式运输名称 | **std** 危险品的受管名称（ADR/JT/T 617/IMDG/IATA DGR） |
| UN number | 联合国编号 | **std** 来自联合国危险品规章体系的四位危险品标识符 |
