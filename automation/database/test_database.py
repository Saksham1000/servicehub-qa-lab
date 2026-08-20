import os,pytest
from sqlalchemy import create_engine,text

@pytest.fixture(scope='module')
def connection():
    url=os.getenv('DATABASE_URL')
    if not url or url.startswith('sqlite'): pytest.skip('DATABASE_URL for live MySQL is required')
    engine=create_engine(url)
    with engine.connect() as conn: yield conn

@pytest.mark.database
def test_booking_references_are_valid(connection):
    q=text('SELECT COUNT(*) FROM bookings b LEFT JOIN users u ON u.id=b.customer_id LEFT JOIN providers p ON p.id=b.provider_id LEFT JOIN services s ON s.id=b.service_id WHERE u.id IS NULL OR p.id IS NULL OR s.id IS NULL')
    assert connection.execute(q).scalar()==0

@pytest.mark.database
def test_no_active_provider_double_booking(connection):
    q=text("SELECT COUNT(*) FROM (SELECT provider_id,appointment_time,COUNT(*) c FROM bookings WHERE status IN ('confirmed','completed') GROUP BY provider_id,appointment_time HAVING COUNT(*)>1) duplicates")
    assert connection.execute(q).scalar()==0

@pytest.mark.database
def test_status_domain(connection):
    assert connection.execute(text("SELECT COUNT(*) FROM bookings WHERE status NOT IN ('confirmed','cancelled','completed')")).scalar()==0
