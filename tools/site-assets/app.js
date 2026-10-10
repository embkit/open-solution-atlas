/* Solution Atlas — catalog search & filtering.
   Progressive enhancement: without JS the full card grid is already rendered.
   Search uses Fuse.js over search-index.json (pack + per-document entries);
   facets filter the server-rendered cards.

   The search index (~800 KB) is NOT fetched on page load: it is loaded lazily
   on first search interaction, so visitors who only browse or use the facet
   filters never pay for it. */

(function () {
  "use strict";

  var q = document.getElementById("q");
  var cards = document.getElementById("cards");
  var hits = document.getElementById("hits");
  var count = document.getElementById("count");
  var clearBtn = document.getElementById("clear");
  var status = document.getElementById("index-status");
  if (!q || !cards) return;

  var cardEls = Array.prototype.slice.call(cards.querySelectorAll(".card"));
  var totalPacks = cardEls.length;
  var active = { domain: new Set(), maturity: new Set(), verification: new Set() };
  var fuse = null;
  var index = null;
  var indexLoading = null;
  var emptyEl = null;

  function setStatus(message) {
    if (!status) return;
    status.textContent = message || "";
    status.hidden = !message;
  }

  // ---- search index: loaded lazily, exactly once -------------------------
  function loadIndex() {
    if (index || indexLoading) return indexLoading || Promise.resolve();
    if (typeof Fuse === "undefined") {
      setStatus("Search is unavailable — the search library failed to load.");
      return Promise.resolve();
    }
    setStatus("Loading search index…");
    indexLoading = fetch("search-index.json")
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        index = data;
        fuse = new Fuse(data, {
          includeScore: true,
          includeMatches: true,
          ignoreLocation: true,
          threshold: 0.34,
          minMatchCharLength: 2,
          keys: [
            { name: "t", weight: 0.42 },
            { name: "z", weight: 0.2 },
            { name: "g", weight: 0.16 },
            { name: "n", weight: 0.12 },
            { name: "x", weight: 0.1 }
          ]
        });
        setStatus("");
      })
      .catch(function () {
        setStatus("Search index unavailable — facet filtering still works.");
      });
    return indexLoading;
  }

  // ---- facets -----------------------------------------------------------
  document.querySelectorAll(".chip").forEach(function (chip) {
    chip.setAttribute("aria-pressed", "false");
    chip.addEventListener("click", function () {
      var facet = chip.getAttribute("data-facet");
      var value = chip.getAttribute("data-value");
      var set = active[facet];
      if (!set) return;
      if (set.has(value)) set.delete(value);
      else set.add(value);
      chip.setAttribute("aria-pressed", set.has(value) ? "true" : "false");
      render();
    });
  });

  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      Object.keys(active).forEach(function (k) { active[k].clear(); });
      document.querySelectorAll('.chip[aria-pressed="true"]').forEach(function (c) {
        c.setAttribute("aria-pressed", "false");
      });
      q.value = "";
      render();
    });
  }

  // ---- input ------------------------------------------------------------
  q.addEventListener("input", function () {
    render();
    if (q.value.trim()) loadIndex();
  });
  q.addEventListener("focus", function () {
    // Warm the index once the visitor shows search intent; do not block the
    // very first render on the network.
    if (q.value.trim()) loadIndex();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== q) {
      e.preventDefault();
      q.focus();
    } else if (e.key === "Escape" && document.activeElement === q) {
      q.value = "";
      render();
      q.blur();
    }
  });

  function facetActive() {
    return Object.keys(active).some(function (k) { return active[k].size > 0; });
  }

  function matchesActive(rec) {
    if (active.domain.size && !active.domain.has(rec.d)) return false;
    if (active.maturity.size && !active.maturity.has(rec.m)) return false;
    if (active.verification.size && !active.verification.has(rec.v)) return false;
    return true;
  }

  function cardMatches(el) {
    if (active.domain.size && !active.domain.has(el.getAttribute("data-domain"))) return false;
    if (active.maturity.size && !active.maturity.has(el.getAttribute("data-maturity"))) return false;
    if (active.verification.size && !active.verification.has(el.getAttribute("data-verification"))) return false;
    return true;
  }

  // ---- render -----------------------------------------------------------
  function render() {
    var query = q.value.trim();
    if (clearBtn) clearBtn.hidden = !(query || facetActive());

    if (query && fuse) {
      showHits(query);
    } else if (query && !index) {
      // Query typed, index not ready yet (or permanently unavailable).
      cards.hidden = true;
      hits.hidden = false;
      hits.innerHTML = "";
      if (count) count.textContent = "";
      var waiting = document.createElement("p");
      waiting.className = "count";
      waiting.textContent = indexLoading
        ? "Loading the search index…"
        : "Search is unavailable — the index could not be loaded. Use the filters below.";
      hits.appendChild(waiting);
    } else {
      showCards(query);
    }
  }

  function showCards(query) {
    cards.hidden = false;
    hits.hidden = true;
    var visible = 0;
    cardEls.forEach(function (el) {
      var ok = cardMatches(el);
      el.hidden = !ok;
      if (ok) visible++;
    });
    if (count) {
      count.textContent = visible === totalPacks
        ? totalPacks + " solutions"
        : visible + " of " + totalPacks + " solutions";
    }
    toggleEmpty(cards, visible === 0, "No solutions match those filters.");
  }

  function showHits(query) {
    var results = fuse.search(query, { limit: 60 });
    var filtered = results.filter(function (r) { return matchesActive(r.item); });
    cards.hidden = true;
    hits.hidden = false;
    if (count) count.textContent = filtered.length + " result" + (filtered.length === 1 ? "" : "s") + " for “" + query + "”";
    hits.innerHTML = "";
    filtered.forEach(function (r) { hits.appendChild(hitNode(r.item, query)); });
    toggleEmpty(hits, filtered.length === 0, "Nothing matched “" + query + "”. Try a tag like “warehouse” or “OEE”.");
  }

  function hitNode(rec, query) {
    var kind = rec.k === "pack" ? "solution" : (rec.k === "doc" ? "chapter" : "about");
    var path = rec.p ? rec.d + " / " + rec.p : rec.d;
    var a = document.createElement("a");
    a.className = "hit";
    a.href = rec.u;
    var top = document.createElement("div");
    top.className = "hit-top";
    var title = document.createElement("span");
    title.className = "hit-title";
    title.innerHTML = highlight(rec.t, query);
    var k = document.createElement("span");
    k.className = "hit-kind";
    k.textContent = kind + (path ? " · " + path : "");
    top.appendChild(title);
    top.appendChild(k);
    a.appendChild(top);
    var snip = snippet(rec.x, query);
    if (snip) {
      var p = document.createElement("p");
      p.className = "hit-snip";
      p.innerHTML = highlight(snip, query);
      a.appendChild(p);
    }
    return a;
  }

  function snippet(text, query) {
    if (!text) return "";
    var lower = text.toLowerCase();
    var needle = query.toLowerCase().split(/\s+/)[0];
    var at = lower.indexOf(needle);
    if (at < 0) return text.slice(0, 180) + (text.length > 180 ? "…" : "");
    var start = Math.max(0, at - 70);
    var end = Math.min(text.length, at + 140);
    return (start > 0 ? "…" : "") + text.slice(start, end).trim() + (end < text.length ? "…" : "");
  }

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function highlight(text, query) {
    var safe = esc(text);
    var terms = query.split(/\s+/).filter(function (t) { return t.length > 1; });
    if (!terms.length) return safe;
    var pattern = terms
      .map(function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); })
      .join("|");
    try {
      return safe.replace(new RegExp("(" + pattern + ")", "gi"), "<mark>$1</mark>");
    } catch (e) {
      return safe;
    }
  }

  function toggleEmpty(container, show, message) {
    if (show) {
      if (!emptyEl || emptyEl.parentNode !== container) {
        emptyEl = document.createElement("p");
        emptyEl.className = "count";
        container.appendChild(emptyEl);
      }
      emptyEl.textContent = message;
      emptyEl.hidden = false;
    } else if (emptyEl) {
      emptyEl.hidden = true;
    }
  }

  render();
})();
