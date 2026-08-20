import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.data_factory import customer
from utils.config import BASE_URL

@pytest.mark.ui
@pytest.mark.smoke
def test_register_requires_separate_login(driver):
    data=customer()
    RegisterPage(driver,BASE_URL).open().register(data)
    WebDriverWait(driver,10).until(lambda d:'Account created' in d.page_source)
    assert 'Sign in to continue' in driver.page_source
    assert driver.execute_script("return localStorage.getItem('token')") is None

@pytest.mark.ui
@pytest.mark.security
@pytest.mark.parametrize('email,password',[('bad@example.com','Wrong123!'),('admin@servicehub.example','Wrong123!')])
def test_invalid_login(driver,email,password):
    page=LoginPage(driver,BASE_URL).open().login(email,password)
    assert 'Incorrect' in page.text(page.ALERT)

@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_and_logout(driver):
    LoginPage(driver,BASE_URL).open().login('admin@servicehub.example','Admin123!')
    WebDriverWait(driver,10).until(lambda d:'Log out' in d.page_source)
    driver.find_element('xpath',"//button[normalize-space()='Log out']").click()
    assert 'Sign in' in driver.page_source
