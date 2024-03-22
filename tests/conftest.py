from src.modules import *
from src.gameapp import *

@pytest.fixture(scope="session")
def driver():
    # Set up Chrome options to emulate a custom device with a screen width of 500 pixels
    option = Options()
    option.add_argument("--window-size=400,1000")
    option.add_argument("--window-position=0,0")
    option.add_experimental_option('mobileEmulation', {
        'deviceMetrics': {'width': 500, 'height': 870, 'pixelRatio': 2.0},
        'userAgent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36'
    })
    # Instantiate a browser driver with the configured options
    driver = webdriver.Chrome(options=option)
    
    # Get the URL
    url = get_token()
    driver.get(url)
    
    yield driver
    
    # Clean up after the test session
    driver.quit()
