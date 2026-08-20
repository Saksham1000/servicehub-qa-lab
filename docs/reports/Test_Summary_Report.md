# Test Summary Report — ServiceHub 1.0

## Verified execution in the build environment
| Run | Result |
|---|---|
| Isolated backend REST + GraphQL suite | 16 passed, 0 failed (1.70 s final reported run) |
| Live Requests + GraphQL suite | 6 passed, 0 failed (0.25 s) |
| Selenium Chrome smoke | 3 passed, 0 failed; 13 deselected (16.13 s) |
| Full Selenium Chrome UI/responsive suite | 16 passed, 0 failed (74.11 s final reported run) |
| React production build | Successful; 15 modules transformed |
| Focused QA bug-mode detector run | Expected non-zero: admin authorization and booking-conflict regressions failed, proving intentional mutations were detected |

Reports are stored under `reports/`. These runs used Python 3.13.5, Node 22.15.0, Chrome 151, SQLite for isolated/live local API state, and local Vite/FastAPI processes. Counts are separate runs and must not be added as unique test cases.

## Not executed here
MySQL/database automation, Docker Compose, Firefox, Postman/Newman, GitHub Actions, and Locust were not executed. Docker was unavailable. Manual CSV case statuses remain Not Run. No performance statistics or production defects are claimed.

## Release view
Scope verified: backend business rules, REST/GraphQL contracts, frontend compilation, Chrome critical/UI/responsive behavior, and bug-mode detection. Known evidence gaps: MySQL-specific behavior/migrations, Firefox, CI, and measured performance. Exit criteria for a portfolio handoff are met; a real production release recommendation remains **Conditional** until those environment-specific checks complete.
