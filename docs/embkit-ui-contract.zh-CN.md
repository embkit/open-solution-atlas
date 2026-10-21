# EmbKit UI 契约——仓库内参考副本

> **本文件并非由我们维护，不应编辑。** 它是 EmbKit
> 权威客户端 UI 规格的逐字副本；将其纳入仓库，是为了让本目录
> 能够采用相同主题，而无需依赖跨仓库路径。
>
> - 上游：`EmbKit/docs/客户端UI规格-参考归纳星.md`
> - 上游 sha256（前 16 位）：`7e3189ed5f73373c`
> - 纳入日期：2026-10-13
>
> 当 EmbKit 的副本发生变化时，应重新纳入此文件并重新运行
> `tests/test_design_tokens.py`；该测试会断言契约中
> 可通过机械方式检查的部分。
>
> **此处的 LOCKED 项不容协商。** `--primary` 为 indigo
> `#4F46E5`，其色相不得更改；中性色依规则必须偏冷——
> "不要引入暖灰，会和 indigo 打架"。本目录是产品的橱窗，
> 因而承载的是产品自身的识别特征，而不是本目录自身的识别特征。

---

# EmbKit 客户端 UI 规格（1:1 参考「归纳星」）

> 来源：两张参考图（文件保险箱 / 文档首页）。
> 决策：**布局、字体、图标、间距、圆角、阴影、组件形态 —— 1:1 照搬**；
> **主色统一到现有 indigo 品牌**（不跟参考图的纯蓝 `#2563EB`）。
> 本文档是后续改造的**唯一契约**，改造时以本文档为准，不自由发挥。
> 最后更新：2026-10-12

---

## 0. 先看清现状（差距在哪）

| 维度 | 现状（`apps/base/src/shell/styles.css`） | 目标（参考图） | 差距 |
|---|---|---|---|
| 主色 | `--purple: #635bff`（Stripe 紫） | indigo `#4F46E5` | **换** |
| 辅助色 | `--cyan: #00d4ff` | 仅用于「分类图标」之一 | 降级为分类色 |
| 中性色 | `--navy #0a2540` / `--page #f6f9fc` / `--line #e3e8ee` | 近乎一致 | **基本不用动** ✅ |
| 字体 | `Inter + PingFang SC` | 完全一致 | **已经对了** ✅ |
| 圆角 | `--r-lg 8px` / `--r-xl 12px` | 6/8/10/12/14/999 | 补齐中间档 |
| 阴影 | 紫调 `rgba(10,37,64,·)` | 冷蓝调、更大模糊半径 | 微调 |
| 侧栏宽 | `190px` | ~220px | **加宽** |
| 图标 | **手写 SVG 34 处**（`App.tsx` 123KB） | Lucide 线性图标，统一 2px 描边 | **重做** ⚠️ |
| 组件库 | 无 Tailwind / 无 shadcn / 无 Radix | — | 保持，纯 CSS |

**两个必须先说的风险：**

1. **`App.tsx` 是 123KB 单体**。1:1 重做要碰几乎全部 UI，全塞在一个文件里改，
   一次改崩就很难回退。**建议改造时同步按视图拆组件**，至少拆成
   `Sidebar` / `ShopView` / `MyToolsView` / `AccountView` / `SettingsView` / `DiagnosticsView`。
2. **引入 `lucide-react` 是一个新依赖**。但参考图的观感**有一半来自图标风格统一**，
   手写 34 个 SVG 无法做到笔画粗细/端点/圆角一致。**建议引入**——
   若坚持零依赖，则必须手写一套统一规范的 SVG（描边 2px、`stroke-linecap:round`、24 viewBox）。

---

## 1. 色彩系统

### 1.1 品牌色（LOCKED — 不得改色相）

| 令牌 | 值 | 用途 |
|---|---|---|
| `--primary` | `#4F46E5` | **唯一主行动色**：CTA、链接、激活态、选中态、焦点环 |
| `--primary-hover` | `#4338CA` | 主按钮悬停 |
| `--primary-active` | `#3730A3` | 主按钮按下 |
| `--primary-soft` | `#6366F1` | 渐变起点（仅品牌面板/安装器用） |
| `--primary-to` | `#8B5CF6` | 渐变终点（仅品牌面板/安装器用） |
| `--primary-tint` | `#EEF2FF` | 图标底、激活态浅底、选中行底 |
| `--primary-ring` | `rgba(79,70,229,.28)` | 焦点环 |

> 官网 `--accent: #4f46e5`、安装器 `#6366F1→#8B5CF6`、客户端 `#635bff` —— **三个紫统一成这一组**。
> 安装器渐变保留 `#6366F1→#8B5CF6`（它已经做完了，且只用于品牌时刻）。

### 1.2 中性色（参考图与现状几乎一致，**保留现值**）

| 令牌 | 值 | 用途 |
|---|---|---|
| `--page` | `#f6f9fc` | 主内容区背景（比侧栏略深，形成左右分层） |
| `--surface` | `#ffffff` | 卡片、侧栏 |
| `--surface-2` | `#f6f9fc` | 次级表面、悬停底色 |
| `--surface-3` | `#eef2f7` | 侧栏悬停、分隔区块 |
| `--line` | `#e8edf3` | 卡片描边、输入框边（比现值 `#e3e8ee` 再浅一档） |
| `--line-strong` | `#d3dae3` | 需要强调的分隔 |
| `--text` | `#0a2540` | 主文字（近黑，带蓝调） |
| `--text-2` | `#425466` | 次文字 |
| `--text-3` | `#8792a2` | 辅助/路径/说明 |

> ⚠️ 中性色**统一偏冷**（蓝调灰）。不要引入暖灰，会和 indigo 打架。

### 1.3 语义色（保留现值）

`--ok #0e7c5a` / `--warn #a5670a` / `--danger #c2373c`，各配 `-soft` 浅底。
**卸载等危险操作用 `--danger`，不要用主色**，否则和主行动抢注意力。

### 1.4 分类色板（参考图的核心视觉，**必须 1:1 保留**）

参考图 8 张分类卡各配一个彩色图标 + 同色系浅底。这是整套 UI 里唯一的多彩区域，
**没有它整个界面会变成一片灰白**。

| 分类 | 主色 | 浅底 | Lucide 图标 |
|---|---|---|---|
| 图片 | `#0EA5E9` | `#E0F2FE` | `image` |
| 视频 | `#EF4444` | `#FEE2E2` | `video` |
| 文档 | `#22C55E` | `#DCFCE7` | `file-text` |
| 软件安装包 | `#F97316` | `#FFEDD5` | `package` |
| 压缩包 | `#A855F7` | `#F3E8FF` | `archive` |
| 设计文件 | `#D946EF` | `#FAE8FF` | `pen-tool` |
| 音频 | `#6366F1` | `#E0E7FF` | `audio-waveform` |
| 其他 | `#94A3B8` | `#F1F5F9` | `folder` |

**映射到 EmbKit 的插件分类**（按插件领域配色，顺序不变）：

| 分类 | 图标 | 主色 |
|---|---|---|
| 格式转换 | `refresh-cw` | `#0EA5E9` |
| 文件预览 | `eye` | `#22C55E` |
| 思维导图 | `git-branch` | `#A855F7` |
| PDF | `file-type` | `#EF4444` |
| 音视频 | `audio-waveform` | `#6366F1` |
| 压缩解压 | `archive` | `#F97316` |
| 效率工具 | `wrench` | `#D946EF` |
| 其他 | `folder` | `#94A3B8` |

**规则**：分类色**只允许**出现在图标底和图标描边上，**不得**用于按钮、文字、卡片背景。

---

## 2. 字体排版

### 2.1 字体栈

参考图用的是 **PingFang SC + SF Pro/Inter 系**。我们客户端**已经在用 Inter + PingFang SC**，
但本项目**只发 Windows**，Windows 上没有 PingFang 也没有 SF Mono，需要补 Windows 侧：

```css
--sans: "Inter", "MiSans", "HarmonyOS Sans SC", "PingFang SC",
        "Microsoft YaHei", -apple-system, "Segoe UI", sans-serif;
--mono: ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace;
```

> 中文推荐 **MiSans** 或 **HarmonyOS Sans SC**（均免费商用，字形最接近 PingFang），
> 与 Inter 混排最自然。系统兜底 `Microsoft YaHei`。
> 拉丁字母/数字一律使用 Inter（参考图的 `AES-256-GCM`、数字 `6 3 9 3` 明显采用中性 grotesque 字体）。

### 2.2 字阶（参考图实测反推）

| 令牌 | 字号/字重/行高/字距 | 用途（参考图对应） |
|---|---|---|
| `--fs-display` | 26px / 700 / 1.3 / **-0.02em** | 页面大标题「文档」「文件保险箱」 |
| `--fs-h1` | 20px / 600 / 1.35 / -0.015em | 卡内主标题「保险箱已锁定」 |
| `--fs-h2` | 16px / 600 / 1.4 / -0.01em | 卡内次标题「没有待整理的文件」 |
| `--fs-h3` | 14px / 600 / 1.45 / 0 | 分区标题「分类与目标文件夹」 |
| `--fs-body` | **13px** / 400 / **1.6** / 0 | 正文、按钮文字 |
| `--fs-sm` | 12px / 400 / 1.55 / 0 | 说明、描述 |
| `--fs-xs` | 11px / 500 / 1.5 / 0 | 路径、脚注、角标 |
| `--fs-num` | 22px / 700 / 1.1 / **-0.02em** | 分类卡右上角数字 |

**排版硬规则**（参考图一致遵循，容易被忽略）：

- 标题一律 `letter-spacing` 负值，越大的字负得越多。
- 正文行长 ≤ 80 字符，行高 1.6。
- 单个组件内**不超过 2 个字重**。
- 数字用 `font-variant-numeric: tabular-nums`（分类卡数字对齐、避免跳动）。
- 营销标题 44px / 700 / `-0.025em`；副标题 18px / 400 / `--text-2`。

---

## 3. 图标系统

### 3.1 规范

| 项 | 值 |
|---|---|
| 字体库 | **Lucide**（`lucide-react`） |
| 描边宽 | `stroke-width: 2`（Lucide 默认，**不要用 1.5**，参考图更实） |
| 端点/拐角 | `round` / `round`（默认） |
| 视口 | `24×24` viewBox |
| 尺寸档 | 导航 18px｜按钮 15px｜行内 16px｜分类卡 17px｜空态大图标 40px |
| 颜色 | 默认 `--text-3`；激活/主行动 `currentColor`（继承父级）；分类图标用 1.4 表主色 |

### 3.2 导航图标映射（参考图 → EmbKit）

| 参考图 | Lucide | EmbKit 对应 |
|---|---|---|
| 首页 | `layout-grid` | 工具商店 `store` 或 `layout-grid` |
| 整理规则 | `sliders-horizontal` | 我的工具 `package` |
| 清理 | `wand-sparkles` | 账号中心 `circle-user-round` |
| 批量命名 | `pen-line` | 设置 `settings` |
| 文件保险箱 | `lock` | 诊断 `stethoscope` |
| 记录 | `history` | — |
| 专业版 | `crown` | — |
| 设置 | `settings` | 设置 `settings` |

### 3.3 其他常用图标

`folder` `folder-open` `folder-plus` `refresh-cw` `shield-check` `lock` `key-round`
`zap` `mail` `search` `chevron-right` `arrow-right` `plus` `more-horizontal`
`toggle-left` `toggle-right` `trash-2` `download` `check` `alert-circle` `sparkles`

---

## 4. 布局骨架

### 4.1 窗口

```
┌─ titlebar (40px, 自定义，含 Windows 窗口按钮) ─────────────┐
│                                                              │
│  ┌─────────┬──────────────────────────────────────┐        │
│  │ Sidebar │  main                                 │        │
│  │  220px  │  header: title + actions(右对齐)      │        │
│  │         │  ─────────────────────────────────   │        │
│  │ logo    │  content (可滚动)                     │        │
│  │ nav     │   · banner card                       │        │
│  │  spacer)│   · section header                    │        │
│  │ footer  │   · setting rows                      │        │
│  └─────────┴──────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 侧栏（220px，三段式）

| 段 | 内容 | 规格 |
|---|---|---|
| **头部** | Logo 圆角方块（36px，圆角半径 10px，白底主色描边或主色实底 + 白色图标）+ 产品名 15px/700 + 副标 11px/`--text-3` | 内边距 `16px 14px` |
| **导航** | 5 项，纵向间距 `2px`，每项高 `36px` | 内边距 `6px 10px` |
| **弹性区** | `flex:1` 把底部推下去 | — |
| **底部** | ① 状态提示卡（浅底 `--surface-3`，圆角半径 10px，内含 `zap` 图标 + 标题 12px/600 + 副标 11px/`--text-3`）<br>② 两行脚注（`shield-check` + 文案；`mail` + 账号），11px/`--text-3` | 内边距 `12px 14px` |

**侧栏背景 `--surface`（白），主区背景 `--page`（浅灰蓝）—— 这个明暗差是参考图左右分层的关键，别做成同色。**

### 4.3 主区

- 内边距：`24px 28px`
- 页眉：标题 + 路径行 + 状态行在左，动作按钮组**右对齐**（同一行按基线对齐）
- 内容区：纵向间距 `20px`
- 分区标题行：标题左、次要链接右（如「管理规则 ›」，主色 12.5px）
- **居中表单类内容**：卡片 `max-width: 460px`，水平居中，垂直居中偏上

---

## 5. 间距与栅格

```css
--sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px;  --sp-4: 16px;
--sp-5: 20px; --sp-6: 24px; --sp-7: 28px;  --sp-8: 32px;
```

| 场景 | 值 |
|---|---|
| 卡片内边距（大卡） | 20–24px |
| 卡片内边距（小卡，如分类卡） | 14px |
| 卡片之间 / 分区间距 | 20px |
| **组间间距必须 > 组内间距** | 20px 对比 8–12px |
| 网格列间距 | 12px |
| 分类卡网格 | **4 列**（≤1100px 降 3 列，≤820px 降 2 列） |
| 正文与容器边缘 | ≥ 16px |

> 硬规则：**禁止出现 7px / 13px / 21px 这类游离值**，一律归入间距刻度（scale）。

---

## 6. 圆角与阴影

```css
--r-sm: 6px;    /* 角标、标签、小型标签块 */
--r-md: 8px;    /* 按钮、输入框、导航项 */
--r-lg: 10px;   /* 分类卡、图标容器、底部提示卡 */
--r-xl: 12px;   /* 常规卡片 */
--r-2xl: 14px;  /* 居中大卡、弹层 */
--r-full: 999px;/* 药丸 */
```

> **同心圆角**：外层圆角 = 内层圆角 + 内边距。参考图里嵌套元素从不共用同一圆角。

```css
--shadow-card: 0 1px 2px rgba(15,23,42,.04), 0 8px 24px rgba(15,23,42,.06);
--shadow-card-hover: 0 2px 4px rgba(15,23,42,.05), 0 14px 34px rgba(15,23,42,.09);
--shadow-pop: 0 12px 32px rgba(15,23,42,.12);   /* 下拉菜单、Toast */
--shadow-modal: 0 20px 50px rgba(15,23,42,.16);
```

> 阴影**偏冷蓝调**（`rgba(15,23,42,·)`），不要纯黑 `rgba(0,0,0,.1)`——参考图的阴影是带蓝色调的。
> 现有值 `rgba(10,37,64,·)` 也可以，两者差别很小，统一用一个即可。

---

## 7. 组件形态（1:1 参考图）

### 7.1 导航项
```
高度 36px｜圆角 8px｜内边距 0 10px｜图标 18 + 间距 10 + 文字 13.5px/500
默认：  图标 --text-3｜文字 --text-2
悬停：  背景 --surface-3
激活：  背景 --primary｜文字与图标 --surface（白）｜无阴影
```

### 7.2 按钮
```
主按钮：  背景 --primary｜文字 白｜高度 34px｜水平内边距 px 16｜圆角 8｜13.5px/600｜图标 15 位于文字前，间距 6
          悬停 --primary-hover｜激活 --primary-active｜焦点环 2px --primary-ring
次按钮：  背景 --surface｜边框 1px --line｜文字 --text｜其余同上｜悬停背景 --surface-2
文字按钮：背景 透明｜文字 --primary｜悬停背景 --primary-tint
危险按钮：背景 --danger｜白色文字｜仅用于卸载/重置
```

### 7.3 卡片
```
背景 --surface｜圆角 12｜边框 1px --line 或 --shadow-card｜内边距 20–24
悬停（可点击时）：--shadow-card-hover + translateY(-1px)
```

### 7.4 分类卡（参考图最标志性的一块）
```
网格 4列 × N行｜间距 12
背景 --surface｜圆角 10｜边框 1px --line｜内边距 14
第一行：图标容器（30px，圆角 8，分类浅色背景，分类主色图标 17px） ……… 数字右对齐 22px/700 tabular-nums
第二行：分类名 13px/500 --text
第三行：路径 11px/400 --text-3
```

### 7.5 角标 / 标签
```
高度 20px｜水平内边距 px 8｜圆角 6｜11px/600
实底（primary + 白字）用于状态，如「文档」
浅底（--surface-3 + --text-2）用于说明，如「仅根目录」
```

### 7.6 输入框
```
高度 36px｜圆角 8｜边框 1px --line｜背景 --surface｜内边距 0 12｜13px
聚焦：边框 --primary + box-shadow 0 0 0 3px var(--primary-ring)
错误：边框 --danger + 下方 12px --danger 提示
```

### 7.7 开关（iOS 式）
```
轨道 40×22｜全圆角（radius full）｜滑块 18
关：背景 --line-strong｜开：背景 --primary
过渡 160ms ease
旁侧文字：标题 13px/500 + 副标 11px/400 --text-3
```

### 7.8 空态（参考图「没有待整理的文件」）
```
图标容器 40px（圆角 10，--primary-tint 背景，--primary 图标）
标题 16px/600 --text
描述 12.5px/400 --text-3
动作组：次按钮 + 主按钮
```
> **不要只写一行「无数据」**。空态必须有：图标 + 标题 + 说明 + 出路。

### 7.9 Toast（参考图底部「✓ 已归入 …」）
```
位置：底部居中，距底部 28px
背景 --surface｜圆角 10｜--shadow-pop｜内边距 12px 18px
勾选图标 --primary｜正文 13px｜强调词 --primary 600｜「可撤销」为文字按钮
进入 160ms translateY(8px)→0 + opacity
```

### 7.10 眉标（eyebrow）
```
图标 13px（--primary）+ 文字 12px/500（--primary）
位于大标题上方，间距 6px
```

---

## 8. 动效（克制，参考图是静态感很强的设计）

| 场景 | 规格 |
|---|---|
| 按钮/导航悬停 | `150ms ease` 背景色 |
| 开关 | `160ms ease` |
| 卡片悬停 | `200ms ease` 阴影 + 1px 位移 |
| Toast 进入 | `160ms ease-out` 位移 8px + 淡入 |
| Toast 退出 | `120ms`（**比进入更快**） |
| 弹层 | `180ms cubic-bezier(0.16,1,0.3,1)` |

**禁止**：
- `transition: all`（必须写具体属性）
- 滚动淡入（fade-in-up 在全站铺开是最明显的 AI 痕迹，参考图没有）
- 任何循环动画
- 不尊重 `prefers-reduced-motion`

---

## 9. 营销外框（参考图的宣传图样式）

制作产品宣传截图时套用这一层：

```
背景：linear-gradient(160deg, #EEF2FF 0%, #F8FAFF 45%, #FFFFFF 100%)
     + 斜向光带（repeating-linear-gradient(120deg, rgba(255,255,255,.6) 0 2px, transparent 2px 26px)）
标题：44px/700，-0.025em，前半 --text、后半 --primary（两段式）
副标：18px/400 --text-2，用「 · 」分隔要点
截图：macOS 红绿灯或 Windows 标题栏 + 圆角 14 + --shadow-modal
```

---

## 10. 现有 → 目标 改动清单

| # | 现值 | 目标 | 文件 | 风险 |
|---|---|---|---|---|
| 1 | `--purple: #635bff` | `--primary: #4F46E5` | `styles.css` | 低 |
| 2 | `--purple-soft: #7a73ff` | `--primary-soft: #6366F1` | `styles.css` | 低 |
| 3 | `--cyan: #00d4ff` | 移入分类色板 | `styles.css` | 低 |
| 4 | 无 `--primary-tint/ring` | 新增 | `styles.css` | 低 |
| 5 | `--r-lg 8 / --r-xl 12` | 补 `--r-sm/md/lg/xl/2xl/full` | `styles.css` | 低 |
| 6 | `--sidebar-w: 190px` | `220px` | `styles.css` | 低 |
| 7 | 阴影 `rgba(10,37,64,·)` | 统一为冷蓝调（或保留，二者皆可） | `styles.css` | 低 |
| 8 | `--sans` 无 Windows 中文字体 | 补 MiSans / HarmonyOS Sans / 微软雅黑 | `styles.css` + 字体打包 | 中 |
| 9 | 手写 SVG ×34 | 换 `lucide-react` | `App.tsx` | **高** |
| 10 | `App.tsx` 123KB 单体 | 按视图拆组件 | `src/shell/**` | **高** |
| 11 | 无分类卡/空态/开关等形态 | 按 §7 新建 | `src/shell/**` | 中 |

---

## 11. 实施顺序（建议）

| 阶段 | 内容 | 可验证 |
|---|---|---|
| **0** | 修改 `styles.css` 的 CSS 变量（#1–#8） | 截图对比，颜色/圆角/阴影生效 |
| **1** | 引入 `lucide-react`，替换导航区图标 | 图标笔画粗细一致 |
| **2** | 侧栏三段式重排（220px + 底部状态卡 + 脚注） | 与参考图并排比对 |
| **3** | 主区页眉（header）+ 分类卡网格 + 空态 + 开关 | 一屏 1:1 |
| **4** | 拆分组件，缩减 `App.tsx` 体积 | typecheck + 功能回归 |
| **5** | 搜索面板 / 账号中心 / 设置补齐为同一套 | 跨页一致性 |

**铁律**：
- 一次只改**一屏**，改完截图与参考图**并排对比**，确认后再进入下一屏。
- 不改 IPC、不改 props 签名、不改数据流 —— **纯视觉层**。
- 不引入第二个强调色；分类色不得外溢到按钮/文字/背景。
- 所有间距均采用 §5 的间距刻度（scale）；禁止游离值。
- 所有交互元素四态齐全（default / hover / focus-visible / active），焦点环可见。

---

## 12. 验收清单

- [ ] 主色为靛蓝色（indigo）`#4F46E5`，全客户端无残留 `#635bff`
- [ ] 侧栏 220px 三段式，激活项为实底药丸
- [ ] 侧栏背景与主区背景**有明暗差**（白色与浅灰蓝）
- [ ] 中性色全部偏冷，无暖灰混入
- [ ] 所有图标描边粗细一致（2px）、端点一致（round）
- [ ] 分类卡 4 列，图标浅底 + 右上大数字，数字 `tabular-nums`
- [ ] 空态有图标 + 标题 + 说明 + 出路，不是「无数据」
- [ ] 危险操作（卸载）使用 `--danger`，不与主行动抢色
- [ ] 无 `transition: all`，无滚动淡入，尊重 `prefers-reduced-motion`
- [ ] 无 7px / 13px / 21px 游离间距
- [ ] 嵌套元素圆角同心（外层 = 内层 + padding）
- [ ] 焦点环全部可见

---

## 13. 配套 Skill（执行本文档时使用）

选择 **`redesign`**（plugin87/ux-ui-agent-skills），理由是它与本文档的约束**一一对应**：

| 本文档的要求 | `redesign` 提供的对应物 |
|---|---|
| §10 改动清单要按「CSS 变量 → 排版间距 → 组件状态 → 动效」推进 | 明文规定的 **apply（应用）顺序**：tokens first（令牌优先）→ typography/spacing（排版/间距）→ component states（组件状态）→ motion（动效） |
| §12「无残留 `#635bff`」「禁止游离值」 | **`scripts/lint_hardcodes.py`** 扫描改动代码中的硬编码色值与主题外数值 |
| §12 验收中的对比度 | **`scripts/validate_contrast.py`** 直接运行 token 源 |
| 三处品牌色不统一（官网/安装器/客户端） | **Single-Theme Consistency（单主题一致性）**规则：「保留多个页面各用一套配色 = 这次改造失败」 |
| 「不改 IPC、不改 props、不改数据流」 | 护栏（Guardrail）：**绝不为了美观牺牲正常工作的功能**；流程中有「对每个此前可正常工作的流程执行冒烟测试」 |
| §7 组件状态要齐全 | 配套 `a11y-audit` 按 WCAG 2.2 AA 执行 |

**来源**：`github.com/plugin87/ux-ui-agent-skills` → 仓库内 `.claude/skills/redesign`
**安装**：`npx skills add https://github.com/plugin87/ux-ui-agent-skills --skill redesign`
**OpenCode 落位**：将该 `SKILL.md` 放到 `.opencode/skill/redesign/SKILL.md`

**执行顺序**：先运行 **Scan → Diagnose** 阶段，**只生成 findings 报告，不修改代码**；
将报告与本文档 §10 改动清单进行对照，确认范围后再进入 Apply 阶段。

> 可选第二道：交付后用 Vercel `web-design-guidelines` 出一份 `file:line` 质检报告
> （`npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines`）。
> 它**只审计不改美学**，零风险。但**不要**安装 Anthropic 的 `frontend-design`——
> 该 skill 明文禁止「紫渐变」，会试图改掉我们已锁定（LOCKED）的靛蓝色（indigo）品牌色。
