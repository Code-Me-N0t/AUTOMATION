from src.modules import *
from src.bet_SB_main import speedBaccarat as SB

def is_driver_alive(driver):
    """Check if the WebDriver session is still active."""
    try:
        # Send a command to check if the driver is still alive
        driver.current_url
        return True
    except WebDriverException:
        return False

@pytest.mark.tableC2
def test_sb_c2(driver1):
    while True:
        bet_on_speed = SB(driver1)
        bet_on_speed.main("C2")

        if not is_driver_alive(driver1):
            logging.info(f'{Fore.GREEN}Browser Closed. Relaunching...')
            continue

@pytest.mark.tableRNG17
def test_sb_rng17(driver2):
    while True:
        bet_on_speed = SB(driver2)
        bet_on_speed.main("RNG017")
        if not is_driver_alive(driver2):
            logging.info(f'{Fore.GREEN}Browser Closed. Relaunching...')
            continue

@pytest.mark.tableRNG06
def test_sb_rng06(driver3):
    while True:
        bet_on_speed = SB(driver3)        
        bet_on_speed.main("RNG006")
        if not is_driver_alive(driver3):
            logging.info(f'{Fore.GREEN}Browser Closed. Relaunching...')
            continue