/* Shared DOM stub for the bespoke demos.
 *
 * A demo that crashes on load is worse than no demo, and nothing else in the
 * repository exercises one. This loads a demo's inline script against a minimal
 * DOM, registering **every** button it creates — including buttons appended
 * into dynamically created wrappers, which the first version of this harness
 * missed and which made "every button is clickable" a true statement about an
 * empty set.
 *
 * The stub has to model four DOM behaviours the demos rely on, and getting any
 * of them wrong makes the harness test the stub instead of the demo:
 *
 *   - assigning `innerHTML` replaces children, and `textContent` reflects them;
 *     without both, stale nodes accumulate and every "is it gone yet?"
 *     assertion passes for the wrong reason.
 *   - `id` is a *property*: the demos build a control with `createElement` and
 *     then assign `.id`, so `getElementById` has to find that element
 *     afterwards. Registering only at creation time left the demo's own purpose
 *     selector invisible to the checks.
 *   - the page's own elements already exist when the script runs, so the ids
 *     the HTML declares are registered up front.
 *   - `getElementById` returns **null** for an id the page does not have. It
 *     used to mint a node on demand, which is how a demo that referenced a
 *     `#log` the page never declared could throw on load in a browser and still
 *     pass here. A stub that answers any question is not a test.
 */

const fs = require("fs");
const vm = require("vm");

const byId = {};
let elCount = 0;

function makeEl(id, tag) {
  const e = {
    id, tagName: tag || "div",
    _children: [], _attrs: {}, _html: "", _text: "", value: "",
    disabled: false, onclick: null, onchange: null,
    style: {}, classList: { toggle() {}, remove() {}, add() {} },
    appendChild(c) { this._children.push(c); return c; },
    removeChild() {},
    setAttribute(k, v) { this._attrs[k] = String(v); },
    getAttribute(k) { return this._attrs[k]; },
    querySelectorAll() { return []; },
    addEventListener() {},
  };
  Object.defineProperty(e, "innerHTML", {
    get() { return this._html; },
    set(v) { this._html = String(v); this._children = []; },
  });
  Object.defineProperty(e, "textContent", {
    get() { return this._text || ""; },
    set(v) { this._text = String(v); },
  });
  if (id) byId[id] = e;
  Object.defineProperty(e, "id", {
    get() { return this._id; },
    set(v) {
      const s = String(v);
      if (!s) return;
      this._id = s;
      byId[s] = this;
    },
  });
  e._id = id || `el${++elCount}`;
  return e;
}

function load(file, opts) {
  opts = opts || {};
  const html = fs.readFileSync(file, "utf8");
  const m = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) throw new Error("no inline <script> in " + file);
  const js = m[1];

  // one registry: getElementById reads it, and so does the returned `els`, so a
  // check can reach a control the demo built by assigning `.id`
  const els = byId;
  const buttons = [];
  for (const decl of html.matchAll(/\bid="([A-Za-z0-9_-]+)"/g)) {
    byId[decl[1]] = makeEl(decl[1]);
  }
  const el = (id) => els[id] || (els[id] = makeEl(id));
  // Every appendChild everywhere registers a button, so a demo that builds its
  // controls inside a generated wrapper is covered.
  const origCreate = (tag) => makeEl("new", tag);

  const document = {
    getElementById: (id) => byId[id] || null,
    createElement: origCreate,
    querySelectorAll: () => [],
    prompt: () => (opts.prompt === undefined ? "test reason" : opts.prompt),
  };

  const seen = new Set();
  function track(e) {
    if (seen.has(e)) return e;
    seen.add(e);
    const orig = e.appendChild.bind(e);
    e.appendChild = function (c) {
      if (c && String(c.tagName).toLowerCase() === "button") {
        c._label = c.textContent || c._text || "";
        buttons.push(c);
      }
      return orig(c);
    };
    return e;
  }
  document.createElement = (tag) => track(origCreate(tag));
  const origGet = document.getElementById;
  document.getElementById = (id) => track(origGet(id));

  // `prompt` is a global in a browser, not a method on `document`. Mutable so a
  // check can override the answer the demo's exemption dialog receives; the
  // demo calls the bare global, not a method on document.
  let answer = opts.prompt;
  const promptFn = () => (answer === undefined ? "test reason" : answer);
  const sandbox = {
    document,
    window: { setTimeout: () => {}, isSecureContext: false },
    console,
    prompt: promptFn,
    alert: () => {},
    confirm: () => true,
  };
  sandbox.globalThis = sandbox;
  document.prompt = promptFn;

  vm.createContext(sandbox);
  vm.runInContext(js, sandbox, { filename: file });

  const deep = (n) => !n ? "" : ((n.innerHTML || n.textContent || "") + " "
    + (n._children || []).map(deep).join(" ")).trim();

  return {
    els,
    buttons,
    text: (id) => deep(els[id]),
    click(labelPrefix) {
      const hit = buttons.find((b) =>
        (b.textContent || b._text || "").indexOf(labelPrefix) === 0);
      if (!hit) {
        throw new Error("no button starts with " + JSON.stringify(labelPrefix)
          + "; have: " + buttons.map((b) => b.textContent || b._text).join(" | "));
      }
      hit.onclick();
      return hit;
    },
    // Precise targeting: a demo's controls carry `data-action`/`data-field`, so
    // a check names the control it means instead of relying on label text and
    // render order. Stale buttons survive in `buttons` across renders, so the
    // match takes the last one, which is the one on screen.
    act(action, field) {
      const hits = buttons.filter((b) =>
        b._attrs["data-action"] === action && (!field || b._attrs["data-field"] === field));
      if (!hits.length) {
        throw new Error("no button with data-action=" + action
          + (field ? " data-field=" + field : "")
          + "; have: " + buttons.map((b) => b._attrs["data-action"]).filter(Boolean).join(","));
      }
      const hit = hits[hits.length - 1];
      if (typeof hit.onclick !== "function") throw new Error("button has no handler: " + action);
      hit.onclick();
      return hit;
    },
    setPrompt(fn) { answer = fn(); },
    clickAll() {
      // Progressive demos reveal controls as state advances, so a snapshot of
      // `buttons` clicks only the first screen. Iterate until a round adds
      // nothing new — but cap the TOTAL, because a demo that re-renders its
      // controls on every state change creates fresh button objects each time
      // and an unbounded loop over a growing array exhausts the heap.
      const done = new Set();
      let total = 0;
      for (let round = 0; round < 8 && total < 200; round++) {
        let thisRound = 0;
        for (const b of buttons.slice()) {
          if (done.has(b) || typeof b.onclick !== "function") continue;
          done.add(b);
          b.onclick();
          thisRound++;
          total++;
          if (total >= 200) break;
        }
        if (thisRound === 0) break;
      }
    },
  };
}

module.exports = { load };
