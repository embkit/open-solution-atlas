# 05 · 数据字典（核心字段）

## 文章元数据

| 字段 | 类型 | 约束 | 含义 |
|---|---|---|---|
| post_id | uuid | 主键 | 内部稳定 id |
| slug | string | `^[a-z0-9]+(-[a-z0-9]+)*$`，≤ 80，唯一 | URL 组件；发布后不可变（BR-04） |
| title | string | 1–150 字符 | 显示标题 |
| summary | string | ≤ 300 字符 | 订阅源/卡片/meta 描述的来源 |
| status | 枚举 | DRAFT/SCHEDULED/PUBLISHED/UNPUBLISHED | SM-01 |
| published_at | timestamptz | 草稿为 null；≤ now 时闸控可见性（BR-07） | 订阅源/排序键 |
| canonical_url | url | 唯一，https | 订阅源的 GUID 来源（BR-08） |
| license_id | 枚举/引用 | 发布时必填 | 每篇文章的许可（CTL-005） |
| repo_path | path | 在仓库中存在 | 指向 SSOT 的链接 |
| og_image_ref | media_id? | 推荐正方形 ≥1200px | 社交卡片 |

## media_asset

| 字段 | 类型 | 约束 |
|---|---|---|
| sha256 | hex(64) | 去重键 |
| content_type | 枚举 | image/png、image/jpeg、image/webp、image/gif、image/svg+xml（仅限经清洗的 SVG） |
| bytes | int | ≤ 5,242,880（FR-003） |
| alt_text | string? | 除非 decorative=true 否则必填（BR-10） |
| width,height | int | 由检查填充 |

## mention

| 字段 | 类型 | 约束 |
|---|---|---|
| source_url | url | http(s)，长度 ≤ 2048 |
| target_post_id | 外键 | 接入时必须存在（FR-013） |
| type | 枚举 | REPLY/LIKE/REPOST/BOOKMARK/MENTION |
| status | 枚举 | PENDING/APPROVED/REJECTED/BLOCKED |
| content_safe | html | 仅清洗器输出；原始来源在作业生命周期之外绝不存储 |
| uk(source_url,target_post_id) | 唯一 | BR-009 |

## redirect

| 字段 | 约束 |
|---|---|
| from_path | 根相对路径，唯一；不得等于某个已存在的存活路径 |
| to_url | 301 时必填；410 时忽略 |
| kind | 301（已移动/已合并）/ 410（已移除） |

## release

| 字段 | 约束 |
|---|---|
| commit_sha | 被构建的确切内容树 |
| status | BUILDING/READY/DEPLOYED/FAILED（SM-02） |
| artifact_prefix | 不可变的存储位置 |

## 时间戳

所有时间均为 UTC；渲染时转换为作者指定的显示时区，且仅用于定时发布界面。
`published_at` 是唯一的公开排序键；`updated_at` 触发 `atom:updated` 但不改变
GUID。
