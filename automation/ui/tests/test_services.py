import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from pages.login_page import LoginPage
from pages.services_page import ServicesPage
from utils.config import BASE_URL

@pytest.fixture
def logged_in(driver):
    LoginPage(driver,BASE_URL).open().login('admin@servicehub.example','Admin123!')
    WebDriverWait(driver,10).until(lambda d:'Logout' in d.page_source)
    return driver

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize('term,expected',[('massage','Massage'),('MASSAGE','Massage'),('Device','Device Repair'),('not-present','')])
def test_search(logged_in,term,expected):
    page=ServicesPage(logged_in,BASE_URL).search(term)
    def expected_result(driver):
        texts=[element.text for element in driver.find_elements(*page.CARDS)]
        return any(expected in text for text in texts) if expected else len(texts)==0
    WebDriverWait(logged_in,10,ignored_exceptions=(StaleElementReferenceException,)).until(expected_result)


