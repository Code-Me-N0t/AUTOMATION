from src.modules import *
from src.main import Sidebet

@pytest.mark.usefixtures("driver", "game_options")
def test_sidebet(driver, game_options):
    test = Sidebet(driver)
    
    if game_options['DT']:
        test.main('DT')
    
    if game_options['BACCARAT']:
        test.main('BACCARAT')
    
    if game_options['SICBO']:
        test.main('SICBO')
    
    if game_options['SEDIE']:
        test.main('SEDIE')
        
    if game_options['3CARDS']:
        test.main('3CARDS')