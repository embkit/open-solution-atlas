# 06-contracts · API Overview (template)

> TEMPLATE STUB — paths/field names/idempotency composition are pack
> conventions, not standards (SOURCES §4). Promises must stay honest to what
> 02-requirements specifies.

## Service inventory

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/…` | bearer · role | _purpose_ | FR-001 |

## Cross-cutting contract rules

1. **Idempotency:** retryable POSTs take an `Idempotency-Key`.
2. **Errors:** RFC 9457 `application/problem+json`.
3. **Append-only facts:** corrections are compensating events (if the pack
   says so — cite the ADR).
4. **Immutability / SoD / isolation:** _pack-specific invariants by ID._

Full OpenAPI 3.1 contract: [`api/openapi.yaml`](./api/openapi.yaml).
