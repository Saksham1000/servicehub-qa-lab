from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self,driver,base_url):
        self.driver=driver
        self.base_url=base_url
        self.wait=WebDriverWait(driver,10)

    def open(self,path=''):
        self.driver.get(self.base_url+path)
        return self

    def click(self,locator):
        element=self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center',behavior:'instant'});",element)
        element=self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self,locator,value):
        element=self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def text(self,locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text
