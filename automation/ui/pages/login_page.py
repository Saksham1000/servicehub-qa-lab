from selenium.webdriver.common.by import By
from .base_page import BasePage
class LoginPage(BasePage):
    EMAIL=(By.CSS_SELECTOR,'[data-testid="email"]');PASSWORD=(By.CSS_SELECTOR,'[data-testid="password"]');SUBMIT=(By.CSS_SELECTOR,'[data-testid="auth-submit"]');ALERT=(By.CSS_SELECTOR,'[role="alert"]')
    def login(self,email,password):self.type(self.EMAIL,email);self.type(self.PASSWORD,password);self.click(self.SUBMIT);return self
