from numpy import choose
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests


class GoogleService:
    def __init__(self, browser: uc.Chrome, email, password="Admin123!", recovery=None) -> None:
        self.browser = browser
        self.email = email
        self.password = password
        self.recovery = recovery
        self.login_url = "https://accounts.google.com/signin/v2/identifier?hl=vi&continue=https%3A%2F%2Fmail.google.com&service=mail&ec=GAlAFw&flowName=GlifWebSignIn&flowEntry=AddSession"
        self.is_login = False
        self.count = 0

    def save_file(self, filename, data):
        with open(f"H:/projects/Python-Selenium-Tutorial/appen_source/{filename}.html", 'w', encoding='utf8') as f:
            f.write(data)
    
    def handle_web_chip(self):
        self.find_option("span", "Để sau", By.TAG_NAME).click()
        
    def find_option(self, class_name, identifier, e_type=By.CLASS_NAME):
        b = self.browser.find_elements(e_type, value=class_name)
        for btn in b:
            if identifier in btn.text:
                return btn
        return None
        
    def login(self):
        self.browser.get(self.login_url)
        if "https://www.google.com/intl/vi/gmail/about/" in self.browser.current_url:
            self.find_option('a', "Đăng nhập", By.TAG_NAME)
        if "accounts.google.com" not in self.browser.current_url:
            return
        
        self.save_file("google_login", self.browser.page_source)
        self.browser.find_element(By.ID, 'identifierId').send_keys(self.email)
        self.browser.find_element(By.CSS_SELECTOR, '#identifierNext > div > button > span').click()
        password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

        self.browser.find_element(
            By.CSS_SELECTOR, password_selector).send_keys(self.password)

        self.browser.find_element(
            By.CSS_SELECTOR, '#passwordNext > div > button > span').click()
        
        self.is_login = True
        time.sleep(3)
        # self.save_file("after_google_login", browser.page_source)
        if "https://gds.google.com/web/chip" in self.browser.current_url:
            self.handle_web_chip()
    
    def get_code(self):
        self.browser.get("https://mail.google.com/mail/u/0/#inbox")

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

if __name__ == "__main__":
    raw = "tiagohousel5190@gmail.com	izpEImmdNc8	cassiusmoreno1676@yahoo.com"
    # email = "maryangelcambron5807@gmail.com"
    # password = "rIRxgzmhT2C"
    # recovery = "marleneclarke9192@yahoo.com"
    email, password, recovery = raw.split()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    browser = uc.Chrome(
        options=options,
    )
    google = GoogleService(browser, email, password, recovery)
    # google.login()
    # code = google.get_code()
    # print(code)
    # time.sleep(1000)

    # browser.execute_script("window.open('');")
    # browser.switch_to.window(browser.window_handles[1])
    # time.sleep(1000)