from src.modules import *
from src.gameapp import get_gameurl
from src.updatebalance import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture(scope="session")
def driver():
    url = get_gameurl()
    option = Options()
    option.add_argument("--window-size=450,950")
    option.add_argument("--window-position=100,70")
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
    url = get_gameurl(index=index)
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

def pytest_configure(config):
    config.addinivalue_line("markers", "update_scenario: mark a test to update scenarios")
    config.addinivalue_line("markers", "single_bet: mark a test for single bets for all games")
    config.addinivalue_line("markers", "single_sedie: mark a test for single bets for sedie")
    config.addinivalue_line("markers", "single_sicbo: mark a test for single bets for sicbo")
    config.addinivalue_line("markers", "multiple_bet: mark a test for multiple bets")
    config.addinivalue_line("markers", "betlimit: mark a test for bet limits")
    config.addinivalue_line("markers", "allin: mark a test for all-in bets")