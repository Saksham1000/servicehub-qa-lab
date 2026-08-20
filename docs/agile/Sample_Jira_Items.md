# Sample GitHub-Compatible Jira-Style Items
This demonstrates artifact structure; the project does not claim paid Jira or Zephyr use.

## Epic SH-1 — Reliable Appointment Management
Enable customers and providers to coordinate services without conflicts or data leakage.

## Story SH-12 — Book an available provider
**As a** customer, **I want** to book an available provider **so that** I receive a service at my preferred time.

Acceptance criteria: authenticated customers can choose an active service and advertised future slot; successful creation returns 201/confirmed and persists; unavailable/past slots fail; a provider cannot have overlapping active bookings; other customers cannot modify it. Requirements: REQ-BOOK-001–003. Tests: TC-BOOK-001–018.

## QA subtask SH-13
Design positive, boundary, conflict, ownership, API-to-DB, and responsive cases; automate critical booking/cancellation; update RTM; attach real report evidence.

## Bug SH-21
**Title:** Uppercase service search returns no results. **Requirement:** REQ-SVC-001. **Expected:** case-insensitive match. **Actual:** no match in bug mode. **Severity/Priority:** Medium/P2. **Acceptance for fix:** TC-SVC-003 and related API/UI regression pass.
