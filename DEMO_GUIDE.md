# Five-Minute Interview Demo
**0:00–0:40 — README.** Say: “This is a personal QA portfolio showing the full lifecycle, not just Selenium. The table summarizes implemented layers without fabricated results.”

**0:40–1:15 — SRS and risk.** Open `docs/requirements/SRS.md` and `Risk_Assessment.md`. Show stable IDs and explain why authorization, time, and double booking lead priority.

**1:15–1:55 — Manual design and RTM.** Filter `Test_Cases.csv` for `REQ-BOOK-003`; show positive, ownership, boundary, API-to-DB, and responsive coverage. Follow it into `RTM.csv`.

**1:55–2:45 — Automation.** Show `automation/ui/pages`, its booking test, then API conflict tests. Say: “Page Objects isolate UI mechanics; lower-level tests efficiently cover rules.” Run `pytest -m smoke` with the stack already started.

**2:45–3:25 — API and SQL.** Open FastAPI `/docs` or a Requests/Postman test, then `docs/DATABASE_TESTING.md`. Explain reconciling an API booking against joined records and duplicate grouping.

**3:25–4:05 — Defects.** Show BUG-DEMO-003 and the matching regression. Explain bug mode is isolated and default behavior passes; never claim it was a client defect.

**4:05–4:40 — CI/reports.** Show `.github/workflows/qa.yml`, health wait, suite gates, and artifact upload. Open actual HTML/JUnit only if generated.

**4:40–5:00 — Close.** Say: “My release decision is based on traceable evidence, critical risk, and exit criteria. Next I would deepen timezone/concurrency and accessibility coverage.”
