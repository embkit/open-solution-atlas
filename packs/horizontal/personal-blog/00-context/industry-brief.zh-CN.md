# 00 · 行业简报 — 个人内容发布

## 这套系统服务的业务

一位独立创作者在自己的域名上发布长文，并对其保有持久的所有权。这是*内容
发布*家族中最小的一员；它更大的亲戚是无头 CMS、新闻编辑室平台，以及多租户
SaaS 博客托管（这些都不在本方案包范围内）。

商业模式通常是间接的：博客支撑作者的名声、咨询、产品或招聘——它本身并不是
一个交易系统。

## 价值链

```
author ──writes──▶ draft ──review/publish──▶ public page ──distribution──▶ reader
                                          │                    ├─ search
                                          │                    ├─ RSS reader
                                          │                    ├─ social/webmention
                                          │                    └─ inbound link
                                          └──◀── feedback: comments / mentions / analytics
```

## 塑造设计的市场现实

1. **平台风险是首要风险。** 只在第三方平台发布的作者会面临账号锁定、算法变更
   与链接失效。因此自有 URL + 完整导出是一项核心能力，而不是加分项。
2. **流量尖峰明显而总量偏低。** 每月访问量从数百到低万，偶尔因外部链接出现
   尖峰。峰值吞吐要求微不足道；成本底线与持久性更重要。
3. **作者通常是唯一的运营者。** 没有值班团队。系统必须能经受数月的无人照看
   仍然安全：不可变的公开产物、最小的服务器暴露面、自动化的 TLS。
4. **IndieWeb / POSSE 模型**（Publish on Own Site, Syndicate Elsewhere）是
   已确立的开放实践：内容以自有站点为正本，转载时附上链接到外部网络，通过
   Webmention 接收回复。
5. **持久的写作格式。** 以纯文件承载的 Markdown 比一代 CMS 数据库活得更久。
   内容必须在没有发布软件的情况下依然可读。

## 典型部署场景

| 场景 | 变体说明 |
|---|---|
| 静态托管 + CDN（全球） | 默认目标；成本最低、攻击面最小 |
| 带反向代理的源站 | 作者希望完全自托管时 |
| 中国大陆托管 | 需要 ICP 备案；分析与评论服务需相应选择——见 `variants/`（计划中） |

## 来源

- IndieWeb wiki — <https://indieweb.org/>（POSSE、Webmention、Micropub）
- W3C Webmention Recommendation — <https://www.w3.org/TR/webmention/>
- W3C ActivityPub — <https://www.w3.org/TR/activitypub/>
