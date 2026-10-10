# 03-domain / Glossary

Canonical terms. English primary; 中文 equivalents. Use these uniformly in
IDs/prose/contracts.

| Term | 中文 | Definition |
|---|---|---|
| WMS | 仓储管理系统 | execution system managing physical warehouse movements and physical stock truth |
| WCS | 仓储控制系统 | equipment control layer (conveyor/AS-RS); receives WMS tasks |
| WES | 仓储执行系统 | orchestration layer between WMS and WCS, often with work optimization |
| DC | 配送中心 | distribution center |
| SKU | 最小存货单位 | stock keeping unit |
| GTIN | 全球贸易项目代码 | GS1 trade item identifier |
| SSCC | 系列货运包装箱代码 | GS1 Serial Shipping Container Code; license plate of a logistic unit |
| GLN | 全球位置码 | GS1 party/location identifier |
| License plate (LP) | 托盘/容器标签 | unique scannable ID on a handling unit (often SSCC) |
| Handling unit (HU) | 装卸/物流单元 | pallet/carton/tote moved as one; recursive hierarchy |
| Lot / batch | 批次 | same-production/material grouping; lot attrs incl. expiry |
| Serial | 序列号 | unique unit-level identity |
| FEFO / FIFO / LIFO | 先到期先出/先进先出/后进先出 | lot direction strategies (BR-06) |
| ASN | 预先发货通知 | advance shipping notice (EDI 856 / DESADV) |
| Putaway | 上架 | move received goods to a storage location |
| Pick face | 拣货面/拣货位 | forward location from which units are picked |
| Reserve | 存储区/备用区 | bulk storage replenishing pick face |
| Replenishment | 补货 | move reserve → pick face |
| Allocation | 分配 | assign stock to demand |
| Soft / hard reservation | 软/硬预留 | convertible plan reserve / committed reserve (BR-05) |
| Wave | 波次 | grouped batch of orders released together |
| Pick method | 拣货方式 | single / batch / zone / cluster picking |
| Interleaving | 任务交错 | combining pick and putaway tasks to cut travel |
| Pack verification | 复核 | scan-based order verification at packing |
| Cartonization | 装箱计算 | algorithmic carton selection |
| Manifest | 装车/发运清单 | list of shipments/parcels on a load/trailer |
| Goods receipt / issue | 收货 / 发货过账 | physical GR/GI events posted to ERP |
| Cycle count | 循环盘点 | recurring partial counts by ABC |
| ABC classification | ABC 分类 | velocity/value classes driving count frequency |
| Variance / adjustment | 差异 / 调整 | count vs. book difference and its correction |
| Hold / quarantine / freeze | 冻结/待检/隔离 | non-allocatable stock states |
| Disposition | 处置 | release/return/rework/scrap decision |
| On-hand / available | 现有量 / 可用量 | total qty / allocatable qty (BR-01) |
| In-transit intra | 库内在途 | qty moving between bins on an open task |
| Owner (货主) | 货主 | stock-owning party; isolation scope in 3PL |
| 3PL | 第三方物流 | third-party logistics; multi-owner warehousing |
| VAS | 增值服务 | labeling/kitting/gift etc. |
| Returns / RMA | 退货/逆向物流 | reverse logistics |
| Yard / dock | 园区/月台 | trailer yard and loading dock doors |
| EPCIS | — | GS1 event standard (Object/Aggregation/Transaction events) |
| AS-RS | 自动化立体库 | automated storage/retrieval system |
| AGV / AMR | 自动导引车/自主移动机器人 | automated guided/autonomous mobile robots |
| PTL / pick-to-voice | 电子标签拣货/语音拣货 | device-assisted picking |
| Bonded warehouse | 保税仓 | customs-supervised warehouse (variant) |
| Cold chain | 冷链 | temperature-controlled logistics (variant) |
| RLS | 行级安全 | row-level security enforcing owner isolation |
| SoD | 职责分离 | segregation of duties |
