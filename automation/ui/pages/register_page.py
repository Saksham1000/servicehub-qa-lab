from selenium.webdriver.common.by import By
from .login_page import LoginPage
class RegisterPage(LoginPage):
    REGISTER_TAB=(By.XPATH,"//button[normalize-space()='Register']");NAME=(By.CSS_SELECTOR,'[data-testid="name"]')
    def register(self,data):self.click(self.REGISTER_TAB);self.type(self.NAME,data['name']);self.type(self.EMAIL,data['email']);self.type(self.PASSWORD,data['password']);self.click(self.SUBMIT);return self
