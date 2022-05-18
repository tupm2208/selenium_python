import time
import undetected_chromedriver as uc
import pandas as pd
from selenium import webdriver
from appen_service import AppenService
from google_service import GoogleService

def get_profile(email):

    df = pd.read_csv("datasets/data.csv")
    df = df[df["email"] == email]
    if len(df) != 1:
        print("Number of rows: ", len(df))
        return None
    
    columns = list(df.columns)
    arr = df.values.tolist()[0]
    profile = {cl: vl for cl, vl in zip(columns, arr)}

    return profile

def main():
    profile = get_profile("hirokawa.hiroshi0706@gmail.com")
    print(profile)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f'--proxy-server={profile["IP"]}:2129')
    # options.add_argument(r'--user-data-dir=C:\Users\TuPM\AppData\Local\Google\Chrome\User Data')
    # options.add_argument(f'--profile-directory={profile["email"]}')
    browser = uc.Chrome(
        options=options,
    )

    
    # appen_service = AppenService(browser, profile)
    # appen_service.register()

    # browser.execute_script("window.open('');")
    # browser.switch_to.window(browser.window_handles[1])

    # google_service = GoogleService(browser, profile["email"], profile["password"])
    # code = google_service.get_code()
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
    # if not code:
    #     return
    # print("code: ", code)
    # appen_service.verify(code)


    # appen_service.login()
    # appen_service.fill_infomation()

    while True:
        time.sleep(10000)


if __name__ == '__main__':
    
    main()
    
