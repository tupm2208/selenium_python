import time
import undetected_chromedriver as uc
import pandas as pd
from selenium import webdriver
from appen_service import AppenService
from google_service import GoogleService

COUNTRY_DIC = {
    "FR": "French	France",
    "DE": "German	Germany",
    "NL": "Dutch	Netherland",
    "JP": "Japanese	Japan",
    "SE": "Swedish	Sweden",
    "DK": "Danish	Denmark",
    "NO": "Norwegian Bokmål	Norway",
}

def extend_code(ccode):
    if ccode in COUNTRY_DIC.keys():
        splited = COUNTRY_DIC[ccode].split("	")
        return {
            "country_language": splited[0],
            "country": splited[1]
        }
    return {}

def get_profile(email):

    df = pd.read_csv("H:/projects/Python-Selenium-Tutorial/datasets/data.csv")
    df = df[df["email"] == email]
    if len(df) != 1:
        print("Number of rows: ", len(df))
        return None
    
    columns = list(df.columns)
    arr = df.values.tolist()[0]
    profile = {cl: vl for cl, vl in zip(columns, arr)}
    profile.update(extend_code(profile["ccode"]))
    print(profile)
    return profile

def get_options(profile):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-features=InfiniteSessionRestore")
    options.add_argument(r'--user-data-dir=H:\Go_Login_profiles\Chrome_register')
    options.add_argument(f'--profile-directory={profile["email"]}')
    return options

def main(profile):

    options = get_options(profile)
    browser = uc.Chrome(
        options=options,
    )
    google_service = GoogleService(browser, profile["email"], profile["epassword"])
    google_service.login()
    browser.close()
    browser.quit()
    

    options = get_options(profile)
    options.add_argument(f'--proxy-server=socks5://127.0.0.1:40000')
    browser = uc.Chrome(
        options=options,
    )
    
    appen_service = AppenService(browser, profile)

    appen_service.register()
    
    browser.execute_script("window.open('');")
    time.sleep(3)
    browser.switch_to.window(browser.window_handles[1])
    google_service = GoogleService(browser, profile["email"], profile["epassword"])
    code = google_service.get_code()
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    if not code:
        return
    print("code: ", code)
    appen_service.verify(code)


    appen_service.login()
    time.sleep(3)
    appen_service.fill_infomation()
    appen_service.apply_yukon()

    while True:
        time.sleep(10000)


if __name__ == '__main__':
    profile = get_profile("dinhhoaianym8plt@gmail.com")
    # profile = {
    #     "email": "tia.g.o.h.o.u.se.l.5.1.9.0@gmail.com",
    #     "password": "Admin123!",
    #     "firstName": "trachpro",
    #     "lastName": "lastname",
    #     "country": "Vietnam",
    #     "phone": "888545888",
    #     "address": "address",
    #     "city": "city",
    #     "state": "state",
    #     "zip": "zip",
    #     "epassword": "izpEImmdNc8",
    #     "country_language": "Vietnamese"
    # }
    
    main(profile)
    
