from selenium.webdriver.common.by import By
from .base_page import BasePage
class AdminPage(BasePage):
    """Admin page object for future UI extensions; admin APIs are automated now."""
    TITLE=(By.TAG_NAME,'h1')
