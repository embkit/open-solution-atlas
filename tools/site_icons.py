#!/usr/bin/env python3
"""site_icons.py — the catalog's icon set and category palette.

The contract mandates Lucide at `stroke-width: 2`, `stroke-linecap: round`,
`24x24 viewBox` — and, for a repository that cannot take a runtime dependency,
explicitly permits a hand-drawn set that follows that spec:

    "若坚持零依赖，则必须手写一套统一规范的 SVG（描边 2px、
     `stroke-linecap:round`、24 viewBox）"

So the set below is hand-drawn to that spec rather than copied path data whose
provenance could not be checked. Every glyph is on a 24-grid, stroked at 2,
round caps and joins, and inherits `currentColor` so a category tint can drive
its stroke without a second rule.

Category colours are from contract §1.4 and, by that section's rule, may appear
**only** on an icon's stroke and its tinted background — never on a button, a
text run, or a card fill.
"""

from __future__ import annotations

# name -> (inner SVG markup on a 24 grid)
PATHS = {
    # --- navigation and chrome ---
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/>'
            '<rect x="14" y="3" width="7" height="7" rx="1.5"/>'
            '<rect x="3" y="14" width="7" height="7" rx="1.5"/>'
            '<rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "book": '<path d="M12 6.5C10.5 5 8.5 4 6 4H3v14h3c2.5 0 4.5 1 6 2.5"/>'
            '<path d="M12 6.5C13.5 5 15.5 4 18 4h3v14h-3c-2.5 0-4.5 1-6 2.5"/>',
    "network": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/>'
               '<circle cx="19" cy="19" r="2.5"/>'
               '<path d="M12 7.5v4M10.4 12.6 6.6 16.6M13.6 12.6l3.8 4"/>',
    "route": '<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/>'
             '<path d="M8.5 19H14a4 4 0 0 0 0-8H9a4 4 0 0 1 0-8h6.5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "chevron": '<path d="m9 6 6 6-6 6"/>',
    "arrow": '<path d="M5 12h13M12.5 6 19 12l-6.5 6"/>',
    "play": '<path d="M7.5 4.8v14.4L20 12 7.5 4.8Z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "check": '<path d="m5 13 4.5 4.5L19 7"/>',
    "alert": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5M12 16.4v.1"/>',
    "shield": '<path d="M12 3 5 6v6c0 4.5 3 8 7 9 4-1 7-4.5 7-9V6l-7-3Z"/>'
              '<path d="m9 12 2 2 4-4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/>'
            '<path d="m3.6 7.2 8.4 6 8.4-6"/>',
    "lock": '<rect x="4.5" y="10" width="15" height="10" rx="2"/>'
            '<path d="M8 10V7.5a4 4 0 0 1 8 0V10"/>',
    "empty": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>'
             '<path d="M8.5 11h5"/>',

    # --- domains ---
    "cpu": '<rect x="7" y="7" width="10" height="10" rx="2"/>'
           '<path d="M12 3v4M12 17v4M3 12h4M17 12h4"/>',
    "zap": '<path d="M13 2.5 5.5 13.5H11l-1 8.5 8-11.5H12l1-8Z"/>',
    "landmark": '<path d="M3 10.5h18M5 10.5v7.5M9.7 10.5v7.5M14.3 10.5v7.5'
                'M19 10.5v7.5M3 20.5h18M12 3l9 5.5H3L12 3Z"/>',
    "pulse": '<path d="M12 20.5S4.5 15.6 4.5 10.4A4.5 4.5 0 0 1 12 7.2a4.5 4.5 0 0 1 7.5 3.2'
             'c0 5.2-7.5 10.1-7.5 10.1Z"/>'
             '<path d="M5.8 12h2.7l1.4-2.4 1.9 4.8L13.3 12h4.9"/>',
    "workflow": '<rect x="3" y="4" width="6" height="6" rx="1.5"/>'
                '<rect x="15" y="14" width="6" height="6" rx="1.5"/>'
                '<path d="M9 7h4.5a2 2 0 0 1 2 2v5"/>',
    "factory": '<path d="M3 20.5h18V9l-6 4V9l-6 4V4H3v16.5Z"/>'
               '<path d="M6.5 17h2.5M12 17h2.5M17 17h1.5"/>',
    "bag": '<path d="M5.5 8h13l-1.2 12.5H6.7L5.5 8Z"/>'
           '<path d="M9 8V6.2a3 3 0 0 1 6 0V8"/>',
    "radio": '<circle cx="12" cy="12" r="2.5"/>'
             '<path d="M8.1 8.1a5.5 5.5 0 0 0 0 7.8M15.9 15.9a5.5 5.5 0 0 0 0-7.8"/>'
             '<path d="M5.2 5.2a9.5 9.5 0 0 0 0 13.6M18.8 18.8a9.5 9.5 0 0 0 0-13.6"/>',

    # --- pack-level overrides ---
    "user-cog": '<circle cx="10" cy="8" r="3.5"/><path d="M4 20a6 6 0 0 1 10.2-4.3"/>'
                '<circle cx="17.5" cy="16.5" r="2.4"/>'
                '<path d="M17.5 12.6v1.5M17.5 18.9v1.5M13.6 16.5h1.5M19.9 16.5h1.5"/>',
    "headset": '<path d="M5 15.5v-3.5a7 7 0 0 1 14 0v3.5"/>'
               '<rect x="3" y="14" width="4" height="6" rx="2"/>'
               '<rect x="17" y="14" width="4" height="6" rx="2"/>',
    "pen": '<path d="M4 20h4.5L19 9.5 14.5 5 4 15.5V20Z"/><path d="m13 6.5 4.5 4.5"/>',
    "truck": '<rect x="2.5" y="7" width="11.5" height="9" rx="1.5"/>'
             '<path d="M14 10h4l3.5 3.5V16H14"/>'
             '<circle cx="6.5" cy="18.2" r="1.8"/><circle cx="17.5" cy="18.2" r="1.8"/>',
    "warehouse": '<path d="M3 20.5V9l9-6 9 6v11.5H3Z"/><path d="M9 20.5v-6.5h6v6.5"/>',
    "database": '<ellipse cx="12" cy="6" rx="7.5" ry="3.2"/>'
                '<path d="M4.5 6v12c0 1.8 3.4 3.2 7.5 3.2s7.5-1.4 7.5-3.2V6"/>'
                '<path d="M4.5 12c0 1.8 3.4 3.2 7.5 3.2s7.5-1.4 7.5-3.2"/>',
    "chart": '<path d="M4 4v16h16"/><rect x="7" y="11" width="3" height="6" rx="1"/>'
             '<rect x="12" y="7" width="3" height="10" rx="1"/>'
             '<rect x="17" y="13" width="3" height="4" rx="1"/>',
    "flask": '<path d="M9 3h6M10 3v6.5L5.5 17a2 2 0 0 0 1.8 3h9.4a2 2 0 0 0 1.8-3'
             'L14 9.5V3"/><path d="M7.5 14h9"/>',
    "scale": '<path d="M12 4v16M6 8h12M8 8l-3 6h6L8 8ZM16 8l-3 6h6l-3-6Z"/>',
    "repeat": '<path d="M4 9a4 4 0 0 1 4-4h10M18 5l-3 3M20 15a4 4 0 0 1-4 4H6M6 19l3-3"/>',
    "map": '<path d="M9 4 3.5 6.5v13L9 17l6 2.5 5.5-2.5v-13L15 6.5 9 4Z"/>'
           '<path d="M9 4v13M15 6.5v13"/>',
}

# Contract §1.4 category palette. `tint` is the icon's background, `stroke` its
# colour; both are used *only* on `.cat-icon`.
CATEGORY = {
    "data-ai":            ("#0ea5e9", "#e0f2fe"),   # 格式转换 → 数据
    "energy-utilities":   ("#f97316", "#ffedd5"),   # 压缩解压 → 能源
    "government-public":  ("#6366f1", "#e0e7ff"),   # 音视频 → 政务
    "healthcare":         ("#22c55e", "#dcfce7"),   # 文件预览 → 医疗
    "horizontal":         ("#a855f7", "#f3e8ff"),   # 思维导图 → 横向
    "manufacturing":      ("#ef4444", "#fee2e2"),   # PDF → 制造
    "retail-commerce":    ("#d946ef", "#fae8ff"),   # 设计文件 → 零售
    "telecom":            ("#94a3b8", "#f1f5f9"),   # 其他 → 电信
}

DOMAIN_ICON = {
    "data-ai": "cpu",
    "energy-utilities": "zap",
    "government-public": "landmark",
    "healthcare": "pulse",
    "horizontal": "workflow",
    "manufacturing": "factory",
    "retail-commerce": "bag",
    "telecom": "radio",
}

PACK_ICON = {
    "his-emr": "pulse",
    "iam-platform": "user-cog",
    "itsm-helpdesk": "headset",
    "personal-blog": "pen",
    "wms": "warehouse",
    "tms": "truck",
    "mes": "factory",
    "power-marketing-cis": "scale",
    "one-stop-service": "landmark",
    "data-exchange": "network",
    "lakehouse-platform": "database",
    "enterprise-bi": "chart",
    "growth-analytics": "chart",
    "mlops-platform": "flask",
    "workflow-bpm": "workflow",
    "telecom-bss": "radio",
    "omnichannel-commerce": "bag",
}


def icon(name: str, css: str = "") -> str:
    """One inline SVG, hand-drawn to the contract's spec.

    Stroke is 2, caps and joins round, viewBox 24 — the contract's requirement
    for a zero-dependency set. `currentColor` is inherited so a category tint
    drives the stroke without a second rule.
    """
    body = PATHS.get(name)
    if body is None:
        body = PATHS["grid"]
    cls = f' class="{css}"' if css else ""
    return (
        f'<svg{cls} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{body}</svg>'
    )


def category_for(domain: str, slug: str = "") -> tuple[str, str]:
    """(stroke, tint) for a pack's icon container."""
    return CATEGORY.get(domain, ("#94a3b8", "#f1f5f9"))


def icon_for(domain: str, slug: str = "") -> str:
    """The glyph name for a pack: a pack override, else its domain's."""
    return PACK_ICON.get(slug) or DOMAIN_ICON.get(domain, "grid")
