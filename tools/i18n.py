# --------------------------------------------------------------------------- #
# Site-chrome internationalisation
# --------------------------------------------------------------------------- #
#
# The site speaks to a bilingual audience, so the chrome that wraps the packs
# is translated rather than assumed. This module is the single source of that
# vocabulary: every string the page templates emit that is *chrome* — nav,
# buttons, panel labels, empty states, copy feedback — lives here in both
# languages, and `tools/build-site.py` renders one of them.
#
# Three rules keep the layer honest:
#
#   1. **Chrome only.** Pack prose is authored content: it already carries its
#      own `lang` attribute (`build-site.annotate_lang`) and half of it is
#      deliberately bilingual (《网络安全法》, 会签). Translating that would
#      mean publishing a second, divergent copy of every pack. The chrome, by
#      contrast, was half English and half Chinese in the *same* header — an
#      English nav above a Chinese spec panel — which is what this fixes.
#
#   2. **Both languages are always complete.** `t()` raises on a missing key
#      or a missing translation, so a half-translated string fails the build
#      rather than shipping blank chrome. `tests/test_i18n.py` asserts the
#      same thing from the outside.
#
#   3. **No markup inside a value.** Every value is plain text, because the
#      client re-renders it with `textContent` when the reader switches
#      language. A value that needs to sit *next to* a `<code>` element is
#      therefore split into several keys around it.
#
# The dictionary is emitted verbatim as `assets/i18n.js` at build time, so the
# client's `window.OSA_I18N.t()` and the server's `t()` can never disagree.

from __future__ import annotations

import json

LOCALES = ("en", "zh")
DEFAULT_LOCALE = "en"

# A locale as the document should declare it. The switch keys on "zh" because
# that is what a reader's preference looks like; the document needs the tag.
HTML_LANG = {"en": "en", "zh": "zh-CN"}


STRINGS: dict[str, dict[str, str]] = {
    # ---- titlebar -------------------------------------------------------- #
    "skip": {
        "en": "Skip to content",
        "zh": "跳至正文",
    },
    "nav.catalog": {"en": "Catalog", "zh": "目录"},
    "nav.standard": {"en": "Standard", "zh": "规范"},
    "nav.taxonomy": {"en": "Taxonomy", "zh": "分类体系"},
    "nav.roadmap": {"en": "Roadmap", "zh": "路线图"},
    "nav.menu": {"en": "Menu", "zh": "菜单"},
    "nav.menu.label": {"en": "Toggle navigation", "zh": "展开或收起导航"},
    "lang.switch": {"en": "Language", "zh": "语言"},
    "lang.en": {"en": "EN", "zh": "EN"},
    "lang.zh": {"en": "中文", "zh": "中文"},

    # ---- translation status -------------------------------------------- #
    # A Chinese build renders the translated chapter where one exists and the
    # English original where one does not. The reader is told which: a page
    # that quietly mixes two languages is worse than either one alone.
    "trans.banner": {
        "en": "No Chinese translation of this page yet; the English original "
              "follows.",
        "zh": "本页尚无中文译本，以下为英文原文。",
    },

    # ---- footer ---------------------------------------------------------- #
    # Every value carries its own spacing: the template joins these pieces with
    # no whitespace of its own where the two languages need different spacing,
    # so an English comma does not become a space before a Chinese one.
    "footer.lead": {
        "en": "— blueprints for real enterprise systems.",
        "zh": "真实企业系统的蓝图。",
    },
    "footer.content": {"en": "Content ", "zh": "内容 "},
    "footer.comma": {"en": ", ", "zh": "，"},
    "footer.code": {"en": "code ", "zh": "代码 "},
    "footer.end": {"en": ".", "zh": "。"},
    "footer.draft": {"en": "Every pack is ", "zh": "每个方案包都是 "},
    "footer.and": {"en": " and ", "zh": "，且"},
    "footer.not_verified": {"en": "not field-verified", "zh": "未经现场验证"},
    "footer.trust.lead": {
        "en": "— read its ",
        "zh": "—— 采信任何具体论断之前，请先阅读它的 ",
    },
    "footer.trust.tail": {"en": ".", "zh": "。"},

    # ---- catalog --------------------------------------------------------- #
    "dir.contents": {
        "en": "Contents of {path}/ in Open Solution Atlas.",
        "zh": "Open Solution Atlas \u4e2d {path}/ \u7684\u76ee\u5f55\u5185\u5bb9\u3002",
    },
    "catalog.page.title": {
        "en": "Open Solution Atlas \u2014 blueprints for real enterprise systems",
        "zh": "Open Solution Atlas \u2014\u2014 \u9762\u5411\u771f\u5b9e\u4f01\u4e1a\u7cfb\u7edf\u7684\u84dd\u56fe\u5e93",
    },
    "catalog.page.desc": {
        "en": "Seventeen machine-readable blueprints for real enterprise "
              "systems, each with traced identifiers, integrity constraints "
              "and prompts assembled from the pack itself.",
        "zh": "\u5341\u4e03\u4e2a\u53ef\u673a\u5668\u8bfb\u53d6\u7684\u771f\u5b9e\u4f01\u4e1a\u7cfb\u7edf\u84dd\u56fe\uff0c"
              "\u6bcf\u4e2a\u90fd\u5e26\u6709\u53ef\u8ffd\u6eaf\u7684\u7f16\u53f7\u3001\u5b8c\u6574\u6027\u7ea6\u675f\uff0c"
              "\u4ee5\u53ca\u7531\u65b9\u6848\u5305\u81ea\u8eab\u62fc\u88c5\u7684\u63d0\u793a\u8bcd\u3002",
    },
    "catalog.hero.title1": {
        "en": "Production-grade blueprints",
        "zh": "生产级蓝图",
    },
    "catalog.hero.title2": {
        "en": "for real enterprise systems",
        "zh": "面向真实企业系统",
    },
    "catalog.hero.sub": {
        "en": "MES · WMS · IAM · BI · workflow · government services — every "
              "decision traced, every identifier resolved, a prompt assembled "
              "from the pack itself, and an interactive demo that shows the "
              "rule failing.",
        "zh": "MES · WMS · IAM · BI · 工作流 · 政务服务 —— 每个决策都有追溯、"
              "每个标识符都可解析、提示词由方案包自身拼装而成，"
              "还有一个会把规则如何失败演示出来的交互 demo。",
    },
    "catalog.trust.draft": {"en": "Every pack is", "zh": "每个方案包都是"},
    "catalog.trust.none": {"en": "; none has been ", "zh": "，且均未经过"},
    "catalog.trust.verified": {"en": "field-verified", "zh": "现场验证"},
    "catalog.trust.maturity": {
        "en": ". Maturity measures completeness, not correctness",
        "zh": "。成熟度衡量的是完整度，而不是正确性",
    },
    "catalog.trust.check": {"en": " — check each pack’s ", "zh": " —— 请查看每个方案包的 "},    "catalog.trust.tail": {"en": ".", "zh": "。"},
    "catalog.search.placeholder": {
        "en": "Search {n} packs — try “warehouse”, “会签”, "
              "“federated login”, “FEFO”…",
        "zh": "搜索 {n} 个方案包 —— 试试「仓储」、「会签」、单点登录、FEFO…",
    },
    "catalog.search.clear": {"en": "Clear filters", "zh": "清除筛选"},
    "facet.domain": {"en": "domain", "zh": "领域"},
    "facet.maturity": {"en": "maturity", "zh": "成熟度"},
    "facet.verification": {"en": "verification", "zh": "验证状态"},
    "catalog.count.some": {
        "en": "{n} of {total} packs", "zh": "共 {total} 个中的 {n} 个"},
    "catalog.empty.title": {
        "en": "No pack matches those filters",
        "zh": "没有方案包符合当前筛选",
    },
    "catalog.empty.body": {
        "en": "Seventeen packs are on the shelf. Clear the filters to see all "
              "of them, or search for a capability rather than a pack name.",
        "zh": "货架上一共 17 个方案包。清除筛选即可看到全部；"
              "也可以按能力而不是按方案包名称来搜索。",
    },
    "catalog.hint": {
        "en": "Search is loaded on first use, so browsing never pays for the index.",
        "zh": "搜索索引在首次使用时才加载，纯浏览不会为此付出代价。",
    },
    "catalog.search.fail": {
        "en": "Search is unavailable — the search library failed to load.",
        "zh": "搜索不可用 —— 搜索库加载失败。",
    },
    "catalog.search.loading": {"en": "Loading search index…", "zh": "正在加载搜索索引…"},
    "catalog.search.index_fail": {
        "en": "Search index unavailable — facet filtering still works.",
        "zh": "搜索索引不可用 —— 但仍可以按筛选条件过滤。",
    },
    "catalog.search.waiting": {"en": "Loading the search index…", "zh": "正在加载搜索索引…"},
    "catalog.search.waiting_fail": {
        "en": "Search is unavailable — the index could not be loaded. "
              "Use the filters below.",
        "zh": "搜索不可用 —— 索引无法加载，请改用下方的筛选条件。",
    },
    "word.result": {"en": "results", "zh": "条结果"},
    "word.result.one": {"en": "result", "zh": "条结果"},
    "word.pack": {"en": "packs", "zh": "个方案包"},
    "catalog.hits.count": {"en": "{n} {word} for “{q}”", "zh": "“{q}”：{n} {word}"},
    "catalog.hits.empty": {
        "en": "Nothing matched “{q}”. Try a tag like “warehouse” or “OEE”.",
        "zh": "没有匹配“{q}”的内容。可以试试「仓储」或「OEE」这类标签。",
    },
    "hit.kind.pack": {"en": "solution", "zh": "方案包"},
    "hit.kind.doc": {"en": "chapter", "zh": "章节"},
    "hit.kind.other": {"en": "about", "zh": "关于"},

    # ---- generated listings and breadcrumbs ------------------------------ #
    "crumb.catalog": {"en": "Catalog", "zh": "目录"},
    "dir.items": {"en": "{n} items", "zh": "{n} 项"},
    "dir.items.one": {"en": "1 item", "zh": "1 项"},

    # ---- 404 ------------------------------------------------------------- #
    "notfound.title": {"en": "Page not found", "zh": "页面未找到"},
    "notfound.body": {
        "en": "That page does not exist — it may have been renamed when a pack "
              "was promoted. The catalog is searchable.",
        "zh": "这个页面不存在 —— 方案包升级时它可能被改名了。可以到目录里搜索。",
    },
    "notfound.back": {"en": "← Back to the catalog", "zh": "← 返回目录"},

    # ---- pack chrome ----------------------------------------------------- #
    "side.overview": {"en": "overview", "zh": "概览"},
    "side.standard": {"en": "pack standard", "zh": "方案包规范"},
    "view.doc": {"en": "Document view", "zh": "文档视图"},
    "view.spec": {"en": "Structured view", "zh": "结构视图"},
    "view.spec.count": {"en": " · {n} IDs", "zh": " · {n} 条标识"},

    # ---- structured spec panel ------------------------------------------- #
    "spec.head": {
        "en": "Spec panel · {total} identifiers",
        "zh": "规格面板 · {total} 条已识别标识",
    },
    "spec.note.by": {"en": "Generated by ", "zh": "由 "},
    "spec.note.from": {
        "en": " from this pack’s Markdown ",
        "zh": " 从本包 Markdown ",
    },
    "spec.note.verb": {"en": "extracted", "zh": "抽取"},
    "spec.note.tail": {
        "en": " rather than written by hand: the numbers below change with the "
              "pack’s content, same source and same version as the prose.",
        "zh": "而成，不是手写页面：下列数字随包内容变化，与散文同源同版本。",
    },
    "spec.reuse.label": {"en": "Machine-readability", "zh": "机器可读性"},
    "spec.reuse.hint": {
        "en": "(a section marked “prose-only” holds identifiers that cannot be "
              "structured yet — a content TODO, not a parsing limit)",
        "zh": "(标记为「仅散文」的章节含有标识但无法结构化，"
              "是内容待办而不是解析上限)",
    },
    "spec.status.structured": {"en": "structured", "zh": "可结构化"},
    "spec.status.prose-only": {"en": "prose", "zh": "仅散文"},
    "spec.status.absent": {"en": "missing", "zh": "缺失"},
    "spec.refs.cited": {"en": "Referenced by: ", "zh": "被引用："},
    "spec.refs.enforced": {"en": "Enforced by: ", "zh": "强制："},
    "spec.refs.traces": {"en": "Traces to: ", "zh": "追溯："},
    "spec.stat.rules": {"en": "Business rules", "zh": "业务规则"},
    "spec.stat.requirements": {"en": "Requirements", "zh": "功能需求"},
    "spec.stat.nfrs": {"en": "NFR targets", "zh": "非功能目标"},
    "spec.stat.controls": {"en": "Controls", "zh": "合规控制"},
    "spec.stat.adrs": {"en": "ADRs", "zh": "架构决策"},
    "spec.stat.constraints": {"en": "Integrity constraints", "zh": "完整性约束"},
    "spec.stat.store": {"en": "of which store-enforced", "zh": "其中由存储强制"},
    "spec.stat.policy": {"en": "policy-assumed targets", "zh": "策略假定目标"},
    "spec.sec.adrs": {"en": "Architecture decisions", "zh": "架构决策"},
    "spec.sec.rules": {"en": "Business rules", "zh": "业务规则"},
    "spec.sec.requirements": {"en": "Functional requirements", "zh": "功能需求"},
    "spec.sec.nfrs": {"en": "Non-functional targets", "zh": "非功能目标"},
    "spec.sec.controls": {"en": "Compliance controls", "zh": "合规控制"},
    "spec.sec.constraints": {"en": "Data-model constraints", "zh": "数据模型约束"},
    "spec.sec.capabilities": {"en": "Capabilities", "zh": "能力"},
    "spec.sec.contexts": {"en": "Bounded contexts", "zh": "限界上下文"},
    "spec.store.tail": {"en": "store-enforced", "zh": "由存储强制"},
    "spec.store.tooltip": {
        "en": "the data model claims this is enforced in the store",
        "zh": "数据模型声称此项由存储强制执行",
    },
    "spec.demo": {"en": "Open interactive demo", "zh": "打开交互 demo"},

    # ---- prompt bundles -------------------------------------------------- #
    "prompts.heading": {
        "en": "Prompts · assembled from this pack",
        "zh": "提示词 · 由本包内容拼装",
    },
    "prompts.note.1": {
        "en": "These are not template placeholders. Every one is assembled at "
              "build time by ",
        "zh": "这些不是模板占位。每条都由 ",
    },
    "prompts.note.2": {"en": " from ", "zh": " 在构建期从 "},
    "prompts.note.pack": {"en": "this pack", "zh": "本包"},
    "prompts.note.3": {
        "en": "’s rules, decided decisions, enforced constraints and testable "
              "targets: ",
        "zh": "的规则、已决决策、强制约束与可测目标拼装而成：带上 ",
    },
    "prompts.note.3b": {"en": "’s semantics, ", "zh": " 的语义、"},
    "prompts.note.4": {
        "en": "’s decision and the store-level constraints is what makes the "
              "generated artefact capable of carrying defined guarantees — "
              "“build me a workflow engine with approvals” will not, and "
              "polishing it will not either. Every bundle states the honesty "
              "conditions (",
        "zh": " 的决策和存储级约束，生成的东西才可能具备已定义的保证 —— "
              "只说「做一个带审批的工作流引擎」不会，而且再润色也不会。"
              "每条都写明诚实条件（",
    },
    "prompts.note.5": {
        "en": ", no compliance claim, ",
        "zh": "、不主张符合性、",
    },
    "prompts.note.6": {
        "en": " is policy rather than a measurement), because the prompt that "
              "omits them gets an implementation that quietly invents them.",
        "zh": " 是策略而非测量），因为省略它们的提示词，会让实现方悄悄把那些东西发明出来。",
    },
    "prompt.copy": {"en": "Copy prompt", "zh": "复制提示词"},
    "prompt.copy_one": {"en": "Copy", "zh": "复制"},
    "prompt.copy_all": {"en": "Copy whole pack", "zh": "复制整包"},
    "prompt.download": {"en": "Download .md", "zh": "下载 .md"},
    "prompt.download_ctx": {"en": "Download context.md", "zh": "下载 context.md"},
    "prompt.impl.title": {"en": "Implement a prototype to spec", "zh": "按规格实现原型"},
    "prompt.impl.blurb": {
        "en": "capabilities · rules · decided decisions · enforced constraints "
              "· testable targets",
        "zh": "能力 · 规则 · 已决决策 · 强制约束 · 可测目标",
    },
    "prompt.adr.title": {"en": "Implement one ADR’s decision", "zh": "实现一条 ADR 的决策"},
    "prompt.adr.blurb": {
        "en": "{n}: the decision + the requirements that depend on it + the file "
              "holding the rejected alternatives",
        "zh": "{n} 条：决策 + 依赖它的需求 + 被否备选项所在文件",
    },
    "prompt.test.title": {"en": "Generate tests for one rule", "zh": "为一条规则生成测试"},
    "prompt.test.blurb": {
        "en": "{n}: the proposition + the requirement that enforces it + the "
              "formula that measures it",
        "zh": "{n} 条：命题 + 强制它的需求 + 测量它的公式",
    },
    "prompt.ctx.title": {
        "en": "Export the whole pack’s context",
        "zh": "导出整包上下文",
    },
    "prompt.ctx.blurb": {
        "en": "{n} characters · each chapter as written, for the model that "
              "needs the source rather than a summary",
        "zh": "{n} 字符 · 各章节原文，供需要原文而非摘要的模型",
    },
    "prompt.aria.inline": {
        "en": "Prompt: implement this pack",
        "zh": "提示词：按规格实现本包",
    },
    "prompt.hint.inline": {
        "en": "Generated from this pack by tools/prompts.py",
        "zh": "由本包内容经 tools/prompts.py 生成",
    },

    # ---- copy feedback (runtime) ----------------------------------------- #
    "copy.ok": {"en": "Copied", "zh": "已复制"},
    "copy.fail": {
        "en": "Copy failed — select the text manually",
        "zh": "复制失败，请手动选择",
    },
    "copy.read_fail": {
        "en": "Could not read the file — open it to copy manually",
        "zh": "读取失败，请打开文件手动复制",
    },

    # ---- enum labels ----------------------------------------------------- #
    # L1 and L4 are in the table although no pack sits there today: the trust
    # ladder is a ladder, so a pack reaching L4 must not render a raw "L4."
    "maturity.L1": {"en": "L1 · Brief", "zh": "L1 · 简报"},
    "maturity.L2": {"en": "L2 · Blueprint", "zh": "L2 · 蓝图"},
    "maturity.L3": {"en": "L3 · Agent-ready", "zh": "L3 · 智能体就绪"},
    "maturity.L4": {"en": "L4 · Proven", "zh": "L4 · 已验证"},
    "verify.unverified": {"en": "unverified", "zh": "未验证"},
    "verify.source-checked": {"en": "source-checked", "zh": "已核对来源"},
    "verify.practitioner-reviewed": {
        "en": "practitioner-reviewed",
        "zh": "从业者已评审",
    },
    "verify.field-proven": {"en": "field-proven", "zh": "现场已验证"},
}


def has(key: str) -> bool:
    return key in STRINGS


def t(key: str, lang: str = DEFAULT_LOCALE, **vars: object) -> str:
    """The `key` string in `lang`, with `{name}` placeholders filled.

    Raises on an unknown key or a missing translation: chrome that is blank in
    one language is worse than a build that stops.
    """
    if key not in STRINGS:
        raise KeyError(f"unknown i18n key: {key!r}")
    entry = STRINGS[key]
    if lang not in entry:
        raise KeyError(f"i18n key {key!r} has no {lang!r} translation")
    text = entry[lang]
    for name, value in vars.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def dictionary() -> dict[str, dict[str, str]]:
    """The whole catalog, as the client needs it."""
    return {key: dict(value) for key, value in STRINGS.items()}


# --------------------------------------------------------------------------- #
# The client runtime
# --------------------------------------------------------------------------- #

# Emitted as `assets/i18n.js`. Kept in this module because it *is* the
# dictionary's other half: the build inlines the catalog above into it, and a
# hand-written copy could drift from the Python one.
I18N_JS_TEMPLATE = r"""/* Generated by tools/i18n.py from the site's string catalog — do not edit.
 *
 * The chrome is server-rendered in the build's language (see build-site.py's
 * --lang), because that is what a reader with JavaScript disabled must get.
 * This file is what lets the reader *choose* between the two: it swaps the
 * text of every `data-i18n` node and attribute in `data-i18n-attrs`, sets
 * <html lang>, remembers the choice, and tells the rest of the page through
 * an `osalocalechange` event so the search module can re-render its strings.
 *
 * Everything degrades: without this script the page is still fully readable
 * in the build's language, and without a stored preference the browser's own
 * language decides.
 *
 * When the site was built with both languages (the English tree at the root
 * and the Chinese tree under zh/), the switch is a link to the same page in
 * the other tree, and this script follows it - prose and chrome change
 * together, which is the only way a page can be in one language. */

(function () {
  "use strict";

  var STRINGS = __DICTIONARY__;
  var FALLBACK = "en";
  var STORE_KEY = "osa-locale";
  var locale = FALLBACK;

  function fill(text, vars) {
    if (!vars) return text;
    return text.replace(/\{(\w+)\}/g, function (match, name) {
      return Object.prototype.hasOwnProperty.call(vars, name)
        ? String(vars[name])
        : match;
    });
  }

  function t(key, vars) {
    var entry = STRINGS[key];
    if (!entry) return key;
    var text = entry[locale] != null ? entry[locale] : entry[FALLBACK];
    return fill(text, vars);
  }

  function varsOf(el) {
    // `data-i18n-vars` is a `key=value` list, not JSON: these attributes are
    // emitted by Python format strings, where braces are not free.
    var raw = el.getAttribute("data-i18n-vars");
    if (!raw) return null;
    var vars = {};
    raw.split(/\s+/).forEach(function (pair) {
      var at = pair.indexOf("=");
      if (at > 0) vars[pair.slice(0, at)] = pair.slice(at + 1);
    });
    return vars;
  }

  function htmlLang(value) {
    return value === "zh" ? "zh-CN" : "en";
  }

  /* The counterpart of this page in the other language, if the site was
   * built with both trees. The build writes it into the body, because only
   * the page knows its own path. An empty value means "there is no other
   * language here" - a single-language build, where the switch can only
   * repaint the chrome. */
  function altUrl(lang) {
    var body = document.body;
    if (!body) return "";
    var value = body.getAttribute("data-alt-" + lang);
    return value && value.trim() ? value.trim() : "";
  }

  function buildLang() {
    var lang = document.documentElement.getAttribute("lang") || "";
    return lang.indexOf("zh") === 0 ? "zh" : "en";
  }

  function remember(lang) {
    try {
      window.localStorage.setItem(STORE_KEY, lang);
    } catch (e) {
      /* private mode and file:// origins: the choice simply does not persist. */
    }
  }

  function apply() {
    document.documentElement.setAttribute("lang", htmlLang(locale));
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = t(el.getAttribute("data-i18n"), varsOf(el));
    });
    // A string that lives in an attribute (a placeholder, an aria-label, a
    // title) carries its target attribute in the marker itself:
    // `data-i18n-placeholder="the.key"`.
    ["placeholder", "aria-label", "title"].forEach(function (attr) {
      document.querySelectorAll("[data-i18n-" + attr + "]").forEach(function (el) {
        el.setAttribute(attr, t(el.getAttribute("data-i18n-" + attr), varsOf(el)));
      });
    });
    document.querySelectorAll("[data-locale]").forEach(function (button) {
      button.setAttribute(
        "aria-pressed",
        button.getAttribute("data-locale") === locale ? "true" : "false"
      );
    });
    try {
      window.localStorage.setItem(STORE_KEY, locale);
    } catch (e) {
      /* private mode and file:// origins: the choice simply does not persist. */
    }
    document.dispatchEvent(
      new CustomEvent("osalocalechange", { detail: { locale: locale } })
    );
  }

  function initialLocale() {
    var stored = null;
    try {
      stored = window.localStorage.getItem(STORE_KEY);
    } catch (e) {
      /* no storage: fall through to the browser's language. */
    }
    if (stored === "en" || stored === "zh") return stored;
    var nav = (window.navigator.language || "").toLowerCase();
    return nav.indexOf("zh") === 0 ? "zh" : FALLBACK;
  }

  locale = initialLocale();

  window.OSA_I18N = {
    locale: function () { return locale; },
    t: t,
    setLocale: function (next) {
      if (next !== "en" && next !== "zh") return;
      if (next === locale) return;
      locale = next;
      apply();
    }
  };

  function ready() {
    /* A bilingual site has a page in the reader's language; the prose cannot
     * be repainted, only the chrome, so the reader is taken there instead.
     * Repainting the chrome alone is what produces a Chinese navigation over
     * English prose. */
    var preferred = initialLocale();
    var target = preferred === buildLang() ? "" : altUrl(preferred);
    if (target) {
      remember(preferred);
      window.location.replace(target);
      return;
    }
    apply();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready);
  } else {
    ready();
  }

  // Delegated so the control works wherever the page puts it, and so adding a
  // second copy of the switch (the nav has one too, for the narrow layout)
  // costs nothing.
  document.addEventListener("click", function (event) {
    var button = event.target && event.target.closest
      ? event.target.closest("[data-locale]")
      : null;
    if (!button) return;
    var next = button.getAttribute("data-locale");
    var target = altUrl(next);
    if (target) {
      remember(next);
      window.location.href = target;
      return;
    }
    window.OSA_I18N.setLocale(next);
  });
})();
"""


def render_i18n_js() -> str:
    """The runtime with the catalog inlined — one generated, deterministic file."""
    payload = json.dumps(dictionary(), ensure_ascii=False, sort_keys=True)
    return I18N_JS_TEMPLATE.replace("__DICTIONARY__", payload)
