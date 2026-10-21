# 03 · 术语表

在每一章中都使用这些确切术语；同义词仅为帮助翻译而列出，绝不引入第二个术语。

| 术语（英） | 中文 | 定义 |
|---|---|---|
| Post | 文章 | 核心的可发布单元；有一个正本 URL 与一条生命周期（SM-01） |
| Draft | 草稿 | 尚未 PUBLISHED 的文章；绝不出现在任何公开制品中（BR-14） |
| Revision | 修订版本 | 文章的 Markdown + 元数据的仅追加不可变快照 |
| Slug | 短标识 | 文章的 URL 路径组件；kebab-case、唯一、发布后不可变 |
| MediaAsset | 媒体资产 | 上传的二进制文件（图片），带替代文本或装饰性标记 |
| Tag / Category / Series | 标签/分类/系列 | 分类体系：多对多标签；可选的单一分类；有序系列 |
| Release | 发布版本 | 原子的构建+部署单元；读者任一时刻只看到一个 Release |
| Redirect | 重定向规则 | 301（已移动/已合并）或 410（已移除）记录，守护旧的文章 URL |
| Mention | 提及 | 指向某篇文章的、已验证的 Webmention；展示前需经审核 |
| Webmention | — | W3C 协议：一个站点通知另一个站点它链接到了对方 |
| POSSE | 自有先行再分发 | Publish (on) Own Site, Syndicate Elsewhere |
| Canonical URL | 规范链接 | 文章唯一权威的 URL |
| Feed | 订阅源 | 列出最新文章的 RSS 2.0 / Atom 1.0 XML |
| SearchIndex | 搜索索引 | 仅覆盖已发布文章的客户端静态索引 |
| Release atomicity | 发布原子性 | 读者看到的是上一个完整站点或新的完整站点，绝不是混合体 |
| Scheduling tolerance | 定时容差 | `publishedAt` 与实际发布之间允许的延迟（≤ 60 秒） |
| ExportBundle | 导出包 | 全部自有内容的单一开放格式归档（FR-017） |
| Audit log | 审计日志 | 作者/审核动作的仅追加记录（CTL-010） |

## 约定

- 状态名使用与状态机中完全一致的大写枚举标记。
- 界面文案中的「删除」对已发布文章意味着生命周期动作 UNPUBLISH；硬删除
  只对草稿存在。
- 「读者」始终指未经认证的公开访客；不存在读者账号概念。
