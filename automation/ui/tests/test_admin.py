import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from utils.config import BASE_URL

@pytest.mark.ui
@pytest.mark.regression
def test_admin_can_authenticate(driver):
    LoginPage(driver,BASE_URL).open().login('admin@servicehub.example','Admin123!')
    WebDriverWait(driver,10).until(lambda d:'signed in as admin' in d.page_source)
