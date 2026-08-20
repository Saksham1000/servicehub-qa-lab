# Database Testing
Database checks reconcile externally created records and query MySQL through SQLAlchemy. Supply `DATABASE_URL`, start Compose, and run `pytest automation/database -m database`.

```sql
SELECT b.id,u.email,p.id AS provider,s.name,b.appointment_time,b.status
FROM bookings b JOIN users u ON u.id=b.customer_id
JOIN providers p ON p.id=b.provider_id JOIN services s ON s.id=b.service_id
WHERE b.id=:booking_id;

SELECT provider_id, appointment_time, COUNT(*) AS active_count
FROM bookings WHERE status IN ('confirmed','completed')
GROUP BY provider_id, appointment_time HAVING COUNT(*) > 1
ORDER BY active_count DESC;

SELECT status, COUNT(*) FROM bookings
WHERE appointment_time >= CURRENT_DATE GROUP BY status ORDER BY status;
```
Expected QA use: confirm request side effects, cancellation state, relationships, isolation, aggregate anomalies, and sorting/filtering. Use disposable test data; do not “fix” rows during validation.
