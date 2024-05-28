from src.modules import *
from src.gameapp import *

@pytest.fixture(scope="session")
def driver():
    url = get_token(84,1000000)
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

@pytest.fixture(scope="session", params=[84, 140, 160, 90])
def drivers(request):
    index = request.param
    url = get_token(index, 1000000)
    option = Options()
    option.add_argument("--window-size=450,950")
    option.add_argument("--window-position=1430,0")
    option.add_argument(f"--user-agent={userAgent.random}")
    option.add_argument(f"--app={url}")
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    yield driver, index 
    driver.quit()

@pytest.fixture(scope="session")
def bal_driver():
    url = get_token(84, 1750.35)
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
