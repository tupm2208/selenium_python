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



class AppenService:
    def __init__(self, browser: uc.Chrome, profile) -> None:
        self.browser = browser
        self.profile = profile
        self.register_url = "https://connect.appen.com/qrp/core/sign-up"
        self.home_url = "https://connect.appen.com/qrp/public/home"


    def register(self):
        self.browser.get(self.register_url)
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        self.browser.find_element(By.NAME, 'email').send_keys(self.profile["email"])
        self.browser.find_element(By.NAME, 'password').send_keys("Admin123!")
        self.browser.find_element(By.NAME, 'firstName').send_keys(self.profile["firstName"])
        self.browser.find_element(By.NAME, 'lastName').send_keys(self.profile["lastName"])
        self.browser.find_element(By.CSS_SELECTOR, '.css-1hwfws3').click()
        self.browser.find_element(By.ID, 'react-select-2-option-112').click()
        self.browser.find_element(By.XPATH, '//label[@data-testid="adult-check"]').click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//label[@data-testid="country-doc-check"]')))
        self.browser.find_element(By.XPATH, '//label[@data-testid="country-doc-check"]').click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-hHEiqL.sc-dlMDgC.coOviN.kPMvCr.submit-button')))
        time.sleep(1)
        element = self.browser.find_element(By.XPATH, '//button[@data-testid="sign-up-btn"]')
        actions = ActionChains(self.browser)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()
        time.sleep(1)


    def verify(self, code):
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        self.browser.find_element(By.NAME, 'verificationCode').send_keys(code)
        time.sleep(3)
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-hHEiqL.sc-dlMDgC.coOviN.kPMvCr')))
        self.browser.find_element(By.XPATH, '//button[@data-testid="verify-email-btn"]').click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-bBjRSN.cdTyhF')))


    def login(self):
        self.browser.get(self.home_url)
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-black-hollow')))
        self.browser.find_element(By.CSS_SELECTOR, '.btn-black-hollow').click()
        
        if "identity.appen.com" not in self.browser.current_url:
            return
        self.browser.find_element(By.ID, 'username').send_keys(self.profile["email"])
        self.browser.find_element(By.ID, 'password').send_keys("Admin123!")
        self.browser.find_element(By.ID, 'rememberMe').click()
        self.browser.find_element(By.NAME, 'login').click()
    

    def chose_language(self):
        choose_language_url = "https://connect.appen.com/qrp/core/vendors/primary_language"

        if choose_language_url not in self.browser.current_url:
            self.browser.get(choose_language_url)
            time.sleep(1)
            if choose_language_url not in self.browser.current_url:
                return

        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'primaryLanguage')))
        self.browser.find_element(By.ID, 'primaryLanguage').click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'react-select-2-option-206')))
        self.browser.find_element(By.ID, 'react-select-2-option-206').click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'languageRegion')))
        self.browser.find_element(By.ID, 'languageRegion').click()
        

        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.select-menu.select-option')))
        time.sleep(1)
        try:
            for e in self.browser.find_elements(By.CSS_SELECTOR, '.select-menu.select-option'):
                if "Japan" in e.text:
                    e.click()
                    break
        except Exception as e:
            pass
        time.sleep(1)
        self.browser.find_element(By.XPATH, '//button[@data-testid="primary-language-submit-btn"]').click()


    def setup_user_profile(self):
        profile_url = "https://connect.appen.com/qrp/core/vendors/user_profile_setup"
        if profile_url not in self.browser.current_url:
            self.browser.get(profile_url)
            time.sleep(1)
            if profile_url not in self.browser.current_url:
                return
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))

        # address
        if "STEP 03:" in self.browser.find_element(By.CSS_SELECTOR, '.sc-fHCHyC.bDtJMO').text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.NAME,"address")))
            self.browser.find_element(By.NAME, 'address').send_keys(self.profile["address"])
            self.browser.find_element(By.NAME, 'city').send_keys(self.profile["city"])
            self.browser.find_element(By.NAME, 'state').send_keys(self.profile["state"])
            self.browser.find_element(By.NAME, 'zip').send_keys(self.profile["zip"])
            self.browser.find_element(By.XPATH, '//div[@data-testid="residency-years-select"]').click()
            self.browser.find_element(By.ID, 'react-select-5-option-5').click()
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(1)

        # Education
        if "STEP 04:" in self.browser.find_element(By.CSS_SELECTOR, '.sc-fHCHyC.bDtJMO').text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="select-education-level"]')))
            self.browser.find_element(By.XPATH, '//div[@data-testid="select-education-level"]').click()
            time.sleep(1)
            try:
                for e in self.browser.find_elements(By.CSS_SELECTOR, '.select-menu.select-option'):
                    if "Bachelor Degree" in e.text:
                        e.click()
                        break
            except Exception as e:
                pass
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(1)

        if "STEP 05:" in self.browser.find_element(By.CSS_SELECTOR, '.sc-fHCHyC.bDtJMO').text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-cBoqAE.doZwHS')))
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(1)
        
        if "STEP 06:" in self.browser.find_element(By.CSS_SELECTOR, '.sc-fHCHyC.bDtJMO').text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'primaryPhone')))
            self.browser.find_element(By.ID, 'primaryPhone').send_keys(self.profile["phone"])
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(1)
        
        if "STEP 07:" in self.browser.find_element(By.CSS_SELECTOR, '.sc-fHCHyC.bDtJMO').text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-fyGvY.fLibQH')))
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(1)

        
    def set_smartphone(self):
        if "complete_profile/smartphone" not in self.browser.current_url:
            return
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'owns-smartphone')))
        self.browser.find_element(By.ID, 'owns-smartphone').click()
        for a_tag in self.browser.find_elements(By.TAG_NAME, "a"):
            if "public/smartphone" in a_tag.text:
                requests.get(a_tag.text, headers={
                    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
                })
                break
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'submit')))
        self.browser.find_element(By.ID, 'submit').click()
        time.sleep(1)
        
    

    def complete_view(self):
        if "complete_profile/view" not in self.browser.current_url:
            return
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.NAME, 'profile.phonecallWilling')))
        try:
            self.browser.find_element(By.NAME, 'profile.gmailSameAccount').click()
        except Exception as e:
            pass
        self.browser.find_element(By.NAME, 'profile.phonecallWilling').click()
        self.browser.find_element(By.NAME, 'pornWilling').click()
        self.browser.find_element(By.NAME, 'offensiveWilling').click()
        self.browser.find_element(By.XPATH, "//select[@name='profile.computerLiteracy']/option[text()='Expert']").click()
        self.browser.find_element(By.NAME, 'save').click()
        time.sleep(1)


    def fill_infomation(self):
        self.chose_language()
        self.setup_user_profile()
        self.set_smartphone()
        self.complete_view()
        print("Complete_registation!")
