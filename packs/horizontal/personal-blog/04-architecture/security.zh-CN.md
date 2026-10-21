# 04 · 安全

## 信任边界与威胁模型

值得保护的资产，按优先级排序：
1. 作者身份 / 发布权利（涂改风险）
2. 读者安全（经由提及/评论的 XSS；隐私）
3. 内容持久性（写作的完整性/可用性）
4. 运行凭据

| 威胁 | 缓解措施 |
|---|---|
| 账号被接管 → 恶意发布 | 通过 OAuth/OIDC 走可信 IdP（或强口令 + TOTP MFA）、短期令牌、会话吊销；单一身份；管理界面托管在独立的 `/admin` 源上，并可选 IP 白名单 |
| Webmention/评论带来的存储型 XSS | 接入时用服务端白名单清洗器；只渲染已通过的 HTML；`rel="nofollow noopener ugc"`；公开页面的 CSP 禁止内联脚本 |
| 经 Webmention 来源抓取发起的 SSRF | 出站白名单；封禁 RFC1918/链路本地/元数据 IP（169.254.169.254）；DNS 重绑定防护；响应上限 2 MB；抓取时不带 Cookie/凭据 |
| 垃圾信息洪泛 | 按 IP 与按来源的速率限制、自适应节流、默认审核、评论表单可选的工作量证明/蜜罐 |
| 媒体上传滥用 | 需要身份认证；类型白名单 + 魔数嗅探；体积上限；content-disposition 隔离；用户媒体从无 Cookie 的独立资源源站提供 |
| 构建环节的供应链 | 锁文件固定版本；CVE 扫描失败即构建失败（NFR-007）；制品签名/不可变；构建器除写入范围的存储令牌外没有任何生产凭据 |
| 内容篡改 | Release 以 Git 提交哈希为键；指针晋升是唯一的变更动作；审计日志（CTL-010）；仓库本身已签名/受保护分支保护 |
| TLS 配置不当 | HSTS 预加载、仅启用现代 TLS、目标 A+；证书自动续期并带到期告警 |
| 读者痕迹被枚举/抓取 | 没有读者账号；IP 留存 ≤ 24 小时；分析为聚合；隐私页由清单生成 |

## 安全响应头（公开页面）

```
Content-Security-Policy: default-src 'self'; img-src 'self' https:; style-src 'self';
                         script-src 'self'; frame-ancestors 'none'; base-uri 'none'
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```
（确切策略受版本控制；第三方脚本只在该追踪清单存在对应条目时才存在 ——
CTL-002。）

## 备份与机密

- 机密绝不入内容仓库；在运行时注入。
- 数据库快照加密；每月演练恢复（见 failure-and-dr.md）。
