import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleService:
    def __init__(self, browser: uc.Chrome, email, password="Admin123!") -> None:
        self.browser = browser
        self.email = email
        self.password = password
        self.login_url = "https://accounts.google.com/signin/v2/identifier?hl=vi&continue=https%3A%2F%2Fmail.google.com&service=mail&ec=GAlAFw&flowName=GlifWebSignIn&flowEntry=AddSession"
        self.is_login = False
        self.count = 0

        
    
    def login(self):
        self.browser.get(self.login_url)
        self.browser.find_element(By.ID, 'identifierId').send_keys(self.email)
        self.browser.find_element(By.CSS_SELECTOR, '#identifierNext > div > button > span').click()
        password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

        self.browser.find_element(
            By.CSS_SELECTOR, password_selector).send_keys(self.password)

        self.browser.find_element(
            By.CSS_SELECTOR, '#passwordNext > div > button > span').click()
        
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".zA.yO")))
        self.is_login = True
    
    def get_code(self):
        self.login()

        for i in self.browser.find_elements(By.CSS_SELECTOR, "table > tbody > tr"):
            if "APPEN" in i.text:
                i.click()
                break
        
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.TAG_NAME, "tr")))
        for element in self.browser.find_elements(By.TAG_NAME, "div"):
            text = element.text
            pattern = "Email Address Verification Code: "
            for e in text.split('\n'):
                if pattern in e:
                    return e.split(pattern)[-1]
        
        if self.count < 5:
            self.count += 1
            time.sleep(5)
            return self.get_code()
        
        return None

