from src.modules import *
from src.gameapp import *

@pytest.fixture(scope="session")
def driver():
    url = get_token()
    option = Options()
    option.add_argument("--incognito")
    option.add_argument("window-position=1410,0")
    option.add_argument("window-size=446,972")
    option.add_argument(f"--app={url}")
    option.add_experimental_option("mobileEmulation", emulation())
    driver = webdriver.Chrome(options=option)
    yield driver
    driver.quit()

def emulation():
    return {
        "deviceMetrics": {
            "width": 430, 
            "height": 895, 
            "pixelRatio": 3.0
            },
        "userAgent": 'Mozilla/5.0'\
        '(Linux; Android 14.0; Samsung Galaxy S20 Ultra/MRA58N)'\
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97'\
        'Mobile Safari/537.36'
    }