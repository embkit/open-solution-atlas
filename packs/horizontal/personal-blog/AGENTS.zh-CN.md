# AGENTS.md — 个人博客与内容发布（L3）

智能体就绪的方案包。按以下顺序加载；尊重每一条可追溯性关联。

## 加载顺序

1. `manifest.yaml` — 范围、法规环境、成熟度 L3
2. `README.md` — 范围与明确的不在范围（多租户 SaaS、新闻编辑室工作流、
   实时协作**不**要构建）
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `03-domain/glossary.md` — 确切术语；不使用同义词
5. `01-business/` — capability-map → processes → user-journeys → business-rules
6. `02-requirements/` — functional（FR-*）→ non-functional（NFR-*）→
   compliance（CTL-*）
7. `03-domain/` — domain-model → state-machines（SM-01..04）
8. `04-architecture/` — overview + integration/security/observability，然后
   ADR-0001..0004；**这些 ADR 是已定决策——不可翻案**
9. `05-data/` — 逻辑模型、字典、数据流
10. `06-contracts/api-overview.md` 然后 `api/openapi.yaml` — 照它实现
11. `07-experience/key-flows.md` — 交互义务
12. `08-quality/` — acceptance-criteria 是完成的定义；test-strategy 与
    failure-and-dr 约束实现方式
13. `09-delivery/` — 先 milestones 再 task-map（T-01..T-24），按里程碑顺序
    执行并带上验证钩子

## 硬规则

- ID 不可变更：按同样的编号实现 FR/NFR/CTL/AC/T 的引用。
- 静态公开/薄动态边缘（ADR-0001）：绝不给公开渲染路径加上运行时数据库读取；
  提及在构建期渲染。
- Git 是内容 SSOT（ADR-0002）；运行库数据库不持有任何自有内容。
- 默认部署发出零第三方请求（BR-12、CTL-001/002）。
- 任何未知或与环境相关的内容 → `> ⚠️ ASSUMPTION:` + 询问人类；绝不静默
  选定供应商。供应商选择属于 `variants/`。
- 除非明确启用，否则不要实现 M7 的条目；原生评论默认关闭（FR-015）。

## 建议的 SDD 交接（Spec Kit / Kiro / BMAD）

- Specify ← 00/01/02 章
- Plan ← 04/05 + ADR + 09-delivery/sizing-notes
- Tasks ← 09-delivery/task-map（T-id 与任务卡 1:1 对应）
- Acceptance gates ← 08-quality/acceptance-criteria（AC-id），测试策略按每个
  T 的验证钩子
