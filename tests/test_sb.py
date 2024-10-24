from src.modules import *
from src.bet_SB_main import speedBaccarat as SB

@pytest.mark.sb
def test_sb(driver):
    bet_on_speed = SB(driver)
    
    bet_on_speed.main("RNG017")
    # bet_on_speed.main("C2")