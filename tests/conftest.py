from src.modules import *
from src.handlers.api_handler import GameAPI

api = GameAPI()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def pytest_addoption(parser):
    parser.addoption("--DT"         , action="store_true", help="Run tests for DT game type")
    parser.addoption("--BACCARAT"   , action="store_true", help="Run tests for BACCARAT game type")
    parser.addoption("--SICBO"      , action="store_true", help="Run tests for SICBO game type")
    parser.addoption("--SEDIE"      , action="store_true", help="Run tests for SEDIE game type")

@pytest.fixture(scope="session")
def game_options(request):
    return {
        'DT'        : request.config.getoption("--DT"),
        'BACCARAT'  : request.config.getoption("--BACCARAT"),
        'SICBO'     : request.config.getoption("--SICBO"),
        'SEDIE'     : request.config.getoption("--SEDIE"),
    }

@pytest.fixture(scope="session")
def driver():
    url = api.get_game_url()
    option = Options()
    option.add_argument("--window-size=450,950")
    option.add_argument("--window-position=900,0")
    option.add_argument("--window-position=1430,0")
    option.add_argument('--log-level=1')
    option.add_argument(f"--user-agent={userAgent.random}")
    option.add_argument(f"--app={url}")
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    
    yield driver
    driver.quit()

@pytest.fixture(scope="session", params=[84, 140]) #, 160, 90
def drivers(request):
    index = request.param
    url = api.get_game_url(index=index)
    option = Options()
    option.add_argument("--window-size=450,950")
    option.add_argument("--window-position=1430,0")
    option.add_argument('--log-level=1')
    option.add_argument(f"--user-agent={userAgent.random}")
    option.add_argument(f"--app={url}")
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=option)
    yield driver, index 
    driver.quit()