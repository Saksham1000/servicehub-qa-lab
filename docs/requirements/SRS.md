# ServiceHub Software Requirements Specification

## Overview and objective
ServiceHub is a personal QA portfolio application for booking appointments with service providers. It provides a realistic, testable boundary across a responsive React client, REST and GraphQL APIs, authorization, and a relational database. The objective is reliable self-service booking with protected customer, provider, and administrator operations.

## Roles
- **Customer:** register, authenticate, discover services/providers, book, view, reschedule, and cancel own appointments.
- **Provider:** authenticate, manage own availability, view own appointments, and mark them completed.
- **Administrator:** view users/bookings and create, update, or deactivate services.

## Functional requirements and acceptance criteria
| ID | Requirement | Acceptance criteria |
|---|---|---|
| REQ-AUTH-001 | Customer registration | Valid unique email and password with 8+ characters, a letter, and a number creates a customer without a session and instructs the user to sign in; duplicates return 409. |
| REQ-AUTH-002 | Login/logout | Valid credentials issue JWT; invalid credentials return 401; client logout removes its token. |
| REQ-AUTH-003 | Protected access | Missing/invalid tokens return 401 and wrong roles return 403. |
| REQ-SVC-001 | Service discovery | Only active services are listed; name search is case-insensitive; category filtering is supported. |
| REQ-SVC-002 | Provider discovery | Provider identity, biography, and future free availability are returned; invalid IDs return 404. |
| REQ-BOOK-001 | Create booking | A customer may book an existing active service/provider at a future advertised slot; response is 201 and is persisted. |
| REQ-BOOK-002 | Prevent conflicts | Past, missing, unavailable, and already occupied slots are rejected; a provider has at most one active booking per instant. |
| REQ-BOOK-003 | Manage own booking | Customer may view/reschedule/cancel only their bookings; cancellation changes status and releases the slot. |
| REQ-PROV-001 | Availability | Provider may create valid future availability for themself; duplicates and invalid ranges are rejected. |
| REQ-PROV-002 | Provider appointments | Provider sees only their appointments and may mark only those appointments completed. |
| REQ-ADMIN-001 | Service administration | Admin may create/update/deactivate services; customers/providers receive 403. |
| REQ-ADMIN-002 | Operational visibility | Admin may view users and all bookings; non-admins receive 403. |
| REQ-API-001 | API contract | Validation errors use 422, unauthenticated 401, forbidden 403, missing 404, conflict 409, and successful CRUD appropriate 2xx codes with JSON contracts. |
| REQ-GQL-001 | GraphQL discovery | Queries expose services/providers and variables/filtering; invalid fields produce GraphQL errors. |
| REQ-GQL-002 | Protected GraphQL | Appointments require a valid JWT and are scoped to the caller's role. |
| REQ-DB-001 | Data integrity | Booking foreign keys resolve, allowed statuses are enforced by application behavior, and cancellation persists. |
| REQ-UI-001 | Responsive access | Login, navigation, search, booking, and appointments remain usable at desktop, tablet, and 360px+ mobile widths. |
| REQ-PERF-001 | Local performance target | In a controlled local baseline, common API p95 target is <800 ms and failure rate target is <1%; actual results must be measured. |

## Business rules
All required fields are validated. Email comparison and service search are case-insensitive. Appointment timestamps must be future times matching provider availability. Active means `confirmed` or `completed`; cancelled slots are reusable. Object ownership is checked server-side and never trusted from client data. Admin permissions are deny-by-default. Invalid IDs never silently create related data. Database commits are atomic.

## Non-functional requirements
Security: hashed passwords, expiring signed JWTs, no repository secrets, role/ownership enforcement. Reliability: health endpoint, transactional writes, deterministic errors. Maintainability: modular backend, Page Objects, fixtures, configuration via environment. Portability: Docker Compose and Chrome/Firefox selection. Usability: keyboard-operable controls and responsive layout. Observability: terminal, HTML, JUnit, logging, and failure screenshots.

## Assumptions and constraints
The laboratory uses one timezone as supplied by clients; production would normalize UTC and display user zones. Availability uses exact start times and one-hour seed slots. MySQL is production-like; SQLite enables fast isolated backend checks. JWT revocation, payments, notifications, native mobile apps, provider onboarding, file uploads, and calendar integration are out of scope. Responsive browser checks are not native Appium tests.

## QA demonstration mode
`QA_BUG_MODE=true` intentionally enables documented laboratory defects. It is false by default and must never be enabled in a real deployment. See defect reports for detection paths.

