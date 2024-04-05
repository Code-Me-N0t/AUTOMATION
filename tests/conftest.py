from src.modules import *
from src.gameapp import *

@pytest.fixture(scope="session")
def driver():
    url = get_token()
    option = Options()
    option.add_argument("--window-size=450,950")
    option.add_argument("--window-position=1430,0")
    option.add_argument(f"--user-agent={userAgent.random}")
    option.add_argument(f"--app={url}")
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    yield driver
    driver.quit()