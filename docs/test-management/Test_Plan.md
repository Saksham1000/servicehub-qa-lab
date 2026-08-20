# ServiceHub Master Test Plan

## Introduction, objectives, and scope
This plan controls quality evaluation for ServiceHub 1.0. The objective is evidence that critical booking, identity, authorization, persistence, and discovery behavior meets the SRS. In scope: functional/negative/boundary, integration, UI, REST, GraphQL, database, regression, performance baseline, security-oriented authorization, cross-browser, and responsive web testing. Out of scope: penetration certification, payment, email/SMS, native apps, accessibility certification, disaster recovery, and production endurance.

## Approach and levels
Static review validates requirements, acceptance criteria, testability, and traceability. Component/API tests isolate rules; integration tests cross API/database; system tests exercise browser workflows; release regression combines risk-weighted suites. Positive equivalence classes are paired with invalid/missing/unauthorized classes and time/password boundaries. API checks validate status, body, schema, side effects, and error shape—not only 200. Database checks are read-only except data created through the API. Locust reads common resources and avoids destructive booking load by default.

## Suites
- **Smoke:** health, registration/login, services, booking journey, basic GraphQL.
- **Targeted:** changed module plus upstream/downstream contracts.
- **Full regression:** all API, GraphQL, database, Chrome UI, responsive, and negative tests.
- **Release:** full regression plus Firefox spot-check, Postman/Newman, performance sanity, migration and checklist review.

## Entry criteria
Approved SRS/acceptance criteria; deployable build; environment healthy; migration complete; known test accounts/data; no blocker preventing testing; secrets supplied outside Git.

## Exit criteria and recommendation
All critical/high requirements covered; smoke 100% pass; no open Critical or High defect affecting release scope; full regression results reviewed; authorization, persistence, and rollback checks pass; Medium residual risk accepted by owner; performance sanity meets project targets or has approved exception. Any security boundary breach, booking loss/double booking, failing smoke, or unassessed migration means **No-Go**. Evidence gaps mean **Conditional/No-Go**, never an invented pass.

## Environment and compatibility
Local/CI: Docker Compose, React/Nginx, FastAPI, MySQL 8.4. Primary browser is current stable headless Chrome; Firefox is release spot-check. Responsive viewports: 1440×900, 1024×768, 768×1024, 390×844, 360×800. API base and credentials are environment-driven.

## Test data strategy
Generate unique customer emails, seed stable admin/provider/services, use future advertised slots, and avoid test-order dependencies. Tests create their own customers/bookings and clean through disposable databases/containers. Never use real personal data. QA bug mode uses a separate run.

## Defect management
Record ID, requirement, environment/build, reproducible steps, expected/actual, severity, priority, evidence, owner/status, and regression test. Lifecycle: New → Triaged → Assigned → Fixed → Retest → Closed/Reopened; Deferred requires explicit risk acceptance.

| Severity | Definition |
|---|---|
| Critical | Security/data-loss or system unavailable with no workaround. |
| High | Critical business journey broken or integrity risk; limited workaround. |
| Medium | Significant non-critical function degraded; workaround exists. |
| Low | Cosmetic/minor usability or low-impact inconsistency. |

| Priority | Scheduling meaning |
|---|---|
| P0 | Immediate release blocker. |
| P1 | Fix before release. |
| P2 | Plan promptly; may release with accepted risk. |
| P3 | Backlog candidate. |

## Deliverables, metrics, risks
Deliverables: SRS, this plan, CSV cases, RTM, automation/report configs, defect reports, risk assessment, summary, and release checklist. Report execution progress, pass rate, requirement coverage, automation coverage, defect distribution/reopen/leakage, and failed regressions using actual evidence only. Top risks are authorization leakage, double booking, cancellation inconsistency, time boundaries, and false-active services. Mitigations include server authorization, negative tests, database reconciliation, exact boundary cases, CI smoke gates, isolated data, and QA bug-mode mutation checks.
