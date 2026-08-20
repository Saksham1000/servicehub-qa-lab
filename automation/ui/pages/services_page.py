from selenium.webdriver.common.by import By
from .base_page import BasePage
class ServicesPage(BasePage):
    SEARCH=(By.CSS_SELECTOR,'[aria-label="Search services"]');SEARCH_BUTTON=(By.XPATH,"//button[normalize-space()='Search']");CARDS=(By.CSS_SELECTOR,'.card');PROVIDER=(By.CSS_SELECTOR,'[data-testid^="provider-"]');SLOT=(By.CSS_SELECTOR,'[data-testid="slot"]');BOOK=(By.CSS_SELECTOR,'[data-testid="book"]')
    def search(self,value):self.type(self.SEARCH,value);self.click(self.SEARCH_BUTTON);return self
    def choose_first(self):self.click((By.CSS_SELECTOR,'[data-testid^="select-service-"]'));self.click(self.PROVIDER);self.click(self.SLOT);return self
