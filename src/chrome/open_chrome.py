import email
import time
import pandas as pd
import undetected_chromedriver as uc
import urllib.request
import urllib.error

from selenium import webdriver

def get_profile(email):

    df = pd.read_csv(r"../../datasets/data.csv")
    df = df[df["email"] == email]
    if len(df) < 1:
        print("Number of rows: ", len(df))
        return {"email": email}
    
    columns = list(df.columns)
    arr = df.values.tolist()[0]
    profile = {cl: vl for cl, vl in zip(columns, arr)}

    return profile


def open_chrome(profile):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f'--proxy-server={profile["IP"]}:2129')
    # options.add_argument(f'--proxy-server==socks5://127.0.0.1:30152')
    # options.add_argument(f'--proxy-server==107.191.62.48:2129')
    options.add_argument(r'--user-data-dir=C:\Users\TuPM\AppData\Local\Google\Chrome\User Data')
    options.add_argument(f'--profile-directory={profile["email"]}')
    
    browser = uc.Chrome(
        options=options,
    )
    
    tz_params = {'timezoneId': 'Asia/Tokyo'}
    browser.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

    while True:
        time.sleep(10000)




def is_bad_proxy(profile):    
    try:
        print("checking...")
        proxy_handler = urllib.request.ProxyHandler({'socks5': "127.0.0.1:20333"})
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
    email = "mei.karasawa1501@gmail.com"
    # email = "monoko.uno0202@gmail.com"
    # email = "kana.tanabe2411@gmail.com"
    # email = "hirokawa.naoko2702@gmail.com"
    # email = "nagisa.hiroshi2610@gmail.com"
    # email = "momoko.kudo2005@gmail.com"
    # email = "momoko.tanabe0303@gmail.com"
    # email = "vking3412@gmail.com"
    # email = "manionjakari5101998@gmail.com"
    # email = "phamminhtu2207@gmail.com"
    # email = "tu.phamminh.2207@gmail.com"
    # email = "arrow6372567nao@gmail.com"
    # email = "arrow7877943momoko@gmail.com"
    # email = "arrow7804399kyo@gmail.com"
    # email = "arrow7820283mei@gmail.com"
    # email = "trachpro2208@gmail.com"
    # email = "quocphamt33s2f51mlc@gmail.com"
    # email = "vanphamwlazkaihgzqtb@gmail.com"
    # email = "angelrmothaibads896@gmail.com"
    # email = "tablesLeinolU3930@gmail.com"
    # email = "truongngo7t7mg3x0fh32@gmail.com"
    # email = "quoctranyh2axyl5cu@gmail.com"
    # email = "nganguyenwkhp1y@gmail.com"
    # email = "haungovsmouhbmg8p4@gmail.com"
    # email = "hungleg180gri4ay@gmail.com"
    # email = "huongnguyen89je9c3@gmail.com"
    # email = "binhnguyenxafzixy7qe@gmail.com"
    # email = "nghiahuys7r4b5ro@gmail.com"
    # email = "binhlywihspnei8qw@gmail.com"
    # email = "liannetownsend8918@gmail.com"

    profile = get_profile(email)
    # profile["IP"] = "139.162.84.217"

    print(f"{email} openning...")
    open_chrome(profile)
    # if profile is not None:
    #     if not is_bad_proxy(profile):
    #         print(f"{email} openning...")
    #         open_chrome(profile)