from src.modules import *
from src.gameapp import *

def update_balance():
    url = get_token(balance=1750.35)
    option = Options()
    option.add_argument("--window-size=450,950")
    option.add_argument("--window-position=1430,0")
    option.add_argument(f"--user-agent={userAgent.random}")
    option.add_argument(f"--app={url}")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(0.5)
    return driver