# 08-quality · Test Strategy (template)

> TEMPLATE STUB — levels, coverage targets, test data, performance/failure
> program that prove the NFRs and CTLs.

## Levels & coverage targets

| Level | What it proves | Gate |
|---|---|---|
| Unit | domain invariants (BR-xx) | coverage target |
| Contract | API conformance, error shape, idempotency | every endpoint |
| Integration | end-to-end flow + failure injections | happy + failures |
| State-machine | SM-xx transitions incl. illegal rejected | all transitions |
| Performance | AC-N* profiles | regression tracked |
| Security / control | RBAC negatives, audit reconstruction | CTL-xx evidence |

## Test data

_Synthetic corpora only; controllable clock for time-dependent rules._

## Environments & promotion

```
PR → fast suite; merge → integration+security; release → performance+DR
```
