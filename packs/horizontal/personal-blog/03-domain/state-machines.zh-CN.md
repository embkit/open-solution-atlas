# 03 · 状态机

## SM-01 文章生命周期

```
                 ┌─────────┐
   create ──────▶│  DRAFT  │◀──────────────┐
                 └────┬────┘               │
          edit/autosave│              restore revision
                 ┌─────▼──────┐      (creates new revision)
                 │ SCHEDULED  │
                 └─────┬──────┘
            publish now│ scheduler fires (FR-009)
                 ┌─────▼──────┐  unpublish   ┌────────────┐
                 │ PUBLISHED  │─────────────▶│  UNPUBLISHED│
                 └─────┬──────┘              └──────┬──────┘
        edit published │ creates revision+rebuild   │ republish
                       └──────────────▶ republished  │
                                                 ◀──┘
```

守卫规则：
- DRAFT/SCHEDULED → PUBLISHED：元数据完整（FR-004）+ 替代文本（FR-003）+
  构建成功。
- PUBLISHED → UNPUBLISHED：发出一个 Release，在该 URL 上返回 410。
- UNPUBLISHED → PUBLISHED：同一 URL 重新生效（除非作者创建重定向，否则不
  产生新 slug）。
- 任何迁移都不得产生订阅源/索引与页面互相矛盾的状态（发布原子性，NFR-015）。

## SM-02 Release 生命周期

```
BUILDING ──build+tests ok──▶ READY ──deploy ok──▶ DEPLOYED (immutable)
   │                          │
   └──failure──▶ FAILED       └──deploy fail──▶ FAILED ──retry──▶ BUILDING
```
- FAILED 绝不取代当前已 DEPLOYED 的 release；读者继续看到上一个完整站点。
- 每个 Release 记录内容树哈希；部署因此可复现。

## SM-03 提及生命周期

```
incoming HTTP ──syntactic/SSRF checks fail──▶ REJECTED (4xx, nothing stored)
      │ pass
      ▼
  PENDING (stored, 202)
      │ fetch source + verify link-back fails ──▶ REJECTED
      │ pass (typed)
      ▼
  VERIFIED-PENDING-MODERATION
      ├── author approve ──▶ APPROVED  (rendered, sanitized)
      ├── author reject  ──▶ REJECTED
      └── author block source ──▶ BLOCKED (future sends auto-rejected)
```
对既有 `(source,target)` 的再次投递会就地更新记录（BR-09），并且只有在已验证
内容发生变化时才重置审核状态。

## SM-04 修订追加日志

`revision n` —(edit/save)→ `revision n+1`（绝不更新/移除既有修订）。
「恢复」= 用较旧的快照创建 revision n+2。
