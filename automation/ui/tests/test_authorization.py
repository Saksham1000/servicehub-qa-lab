import pytest
from pages.register_page import RegisterPage
from utils.config import BASE_URL
from utils.data_factory import customer
@pytest.mark.ui
@pytest.mark.security
def test_customer_ui_has_no_admin_controls(driver):RegisterPage(driver,BASE_URL).open().register(customer());assert 'Manage users' not in driver.page_source
