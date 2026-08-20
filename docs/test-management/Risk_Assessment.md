# Risk-Based Test Assessment
Score = Probability (1–5) × Impact (1–5).

| Risk | P | I | Score | Response |
|---|---:|---:|---:|---|
| Unauthorized appointment access | 3 | 5 | 15 | Ownership/API/GraphQL negative tests; release blocker |
| Provider double booking | 3 | 5 | 15 | Conflict, concurrency, and SQL grouping checks |
| Lost or inconsistent cancellation | 3 | 5 | 15 | API-to-DB reconciliation and slot-reuse regression |
| Date/time boundary error | 4 | 4 | 16 | Past/now/future exact boundaries; future UTC improvement |
| Inactive service remains bookable | 3 | 4 | 12 | Catalog visibility plus booking validation review |
| Orphan relational data | 2 | 5 | 10 | FK/LEFT JOIN integrity query |
| Mobile control unusable | 3 | 3 | 9 | Five responsive viewports and critical journey |
| Search mismatch | 3 | 2 | 6 | Case/partial/no-result equivalence classes |

Time and authorization have the highest priority. Risk is reassessed after requirements, schema, authentication, or scheduling changes.
