import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def get_phone():
    url = "https://api.viotp.com/users/balance?token=bc123ea9bcf641e882c39842746bdcea&serviceId=1"
    url = "https://api.viotp.com/request/getv2?token=bc123ea9bcf641e882c39842746bdcea&serviceId=1&network=MOBIFONE|VINAPHONE|VIETTEL|VIETNAMOBILE|ITELECOM"
    res = requests.get(url)
    print(res.json())

def find_tag(browser, tag, identifier):
    b = browser.find_elements(By.TAG_NAME, value=tag)
    for btn in b:
        if identifier in btn.text:
            return btn
    return None


def open_chrome(profile=None):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    browser = uc.Chrome(
        options=options,
    )
    
    #implicit wait
    browser.implicitly_wait(0.5)
    #launch URL
    browser.get("https://accounts.google.com/signup")
    #identify elements within form
    firstname = browser.find_element(By.ID, value="firstName")
    firstname.send_keys("Test")
    lastname = browser.find_element(By.ID, value="lastName")
    lastname.send_keys("One")
    username = browser.find_element(By.ID, value="username")
    username.send_keys("dialog1123dog")
    password = browser.find_element(By.NAME, value="Passwd")
    password.send_keys("test124@")
    c = browser.find_element(By.NAME, value="ConfirmPasswd")
    c.send_keys("test124@")
    b = find_tag(browser, 'button', "Tiếp theo")
    time.sleep(3)
    b.click()
    

    while True:
        time.sleep(10000)  

if __name__ == "__main__":
    get_phone()
    # open_chrome()