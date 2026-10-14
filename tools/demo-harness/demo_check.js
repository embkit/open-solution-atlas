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

if (slug.indexOf("enterprise-bi") >= 0) {
  // An artifact pins a model version, and certification is computed. The
  // temptation the demo exists to refuse is declaring a dashboard certified.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // publishing a new definition version must not move the artifact
  d.act("publish-v4");
  check("publishing a new version leaves every invariant held",
    d.text("violations").indexOf("sev-1") < 0);
  check("the artifact still renders the version it is pinned to",
    d.text("artifact").indexOf("v3") >= 0);

  // versions are append-only
  d.act("edit-v3-inplace");
  check("rewriting a published version trips ADR-0003",
    d.text("violations").indexOf("ADR-0003") >= 0);

  // silently following latest
  d.act("repoint-latest");
  check("following latest without review trips BR-06",
    d.text("violations").indexOf("BR-06") >= 0);

  // there is no certified_by field to write
  d.act("declare-certified");
  check("declaring certification trips BR-07",
    d.text("violations").indexOf("BR-07") >= 0);
  check("…and BR-05, because a certified artifact without provenance is not one",
    d.text("violations").indexOf("BR-05") >= 0);
  check("the panel says there is no field to write",
    d.text("certNote").indexOf("可以写入的字段") >= 0);

  // a review with a reason is what makes it certified
  d.act("request-review");
  check("a review decision with a reason clears BR-07",
    d.text("violations").indexOf("BR-07") < 0);
  check("…and the state is computed, not declared",
    d.text("artifact").indexOf("计算") >= 0);

  // a rejection with no reason supports nothing
  d.act("reject-no-reason");
  check("a rejection with no reason trips BR-07 again",
    d.text("violations").indexOf("BR-07") >= 0);

  // embeds resolve through the semantic layer
  d.act("embed-direct");
  check("an embed reading the table directly trips BR-08",
    d.text("violations").indexOf("BR-08") >= 0);
  d.act("embed-via-model");
  check("…and an embed through the model does not clear it, because the first one stands",
    d.text("violations").indexOf("BR-08") >= 0);
}

if (slug.indexOf("iam-platform") >= 0) {
  // Every control here is one an operator is under pressure to wave through.
  // Each must refuse, and the refusal must be a policy decision with a reason.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // an elevation with a lifetime, and the auto-revoke that follows from it
  d.act("elevate-1h");
  check("a time-limited elevation holds every invariant",
    d.text("violations").indexOf("sev-1") < 0);
  d.act("advance-time");
  check("the elevation is auto-revoked at expiry",
    d.text("elev").indexOf("\u65e0") >= 0);

  // an elevation with no lifetime is illegal
  d.act("elevate-open");
  check("an open-ended elevation trips BR-05",
    d.text("violations").indexOf("BR-05") >= 0);

  // segregation of duties, caught at write time
  d.act("grant-conflict");
  check("a conflicting role pair trips BR-03",
    d.text("violations").indexOf("BR-03") >= 0);
  d.act("grant-with-exception");
  check("a recorded exception clears BR-03",
    d.text("violations").indexOf("BR-03") < 0);

  // deny-overrides
  d.act("add-deny");
  d.act("evaluate");
  check("deny wins even with permits present",
    d.text("decisionNote").indexOf("deny") >= 0);
  d.act("evaluate-first-match");
  check("first-match semantics let a permit through past a deny",
    d.text("violations").indexOf("BR-14") >= 0);

  // a cross-realm read is impossible, not filtered
  d.act("read-cross-realm");
  check("reading another realm trips BR-07",
    d.text("violations").indexOf("BR-07") >= 0);

  // a federated subject has no local credential
  d.act("set-local-password");
  check("a local password on a federated subject trips BR-15",
    d.text("violations").indexOf("BR-15") >= 0);

  // overdue access review
  d.act("advance-time");
  d.act("advance-time");
  check("an overdue access review trips BR-04",
    d.text("violations").indexOf("BR-04") >= 0);
}

if (slug.indexOf("/mes/") >= 0) {
  // Every step here is one a shop floor under schedule pressure skips. Each is
  // refused, and the refusal is a constraint rather than a reminder.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // routing precedence
  d.act("start-op20");
  check("starting an operation before its predecessor trips BR-02",
    d.text("violations").indexOf("BR-02") >= 0);
  d.act("finish-op10");
  check("completing the predecessor clears BR-02",
    d.text("violations").indexOf("BR-02") < 0);

  // the blocking inspection gate
  d.act("gate-skip");
  check("starting with a blocking inspection outstanding trips BR-05",
    d.text("violations").indexOf("BR-05") >= 0);
  d.act("gate-pass");
  check("passing the inspection clears BR-05",
    d.text("violations").indexOf("BR-05") < 0);

  // shop-floor material never goes negative
  d.act("consume-ok");
  check("consuming within the lot balance holds every invariant",
    d.text("violations").indexOf("sev-1") < 0);
  d.act("consume-over", "12");
  check("consuming beyond the lot balance trips BR-04",
    d.text("violations").indexOf("BR-04") >= 0);
  check("the lot is shown negative rather than clamped",
    d.text("material").indexOf("-") >= 0);
  d.act("receive-lot");
  check("receiving stock clears BR-04", d.text("violations").indexOf("BR-04") < 0);

  // genealogy completeness
  d.act("close-unit");
  check("closing a unit without a complete genealogy trips BR-06",
    d.text("violations").indexOf("BR-06") >= 0);
  d.act("scan", "LOT-STEEL-88");
  check("one component is not enough", d.text("violations").indexOf("BR-06") >= 0);
  d.act("scan", "LOT-BOLT-14");
  check("the dossier resolving to every key component clears BR-06",
    d.text("violations").indexOf("BR-06") < 0);

  // OEE from validated state only
  d.act("enter-oee");
  check("a hand-entered OEE trips BR-09",
    d.text("violations").indexOf("BR-09") >= 0);
}

if (slug.indexOf("/tms/") >= 0) {
  // "Get the truck out, the POD can follow" is the most ordinary sentence in
  // this business. Each step below is refused, and the money follows the frozen
  // snapshot rather than the current contract.
  check("starts with no violation", d.text("violations").indexOf("sev-1") < 0);

  // dispatch before the tender is accepted
  d.act("dispatch-before-tender");
  check("dispatching with no tender trips BR-03",
    d.text("violations").indexOf("BR-03") >= 0);
  d.act("tender-accept");
  check("accepting the tender freezes the rate snapshot",
    d.text("money").indexOf("2025-Q4") >= 0);
  d.act("dispatch");
  check("…and clears BR-03", d.text("violations").indexOf("BR-03") < 0);

  // delivered without a captured proof
  d.act("deliver-without-pod");
  check("reaching DELIVERED with no POD trips BR-06",
    d.text("violations").indexOf("BR-06") >= 0);
  d.act("capture-pod");
  check("capturing the POD clears BR-06",
    d.text("violations").indexOf("BR-06") < 0);

  // the invoice is priced from the frozen snapshot, not the current contract
  d.act("publish-contract");
  d.act("invoice-from-latest");
  check("pricing an invoice from a newer contract trips BR-04",
    d.text("violations").indexOf("BR-04") >= 0);
  d.act("invoice-from-snapshot");
  check("pricing from the snapshot clears BR-04",
    d.text("violations").indexOf("BR-04") < 0);

  // three-way match
  d.act("invoice-mismatch");
  check("an invoice that does not match trips BR-05",
    d.text("violations").indexOf("BR-05") >= 0);
  d.act("invoice-match");
  check("a matching invoice clears BR-05",
    d.text("violations").indexOf("BR-05") < 0);

  // dangerous goods are validated, not re-implemented
  d.act("dg-unknown");
  check("an unknown UN number trips BR-07",
    d.text("violations").indexOf("BR-07") >= 0);
  d.act("dg-validate");
  check("validating against the reference dataset clears BR-07",
    d.text("violations").indexOf("BR-07") < 0);
}

console.log(failures ? "\nFAILURES: " + failures : "\nsemantic checks passed");
process.exit(failures ? 1 : 0);
