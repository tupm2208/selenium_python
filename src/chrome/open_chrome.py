import time
import pandas as pd
import undetected_chromedriver as uc
import urllib.request
import urllib.error

from selenium import webdriver

def get_profile(email):

    df = pd.read_csv(r"C:\Users\TuPM\Downloads\projects\Python-Selenium-Tutorial\datasets\data.csv")
    df = df[df["email"] == email]
    if len(df) != 1:
        print("Number of rows: ", len(df))
        return None
    
    columns = list(df.columns)
    arr = df.values.tolist()[0]
    profile = {cl: vl for cl, vl in zip(columns, arr)}

    return profile


def open_chrome(profile):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f'--proxy-server={profile["IP"]}:2129')
    options.add_argument(r'--user-data-dir=C:\Users\TuPM\AppData\Local\Google\Chrome\User Data')
    options.add_argument(f'--profile-directory={profile["email"]}')
    browser = uc.Chrome(
        options=options,
    )

    tz_params = {'timezoneId': 'Asia/Tokyo'}
    # tz_params = {'timezoneId': 'America/Dawson'}
    
    browser.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
    while True:
        time.sleep(10000)




def is_bad_proxy(profile):    
    try:
        print("checking...")
        proxy_handler = urllib.request.ProxyHandler({'http': profile["IP"]+":2129"})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('http://www.example.com')  # change the URL to test here
        sock=urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    print("good proxy")
    return False

if __name__ == "__main__":
    # email = "kyo.myojin0210@gmail.com"
    # email = "mei.karasawa1501@gmail.com"
    # email = "monoko.uno0202@gmail.com"
    # email = "kana.tanabe2411@gmail.com"
    # email = "hirokawa.naoko2702@gmail.com"
    # email = "nagisa.hiroshi2610@gmail.com"
    # email = "momoko.kudo2005@gmail.com"
    # email = "momoko.tanabe0303@gmail.com"
    # email = "vking3412@gmail.com"
    email = "manionjakari5101998@gmail.com"
    # email = "phamminhtu2207@gmail.com"
    profile = get_profile(email)
    if profile is not None:
        if not is_bad_proxy(profile):
            open_chrome(profile)