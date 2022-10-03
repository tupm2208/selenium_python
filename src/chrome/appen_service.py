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
        self.login_url = "https://identity.appen.com/auth/realms/QRP/protocol/openid-connect/auth?response_type=code&client_id=appen-connect&redirect_uri=https%3A%2F%2Fconnect.appen.com%2Fqrp%2Fcore%2Flogin%2Fview%3Bjsessionid%3D7EF0176B60F08781F8DC360CC955FC0D&state=cdb29735-4824-46d6-9d99-5ba3f5452fc0&login=true&scope=openid"
        self.login_url = "https://connect.appen.com/qrp/core/login"
        self.is_filled = False

    def save_file(self, filename):
        with open(f"H:/projects/Python-Selenium-Tutorial/appen_source/{filename}.html", 'w', encoding='utf8') as f:
            f.write(self.browser.page_source)

    def find_option(self, class_name, identifier, e_type=By.CLASS_NAME):
        b = self.browser.find_elements(e_type, value=class_name)
        for btn in b:
            # print(btn.text)
            try:
                if identifier in btn.text:
                    return btn
            except Exception as e:
                continue
        return None

    def register(self):
        self.browser.get(self.register_url)
        try:
            self.browser.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        except Exception as e:
            pass
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        self.fill_email_password()
        self.browser.find_element(By.NAME, 'firstName').send_keys(self.profile["firstName"])
        self.browser.find_element(By.NAME, 'lastName').send_keys(self.profile["lastName"])
        self.browser.find_element(By.CSS_SELECTOR, '.css-1hwfws3').click()
        self.save_file("register")
        self.find_option("select-option", self.profile["country"]).click()
        self.find_option("span", "18 years", By.TAG_NAME).click()
        self.find_option("span", "tax documentation", By.TAG_NAME).click()
        # WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//label[@data-testid="country-doc-check"]')))
        # self.browser.find_element(By.XPATH, '//label[@data-testid="country-doc-check"]').click()
        # WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-hHEiqL.sc-dlMDgC.coOviN.kPMvCr.submit-button')))
        time.sleep(1)
        
        element = self.browser.find_element(By.XPATH, '//button[@data-testid="sign-up-btn"]')
        actions = ActionChains(self.browser)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()
        
        # time.sleep(100)
    
    def sign_yukon_docs(self):
        if "esign/view/personalized_agreement" not in self.browser.current_url:
            return
        self.fill_email_password()
        self.browser.find_element(By.NAME, 'sign').click()
    
    def fill_yukon_info(self):
        url = "https://connect.appen.com/qrp/core/vendors/intelligent_attributes/view/0"
        if "vendors/intelligent_attributes/view" not in self.browser.current_url:
            self.browser.get(url)
            if "vendors/intelligent_attributes/view" not in self.browser.current_url:
                return
        
        # self.save_file("yukon_field")
        self.browser.find_element(By.NAME, 'attributes[0].stringValue').click()
        self.find_option("option", "More than 5 years", By.TAG_NAME).click()
        self.browser.find_element(By.NAME, 'attributes[1].stringValue').click()
        self.browser.find_element(By.NAME, 'attributes[2].stringValue').send_keys("Google")
        self.browser.find_element(By.NAME, 'save').click()

        
        
    def apply_yukon(self):
        yukon_url = "https://connect.appen.com/qrp/core/vendors/projects?qualify=&project.id=1"
        self.browser.get(yukon_url)
        if "qualify=&project.id=1" in self.browser.current_url:
            self.save_file("yukon_1")
            self.browser.find_element(By.NAME, 'doQualify').click()
            time.sleep(1)
            self.save_file("yukon_2")
        
        self.sign_yukon_docs()
        self.fill_yukon_info()

    def fill_email_password(self, filed="email"):
        
        if not self.is_filled:
            self.browser.find_element(By.NAME, filed).send_keys(self.profile["email"])
            self.browser.find_element(By.NAME, 'password').send_keys("Admin123!")



    def verify(self, code):
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        self.save_file("verification_code")
        self.browser.find_element(By.NAME, 'verificationCode').send_keys(code)
        time.sleep(1)
        self.find_option("button", "Verify Email", By.TAG_NAME).click()
        time.sleep(1)


    def login(self):
        # self.browser.get(self.home_url)
        # WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-black-hollow')))
        # self.browser.find_element(By.CSS_SELECTOR, '.btn-black-hollow').click()
        self.browser.get(self.login_url)
        
        if "identity.appen.com" not in self.browser.current_url:
            return
        # time.sleep(10)
        # self.save_file("login")
        self.fill_email_password("username")
        self.browser.find_element(By.NAME, 'login').click()
        if "identity.appen.com" in self.browser.current_url:
            self.is_filled = True
            self.login()
    

    def chose_language(self):
        choose_language_url = "https://connect.appen.com/qrp/core/vendors/primary_language"

        if choose_language_url not in self.browser.current_url:
            self.browser.get(choose_language_url)
            time.sleep(1)
            if choose_language_url not in self.browser.current_url:
                return

        
        try:
            WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        except Exception as e:
            print(e)
            
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'primaryLanguage')))
        self.browser.find_element(By.ID, 'primaryLanguage').click()
        # time.sleep(100)
        self.find_option("select-option", self.profile["country_language"]).click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'languageRegion')))
        self.browser.find_element(By.ID, 'languageRegion').click()
        time.sleep(3)
        self.find_option("select-option", self.profile["country"]).click()
        time.sleep(3)
        self.browser.find_element(By.XPATH, '//button[@data-testid="primary-language-submit-btn"]').click()


    def setup_user_profile(self):
        time.sleep(3)
        profile_url = "https://connect.appen.com/qrp/core/vendors/user_profile_setup"
        if profile_url not in self.browser.current_url:
            self.browser.get(profile_url)
            time.sleep(3)
            if profile_url not in self.browser.current_url:
                return
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"page-wrapper")))
        
        # time.sleep(100)
        
        # address
        if "STEP 03:" in self.find_option("h2", "STEP", By.TAG_NAME).text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.NAME,"address")))
            self.browser.find_element(By.NAME, 'address').send_keys(self.profile["address"])
            self.browser.find_element(By.NAME, 'city').send_keys(self.profile["city"])
            self.browser.find_element(By.NAME, 'state').send_keys(self.profile["state"])
            self.browser.find_element(By.NAME, 'zip').send_keys(self.profile["zip"])
            self.browser.find_element(By.XPATH, '//div[@data-testid="residency-years-select"]').click()
            self.browser.find_element(By.ID, 'react-select-5-option-5').click()
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(3)

        # Education
        if "STEP 04:" in self.find_option("h2", "STEP", By.TAG_NAME).text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="select-education-level"]')))
            self.browser.find_element(By.XPATH, '//div[@data-testid="select-education-level"]').click()
            time.sleep(3)
            try:
                for e in self.browser.find_elements(By.CSS_SELECTOR, '.select-menu.select-option'):
                    if "Bachelor Degree" in e.text:
                        e.click()
                        break
            except Exception as e:
                pass
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(3)

        if "STEP 05:" in self.find_option("h2", "STEP", By.TAG_NAME).text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-cBoqAE.doZwHS')))
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(3)
        
        if "STEP 06:" in self.find_option("h2", "STEP", By.TAG_NAME).text:
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.ID, 'primaryPhone')))
            self.browser.find_element(By.ID, 'primaryPhone').send_keys(self.profile["phone"])
            self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(3)
        self.save_file("setup_user_profile")
        print(self.find_option("h2", "STEP", By.TAG_NAME).text)
        if "STEP 07:" in self.find_option("h2", "STEP", By.TAG_NAME).text:
            # print("========================")
            self.find_option("button", "Save And Submit Profile", By.TAG_NAME).click()
            # self.browser.find_element(By.XPATH, '//button[@data-testid="next-btn"]').click()
            time.sleep(10)
        
        ctn = self.find_option("button", "Continue", By.TAG_NAME)
        if ctn is not None:
            ctn.click()


        
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

    def sign_first_document(self):
        if "vendors/esign/view/electronic_consent" not in self.browser.current_url:
            return
        
        self.fill_email_password()
        self.browser.find_element(By.NAME, 'sign').click()
        # self.save_file("sign_first")
        time.sleep(3)
    
    def sign_second_document(self):
        if "esign/view/company_confidentiality_agreement" not in self.browser.current_url:
            return
        self.fill_email_password()
        self.browser.find_element(By.NAME, 'sign').click()
        time.sleep(3)
        

    def fill_infomation(self):
        self.chose_language()
        self.setup_user_profile()
        self.set_smartphone()
        self.complete_view()
        self.sign_first_document()
        self.sign_second_document()
        print("Complete_registation!")


if __name__ == "__main__":
    profile = {
        "email": "t.iago.house.l5190@gmail.com",
        "password": "Admin123!",
        "firstName": "trachpro",
        "lastName": "lastname",
        "country": "Vietnam",
        "phone": "888545888",
        "address": "address",
        "city": "city",
        "state": "state",
        "zip": "zip",
        "epassword": "izpEImmdNc8",
        "country_language": "Vietnamese"
    }

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    browser = uc.Chrome(
        options=options,
    )
    appen = AppenService(browser, profile)
    # appen.register()
    appen.login()
    appen.fill_infomation()
    time.sleep(1000)