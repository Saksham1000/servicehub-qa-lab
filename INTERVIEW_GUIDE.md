# ServiceHub QA Interview Guide
Use these as reasoning prompts, not a script.

1. **What is this project?** A personal end-to-end QA laboratory around a realistic service-booking system, spanning requirements through release evidence.
2. **Why booking?** It contains identity, roles, time boundaries, ownership, concurrency, and persistence—high-value QA risks.
3. **How did you select tests?** I scored impact/probability, prioritized authorization and double booking, then covered equivalence, negative, and boundaries.
4. **What is the highest risk?** Unauthorized data access and active provider conflicts because their impact is severe.
5. **Why Selenium?** It validates real browser integration and critical user journeys; API tests cover more combinations cheaply.
6. **What is POM?** Page classes own locators/actions; tests express intent and UI maintenance stays localized.
7. **What does Pytest add?** Discovery, fixtures, parametrization, markers, hooks, assertions, and multiple report formats.
8. **What is a fixture?** Managed setup/teardown such as a browser, API session, or unique customer.
9. **Why explicit waits?** They synchronize with observed conditions and reduce fixed-delay flakiness.
10. **How do you avoid flaky UI tests?** Stable locators, isolated data, conditions, independent tests, screenshots/logs, and root-cause tracking.
11. **Why not automate all 76 manual cases in UI?** UI automation is slower/brittle; automate critical UI flows and push rule matrices to API level.
12. **What do API tests assert?** Status, schema/types, values, security, errors, headers where relevant, and persistence side effects.
13. **Key status codes?** 201 create, 204 cancel, 401 unauthenticated, 403 unauthorized, 404 missing, 409 conflict, 422 validation.
14. **How is authentication tested?** Valid/invalid/missing/malformed/expired tokens and role/ownership boundaries.
15. **Authentication vs authorization?** Identity verification versus permission to perform a specific action/object.
16. **Why SQL for QA?** It independently validates state, relations, aggregates, and anomalies hidden by UI/API formatting.
17. **Example JOIN?** Booking joined to users/providers/services confirms every foreign key resolves and values match the request.
18. **What does GROUP BY test?** It identifies more than one active booking per provider/time.
19. **What is GraphQL testing different?** Validate field selection, variables, schema errors, resolver authorization, and partial/error envelopes.
20. **Smoke vs regression?** Smoke is a small release-blocking confidence gate; regression is broader change-impact coverage.
21. **What is a defect lifecycle?** New, triaged, assigned, fixed, retested, closed or reopened; deferred requires accepted risk.
22. **Severity vs priority?** Impact versus scheduling; a low-severity demo typo could have high priority.
23. **What does the RTM provide?** Visible requirement coverage and impact analysis when requirements change.
24. **How would you performance-test?** Record environment/workload, ramp realistic reads, examine p95/throughput/failures, correlate resources, never invent results.
25. **QA in Agile?** Refine acceptance/testability early, plan risk, test increments, triage, regress, demonstrate evidence, assess release.
26. **What does CI do here?** Recreates services, checks health, runs layers, generates and preserves machine/human reports.
27. **How do you debug a failure?** Reproduce, classify product/test/environment, inspect response/log/screenshot/data, minimize, compare change, report evidence.
28. **What if a test is flaky?** Treat it as a defect; isolate cause and repair. Temporary quarantine needs ownership and replacement coverage.
29. **How make a release decision?** Evaluate exit criteria, critical risks, evidence, unresolved defects, rollback, and state Go/Conditional/No-Go transparently.
30. **What would you improve?** UTC/timezones, transactional concurrency tests, migrations, richer provider/admin UI, accessibility, and measured baselines.
31. **What is QA bug mode?** Isolated intentional mutations proving tests can detect faults; false by default and not a claim about client defects.
32. **What did you learn?** Quality is traceable risk control across layers, not merely browser scripts or pass counts.
