# Severity and Priority
Severity is technical/business impact; priority is repair order. They correlate but are not interchangeable. A rare typo can be Low/P1 before a marketing demo, while a severe edge case may be High/P2 when unreachable in the current release.

| Example | Severity | Priority | Reason |
|---|---|---|---|
| Customer reads another customer's appointment | Critical | P0 | Privacy/security boundary breach |
| Provider double-booked | High | P1 | Core integrity failure |
| Cancelled slot remains unavailable | Medium | P1 | Revenue/journey impact with alternative slot workaround |
| Search is case-sensitive | Medium | P2 | Discovery degraded; workaround exists |
| Minor mobile spacing | Low | P3 | No functional loss |
