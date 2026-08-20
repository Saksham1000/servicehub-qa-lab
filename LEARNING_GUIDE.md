# Learn ServiceHub QA Lab

## The system in one journey
A customer types into React. `fetch` sends JSON to FastAPI. FastAPI validates the Pydantic schema, decodes the JWT, checks the customer role/ownership and booking rules, then SQLAlchemy commits to MySQL. The response updates the UI. Tests observe this through public boundaries and separately reconcile the stored row.

## Core tools in plain language
- **Selenium** controls a real browser like a user. The booking smoke chooses elements by stable `data-testid` attributes and confirms the appointment view.
- **Pytest** discovers `test_...` functions, runs assertions, and reports failures. Markers select suites: `-m smoke` or `-m regression`.
- A **fixture** prepares and cleans reusable context. `driver` creates a selected browser; `customer` registers unique data. Tests stay independent.
- **Page Object Model** puts UI locators/actions into pages, leaving tests focused on behavior. When a locator changes, update one page class.
- **Explicit waits** wait for a condition such as clickable/visible. Fixed sleeps are slower and flaky.
- **Requests/API testing** skips the UI and checks status, JSON shape, errors, security, and side effects. It is faster and pinpoints server behavior.
- **Postman** stores runnable requests and JavaScript assertions. Its environment carries `base_url` and the token returned by registration.
- **Database testing/SQL** verifies what the API actually persisted. JOIN connects booking to customer/provider/service; GROUP BY finds duplicate active slots.
- **GraphQL** lets the client request selected fields from one endpoint. Unlike REST, a validation failure may be HTTP 200 with an `errors` array.
- **Smoke testing** asks whether critical build paths work. **Regression testing** checks broadly that changes did not break established behavior.
- **Severity** is impact; **priority** is repair order.
- An **RTM** connects each requirement to manual and automated evidence so important behavior is not silently missed.
- **Locust** simulates concurrent users and measures latency, throughput, and failures. Targets are project-specific and results must be measured.
- **CI/CD** automates repeatable build/test steps. GitHub Actions starts MySQL/application services, waits for health, runs tests, and uploads reports; passing CI is evidence for one build, not a guarantee of quality.

## How to study
Read SRS requirement IDs, find their CSV test cases, follow the RTM to automation, then trace an endpoint through `main.py`, model, API test, and SQL check. Toggle bug mode only in a separate demo and predict which regression should fail before running it.
