from selenium.webdriver.common.by import By
from .base_page import BasePage
class AppointmentsPage(BasePage):
    NAV=(By.CSS_SELECTOR,'[data-testid="appointments-nav"]');ROWS=(By.CSS_SELECTOR,'.appointment')
    def open_list(self):self.click(self.NAV);return self
