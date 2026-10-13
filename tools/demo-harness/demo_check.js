/* Smoke and semantic checks for the bespoke demos.
 *
 * Usage: node tools/demo-harness/demo_check.js <demo.html> [smoke|semantic]
 *
 *   smoke    — it loads, and every control it renders can be clicked.
 *   semantic — it *fails correctly*, which is the whole point of these demos:
 *              each check asserts that the invariant panel lights up on the
 *              action the pack's rule is about. A demo whose failure path is
 *              decorative is a demo that teaches the wrong thing.
 *
 * Driven by tests/test_demo_harness.py so CI runs it; run it by hand while
 * working on a demo.
 */
const { load } = require("./demo_stub");

const file = process.argv[2];
const mode = process.argv[3] || "semantic";
let failures = 0;
const check = (name, cond) => {
  if (cond) console.log("ok:", name);
  else { console.error("FAIL:", name); failures++; }
};

let d;
try {
  d = load(file);
} catch (e) {
  console.error("THREW ON LOAD:", e.message);
  process.exit(1);
}
check("loads without throwing", true);
check("renders at least one button", d.buttons.length > 0);

const slug = file.replace(/\\/g, "/");

if (mode === "smoke") {
  let thrown = null;
  try { d.clickAll(); } catch (e) { thrown = e; }
  check("every button is clickable", !thrown);
  if (thrown) console.error("   ", thrown.message);
  console.log(failures ? "\nFAILURES: " + failures
    : "\n" + d.buttons.length + " buttons, smoke passed");
  process.exit(failures ? 1 : 0);
}

/* ------------------------------------------------------------------ *
 * Semantic checks — per demo, the rule must actually fire
 * ------------------------------------------------------------------ */

if (slug.indexOf("workflow-bpm") >= 0) {
  // 会签 is a multi-participant pattern, so it REQUIRES a declared completion
  // policy (BR-05 / FR-013 / constraint 7). Without one, the panel must say so.
  const cs = d.buttons.find((b) => (b.textContent || "") === "会签");
  check("会签 button exists", !!cs);
  if (cs) cs.onclick();
  d.els.policy.value = "";
  d.els.policy.onchange();
  check("会签 without a policy trips FR-013", d.text("violations").indexOf("FR-013") >= 0);
  check("…and NFR-007", d.text("violations").indexOf("NFR-007") >= 0);
  check("…and the constraint-7 note is shown", /REQUIRES/.test(d.text("policyNote")));
  d.els.policy.value = "unanimous";
  d.els.policy.onchange();
  check("declaring a policy clears them", d.text("violations").indexOf("FR-013") < 0);
}

if (slug.indexOf("one-stop-service") >= 0) {
  // Article 7 is per field, and its failure mode is the system being helpful.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  d.act("lookup-ok", "name");
  check("a successful lookup pre-fills rather than asking",
    d.text("render").indexOf("已回填") >= 0);

  d.act("lookup-fail", "id-number");
  check("a failed lookup with no alternative trips FR-013",
    d.text("violations").indexOf("FR-013") >= 0);

  d.setPrompt(() => "");
  d.act("exempt", "marital");
  check("an empty exemption reason trips NFR-003",
    d.text("violations").indexOf("NFR-003") >= 0);

  d.act("demand", "marital");
  check("demanding an obtainable field trips FR-011",
    d.text("violations").indexOf("FR-011") >= 0);
  check("…and NFR-001", d.text("violations").indexOf("NFR-001") >= 0);
  check("…and the applicant view shows sev-1",
    d.text("applicant").indexOf("sev-1") >= 0);
  check("the log records the demand", d.text("log").indexOf("DEMAND") >= 0);

  d.act("demand", "marital");
  check("withdrawing the demand clears FR-011",
    d.text("violations").indexOf("FR-011") < 0);
}

if (slug.indexOf("data-exchange") >= 0) {
  // The loop is a cycle: no transfer without a live, purpose-matching grant,
  // every share walks back to an approval, and revocation is measured by the
  // lead time until access is actually removed.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // a transfer needs an approval to exist at all, but no grant yet — which is
  // the unaccountable case: data left with nothing authorising it
  d.act("register");
  d.els.purpose.value = "social-security";
  d.act("request");
  d.act("transfer-ok");
  check("a transfer with no grant trips BR-08",
    d.text("violations").indexOf("BR-08") >= 0);
  check("…and FR-018, because the share cannot walk back to an approval",
    d.text("violations").indexOf("FR-018") >= 0);
  check("the loop is marked broken", d.text("lineage").indexOf("broken") >= 0);

  // create the grant, then transfer again: the loop closes
  d.act("grant");
  d.act("transfer-ok");
  check("a governed transfer closes the loop",
    d.text("lineage").indexOf("closed") >= 0);

  // a grant exists but does not cover this transfer's purpose
  d.act("transfer-mismatch");
  check("a purpose-mismatched transfer is not a grant for it",
    d.text("violations").indexOf("BR-08") >= 0);

  // revoking records the act; the control is the lead time until access goes
  d.act("revoke");
  check("recording a revocation while access persists trips BR-07",
    d.text("violations").indexOf("BR-07") >= 0);
  check("…and the window is named as the defect",
    d.text("revokeNote").indexOf("访问尚未移除") >= 0);

  d.act("remove-access");
  check("removing access at every channel clears BR-07",
    d.text("violations").indexOf("BR-07") < 0);
}

console.log(failures ? "\nFAILURES: " + failures : "\nsemantic checks passed");
process.exit(failures ? 1 : 0);
