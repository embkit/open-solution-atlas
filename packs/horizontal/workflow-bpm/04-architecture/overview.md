# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design. BPMN 2.0 is the
> modelling vocabulary; **no conformance profile is claimed** (BR-12, ADR-0001).
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — the three layers that must not blur

```
   ┌───────────────────────────────────────────────────────────────┐
   │  DEFINITION  (governed, versioned)                            │
   │  ProcessDefinition → DefinitionVersion                        │
   │  gateways · timers · forms · the VOCABULARY SEMANTICS         │
   │  publish records the IN-FLIGHT TREATMENT                      │
   └───────────────────────────┬───────────────────────────────────┘
                               │ instantiate (pins the version)
                               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  RUNTIME  (instances pinned to a version)                     │
   │  ProcessInstance · Token · InstanceEvent                       │
   │  state = fold(events)  — replayable, never rewritten          │
   └───────────────────────────┬───────────────────────────────────┘
                               │ spawns
                               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  WORK ITEMS  (the vocabulary, defined)                        │
   │  assign · claim · transfer · delegate ·                       │
   │  会签 · 或签 · 加签 · 退回 · 撤回 · add-comment                │
   │  each pattern REQUIRES a declared CompletionPolicy             │
   └───────────────────────────┬───────────────────────────────────┘
                               │ resolves
                               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  PARTICIPANTS  (role + business scope, never a name)          │
   │  Participant · Role · Scope · Delegation (scoped, expiring)    │
   │  org changes affect FUTURE resolution, never running instances  │
   └───────────────────────────────────────────────────────────────┘

   ┌───────────────────────────────────────────────────────────────┐
   │  CN VARIANT (labelled — core runs without it)                  │
   │  公文 · 文号 (gapless, auditable) · 电子签章 (valid at signing) │
   └───────────────────────────────────────────────────────────────┘
```

## The two boundaries that must stay explicit

### 1. Definition → Runtime

A publication does not touch a running instance. The in-flight treatment — finish
on old version, migrate, or terminate — is **recorded with the publication**
(BR-03, constraint 2), because the alternative default is whichever one the engine
happens to do.

### 2. Core → CN variant

公文, 文号 and 电子签章 live in a labelled variant (BR-11). The core must operate
with them absent (FR-028), which is how the isolation is proved rather than
asserted. A deployment outside the CN regime takes the core without them.

## Deployment view

```
                    ┌──────────────────────────────┐
                    │  authoring (modeller · forms)  │
                    └───────────────┬──────────────┘
                                    │ publish
   ┌──────────────────┐   ┌─────────▼──────────┐   ┌──────────────────┐
   │  org source      │──▶│  Definition store  │──▶│  Participant &   │
   │  (HR / IAM)      │   │  (versioned)       │   │  delegation       │
   └──────────────────┘   └─────────┬──────────┘   └──────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
   ┌────────────────────┐ ┌───────────────────┐ ┌───────────────────┐
   │ Runtime store      │ │ Event log         │ │ Work item inbox   │
   │ (instances pinned  │ │ (append-only;     │ │ (role/scope       │
   │  to versions)      │ │  replayable)      │ │  resolved)        │
   └─────────┬──────────┘ └───────────────────┘ └───────────────────┘
             │
             ▼
   ┌───────────────────────────────────────────────────────────┐
   │  Timer service — reminders, deadlines, escalation          │
   │  (trigger + action + authority, all three declared)       │
   └───────────────────────────────────────────────────────────┘
             │
             ▼
   ┌───────────────────────────────────────────────────────────┐
   │  Documents & artefacts — authority attached, seal variant │
   │  Retention per class                                       │
   └───────────────────────────────────────────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Definition store** | versioned, immutable once published | a running instance's meaning must not move (BR-02, BR-03) |
| **Event log** | append-only, separate from the instance row | state = fold(events); a mutated current-state field is how replayability silently dies |
| **Participant resolution** | role-and-scope, org-source-driven | approval breaks silently when someone changes jobs (BR-04) |
| **Timer service** | a separate service with declared authority | escalation without a recorded authority is how a control becomes an unreviewed automatic act |
| **CN variant** | a labelled module | the core must run without it (FR-028) |

## What this architecture deliberately does not do

- No in-place edit of a published definition version (BR-02).
- No retroactive application of a new version to in-flight instances (BR-03).
- No user name as a participant in a definition (BR-04).
- No multi-participant pattern without a declared completion policy (BR-05).
- No rewrite of instance history (BR-07).
- No 公文 / 文号 / 电子签章 behaviour in the core (BR-11).
- No claimed BPMN maturity, engine conformance profile or DMN target (BR-12).