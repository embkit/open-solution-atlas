# 03-domain / 术语表

规范术语。以英文为主；中文为对应译名。在标识符、正文和契约中统一使用。

| 术语（英） | 中文 | 定义 |
|---|---|---|
| WMS | 仓储管理系统 | 管理仓库实物搬运及实物库存真实状态的执行系统 |
| WCS | 仓储控制系统 | 设备控制层（输送机/AS-RS）；接收 WMS 任务 |
| WES | 仓储执行系统 | WMS 与 WCS 之间的编排层，通常具备作业优化功能 |
| DC | 配送中心 | 配送中心 |
| SKU | 最小存货单位 | 库存管理单位 |
| GTIN | 全球贸易项目代码 | GS1 贸易项目标识符 |
| SSCC | 系列货运包装箱代码 | GS1 系列货运包装箱代码；物流单元的托盘/容器标签 |
| GLN | 全球位置码 | GS1 参与方/位置标识符 |
| License plate (LP) | 托盘/容器标签 | 装卸单元上可供扫描的唯一标识符（通常为 SSCC） |
| Handling unit (HU) | 装卸/物流单元 | 作为一个整体移动的托盘/纸箱/周转箱；递归层级 |
| Lot / batch | 批次 | 同次生产/同一物料分组；批次属性包括有效期 |
| Serial | 序列号 | 单元级唯一身份标识 |
| FEFO / FIFO / LIFO | 先到期先出/先进先出/后进先出 | 批次流向策略（BR-06） |
| ASN | 预先发货通知 | 预先发货通知（EDI 856 / DESADV） |
| Putaway | 上架 | 将已收货货物移至存储位置 |
| Pick face | 拣货面/拣货位 | 从中拣选单元的前置位置 |
| Reserve | 存储区/备用区 | 为拣货面补货的散货存储区域 |
| Replenishment | 补货 | 存储区 → 拣货面 |
| Allocation | 分配 | 将库存分配给需求 |
| Soft / hard reservation | 软/硬预留 | 可转换的计划预留/已承诺的预留（BR-05） |
| Wave | 波次 | 一并发布的成组订单批次 |
| Pick method | 拣货方式 | 单件/批次/分区/集群拣货 |
| Interleaving | 任务交错 | 组合拣货和上架任务，以减少行走距离 |
| Pack verification | 复核 | 在打包环节基于扫描的订单验证 |
| Cartonization | 装箱计算 | 算法化纸箱选择 |
| Manifest | 装车/发运清单 | 载具/拖车上的发货/包裹清单 |
| Goods receipt / issue | 收货 / 发货过账 | 过账至 ERP 的实物收货/发货事件 |
| Cycle count | 循环盘点 | 按 ABC 定期执行的局部盘点 |
| ABC classification | ABC 分类 | 决定盘点频率的速度/价值类别 |
| Variance / adjustment | 差异 / 调整 | 盘点值与账面值的差异及其更正 |
| Hold / quarantine / freeze | 冻结/待检/隔离 | 不可分配库存状态 |
| Disposition | 处置 | 放行/退回/返工/报废决定 |
| On-hand / available | 现有量 / 可用量 | 总量 / 可分配量（BR-01） |
| In-transit intra | 库内在途 | 在未结任务中于货位之间移动的数量 |
| Owner (货主) | 货主 | 持有库存的参与方；3PL 中的隔离范围 |
| 3PL | 第三方物流 | 第三方物流；多货主仓储 |
| VAS | 增值服务 | 贴标/组装/礼品等 |
| Returns / RMA | 退货/逆向物流 | 逆向物流 |
| Yard / dock | 园区/月台 | 拖车园区和装卸月台门 |
| EPCIS | — | GS1 事件标准（Object/Aggregation/Transaction 事件） |
| AS-RS | 自动化立体库 | 自动化存储/取货系统 |
| AGV / AMR | 自动导引车/自主移动机器人 | 自动导引/自主移动机器人 |
| PTL / pick-to-voice | 电子标签拣货/语音拣货 | 设备辅助拣货 |
| Bonded warehouse | 保税仓 | 海关监管仓库（变体） |
| Cold chain | 冷链 | 温控物流（变体） |
| RLS | 行级安全 | 实施货主隔离的行级安全 |
| SoD | 职责分离 | 职责分离 |