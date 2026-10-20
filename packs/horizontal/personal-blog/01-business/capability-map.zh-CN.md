# 01 · 业务能力地图

一级能力及其二级分解。能力 ID（`CAP-xx`）是功能需求回溯的锚点。

```
PERSONAL PUBLISHING 个人发布
├── CAP-01 Authoring 创作
│   ├── CAP-01.1 Markdown 编辑与实时预览
│   ├── CAP-01.2 草稿自动保存与修订历史
│   ├── CAP-01.3 媒体库（上传、替代文本、来源）
│   └── CAP-01.4 元数据编辑（标题、slug、标签、摘要、许可）
│
├── CAP-02 Organization 组织
│   ├── CAP-02.1 分类体系（标签 / 分类 / 系列）
│   ├── CAP-02.2 归档（按日期、标签、分类的索引页）
│   └── CAP-02.3 面向已发布内容的站内检索
│
├── CAP-03 Publishing 发布
│   ├── CAP-03.1 发布 / 取消发布流程
│   ├── CAP-03.2 定时发布
│   ├── CAP-03.3 正本 URL 与重定向管理
│   └── CAP-03.4 静态构建与 CDN 分发
│
├── CAP-04 Distribution 分发
│   ├── CAP-04.1 RSS/Atom 订阅源
│   ├── CAP-04.2 站点地图与 SEO 元数据（OG/Twitter/JSON-LD）
│   ├── CAP-04.3 POSSE 联合发布链接（手工/可选）
│   └── CAP-04.4 邮件/-newsletter 桥接（可选，经由订阅源）
│
├── CAP-05 Interaction 互动
│   ├── CAP-05.1 Webmention 接收与验证
│   ├── CAP-05.2 审核队列（通过 / 拒绝 / 拉黑）
│   └── CAP-05.3 原生评论表单（可选，需审核）
│
├── CAP-06 Insight 洞察
│   ├── CAP-06.1 保护隐私的页面分析
│   └── CAP-06.2 订阅者 / 引荐来源的粗粒度可见性
│
└── CAP-07 Ownership 主权保障
    ├── CAP-07.1 完整内容导出（Markdown + 媒体 + 元数据）
    ├── CAP-07.2 备份 / 恢复
    └── CAP-07.3 便于迁移的结构（无专有格式）
```

## 能力优先级

| 必须有（MVP） | 应该有 | 可以有 |
|---|---|---|
| CAP-01、CAP-02（标签/归档）、CAP-03、CAP-04.1、CAP-04.2、CAP-05.1/05.2、CAP-06.1、CAP-07 | CAP-02.3 检索、CAP-03.2 定时发布、CAP-05.3 原生评论 | CAP-04.3 POSSE 自动化、CAP-04.4 newsletter 桥接 |
