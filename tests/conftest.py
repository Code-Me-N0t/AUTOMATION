from src.modules import *
from src.gameapp import *

@pytest.fixture(scope="session")
def driver():
    url = get_token()
    option = Options()
    option.add_argument("--incognito")
    option.add_argument("window-position=1430,0")
    option.add_argument("window-size=446,972")
    option.add_argument(f"--app={url}")
    option.add_experimental_option("mobileEmulation", emulation())
    
    # Define and initialize the driver
    driver = webdriver.Chrome(options=option)
    
    retries = 0
    max_retries = 3
    while retries < max_retries:
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator("PRE LOADING"))))
            break
        except TimeoutException:
            if retries < max_retries - 1:
                displayToast(driver, 'Element not found. Relaunching the driver...')
                driver.quit()
                driver = webdriver.Chrome(options=option)
                retries += 1
            else: raise
    
    yield driver
    
    # Clean up after the test session
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