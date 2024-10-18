from src.modules import *
from src.multi_main import Multi

@pytest.mark.usefixtures("driver", "game_options")
def test_multi(driver, game_options):
    multi = Multi(driver)
    
    if game_options['DT']:
        multi.main('DT')
    
    if game_options['BACCARAT']:
        multi.main('BACCARAT')
    
    if game_options['SICBO']:
        multi.main('SICBO')
    
    if game_options['SEDIE']:
        multi.main('SEDIE')