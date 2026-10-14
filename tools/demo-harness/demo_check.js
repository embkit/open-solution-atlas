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

if (slug.indexOf("/wms/") >= 0) {
  // Stock is a fold of the event stream, not a number you can edit. Two
  // different repairs, and conflating them is the point of the demo: a wrong
  // *fact* is reversed by a compensating event; a wrong *projection* is rebuilt
  // from the stream. Neither is an UPDATE.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // the legitimate path holds every invariant
  d.act("receive");
  d.act("reserve-ok");
  d.act("deduct");
  check("receiving, reserving and picking within availability holds everything",
    d.text("violations").indexOf("sev-1") < 0);

  // a reservation with no lifetime
  d.act("reserve-noexp");
  check("a reservation with no expiry trips BR-05",
    d.text("violations").indexOf("BR-05") >= 0);
  d.act("release");
  check("expiry release clears BR-05", d.text("violations").indexOf("BR-05") < 0);

  // a change that bypasses the event stream
  d.act("edit-direct");
  check("editing the quantity off-stream trips BR-14",
    d.text("violations").indexOf("BR-14") >= 0);
  check("…and ADR-0002", d.text("violations").indexOf("ADR-0002") >= 0);
  check("the projection is shown to diverge from the fold",
    d.text("foldNote").indexOf("偏离") >= 0);
  d.act("rebuild");
  check("rebuilding the projection from the stream clears it",
    d.text("violations").indexOf("BR-14") < 0);

  // a deduction beyond available
  d.act("deduct-over");
  check("a deduction beyond available trips BR-02",
    d.text("violations").indexOf("BR-02") >= 0);
  check("…and BR-01, because the buckets no longer reconcile",
    d.text("violations").indexOf("BR-01") >= 0);
  check("the bucket is shown negative, not clamped to zero",
    d.text("buckets").indexOf("-") >= 0);

  // the fact is wrong, so only a compensating event reverses it
  d.els.reason.value = "mis-pick";
  d.act("compensate");
  check("a compensating event with a reason clears BR-02",
    d.text("violations").indexOf("BR-02") < 0);
  check("…and the buckets reconcile again",
    d.text("violations").indexOf("BR-01") < 0);
}

if (slug.indexOf("his-emr") >= 0) {
  // A signed clinical document is evidence. Corrections are additive, a
  // retraction keeps the original, and no billing artefact may edit it. The
  // substitute for the edit is an addendum — so the demo has to show both the
  // forbidden path and the permitted one.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // the permitted repair: an addendum that references the original
  d.act("addendum");
  check("an addendum leaves every invariant held",
    d.text("violations").indexOf("sev-1") < 0);
  check("…and the current text is the original plus the addendum",
    d.text("currentNote").indexOf("追加更正") >= 0);

  // the forbidden repair: edit the signed document in place
  d.act("edit-inplace");
  check("editing a signed document in place trips BR-07",
    d.text("violations").indexOf("BR-07") >= 0);
  check("…and ADR-0002, because the signature is the evidence",
    d.text("violations").indexOf("ADR-0002") >= 0);
  check("the divergence is shown rather than described",
    d.text("currentNote").indexOf("不一致") >= 0);

  // a retraction keeps the original
  d.act("retract-delete");
  check("deleting the original on retraction trips BR-08",
    d.text("violations").indexOf("BR-08") >= 0);
  check("the original is shown as gone, which is the defect",
    d.text("original").indexOf("已被删除") >= 0);

  // coded facts carry the version they were recorded under
  d.act("remap-inplace");
  check("rewriting a mapping in place trips BR-11",
    d.text("violations").indexOf("BR-11") >= 0);
  d.act("new-mapping-version");
  check("a new mapping version clears BR-11",
    d.text("violations").indexOf("BR-11") < 0);

  // the billing pressure
  d.act("bill-adjust");
  check("billing editing the clinical record trips BR-12",
    d.text("violations").indexOf("BR-12") >= 0);
}

console.log(failures ? "\nFAILURES: " + failures : "\nsemantic checks passed");
process.exit(failures ? 1 : 0);
