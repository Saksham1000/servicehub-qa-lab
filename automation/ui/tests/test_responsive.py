import pytest
from pages.login_page import LoginPage
from utils.config import BASE_URL
@pytest.mark.ui
@pytest.mark.responsive
@pytest.mark.parametrize('width,height',[(1440,900),(1024,768),(768,1024),(390,844),(360,800)])
def test_login_remains_usable(driver,width,height):driver.set_window_size(width,height);page=LoginPage(driver,BASE_URL).open();assert driver.find_element(*page.SUBMIT).is_displayed()
