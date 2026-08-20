import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.booking_page import BookingPage
from pages.appointments_page import AppointmentsPage
from utils.config import BASE_URL
from utils.data_factory import customer

@pytest.mark.ui
@pytest.mark.smoke
def test_customer_booking_journey(driver):
    data=customer()
    RegisterPage(driver,BASE_URL).open().register(data)
    WebDriverWait(driver,10).until(lambda d:'Account created' in d.page_source)
    LoginPage(driver,BASE_URL).login(data['email'],data['password'])
    WebDriverWait(driver,10).until(lambda d:'Log out' in d.page_source)
    BookingPage(driver,BASE_URL).book_first_available()
    AppointmentsPage(driver,BASE_URL).open_list()
    assert driver.find_elements(*AppointmentsPage.ROWS)
