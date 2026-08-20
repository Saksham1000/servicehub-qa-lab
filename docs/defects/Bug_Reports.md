# QA Demonstration Defect Reports
These are intentional laboratory mutations activated only with `QA_BUG_MODE=true`. â€œActualâ€ describes that mode, not the default application. Evidence should be attached from a real demo run; none is fabricated here.

## BUG-DEMO-001 â€” Provider can be double-booked
- **Requirement:** REQ-BOOK-002 Â· **Environment:** local bug mode Â· **Severity/Priority:** High/P1 Â· **Status:** Demonstration mutation
- **Preconditions:** two customers; one free provider slot.
- **Steps:** enable bug mode; customer A books slot; customer B submits identical provider/time.
- **Expected:** second request is 409; one active record. **Actual:** the normal conflict guard is bypassed and the second active booking is accepted.
- **Evidence:** To capture from API response and SQL duplicate query. **Regression:** TC-BOOK-006 / `test_no_active_provider_double_booking`.

## BUG-DEMO-002 â€” Cancelled slot not released
- **Requirement:** REQ-BOOK-003 Â· **Severity/Priority:** Medium/P1 Â· **Status:** Demonstration mutation
- **Steps:** book then cancel; request availability; attempt same slot.
- **Expected:** slot available and re-bookable. **Actual:** cancelled time remains excluded from advertised availability.
- **Evidence:** Not captured. **Regression:** TC-BOOK-016 / `test_booking_cancel_releases_slot`.

## BUG-DEMO-003 â€” Customer can modify another customer's booking
- **Requirement:** REQ-BOOK-003 Â· **Severity/Priority:** Critical/P0 Â· **Status:** Demonstration mutation
- **Steps:** create booking as B; enable bug mode; authenticate A; PATCH/DELETE B's ID.
- **Expected:** 403. **Actual:** ownership check accepts customer A.
- **Evidence:** To capture in a bug-mode run. **Regression:** TC-BOOK-014 and TC-BOOK-017.

## BUG-DEMO-004 â€” Admin authorization bypass
- **Requirement:** REQ-ADMIN-001/002 Â· **Severity/Priority:** Critical/P0 Â· **Status:** Demonstration mutation
- **Expected:** customers receive 403. **Actual:** the bug-mode authorization dependency accepts a regular customer for admin routes.
- **Evidence:** Not captured. **Regression:** TC-ADMIN-005/008.

## BUG-DEMO-005 â€” Search becomes case-sensitive
- **Requirement:** REQ-SVC-001 Â· **Severity/Priority:** Medium/P2 Â· **Status:** Demonstration mutation
- **Steps:** enable bug mode; search `MASSAGE`.
- **Expected:** Massage returned. **Actual:** no match due to case-sensitive comparison.
- **Evidence:** To capture from response/UI. **Regression:** TC-SVC-003 / `test_search_is_case_insensitive`.

Bug mode is educational, must remain false by default, and is not proof that these defects were discovered in a client product.

