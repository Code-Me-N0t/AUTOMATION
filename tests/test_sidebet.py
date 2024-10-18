from src.modules import *
from src.side_main import Sidebet

@pytest.mark.single
@pytest.mark.usefixtures("driver", "game_options")
def test_singleDriver(driver, game_options):
    run_tests(driver, game_options, 84)

@pytest.mark.multiple
@pytest.mark.usefixtures("drivers", "game_options")
def test_multipleDrivers(drivers, game_options):
    driver, index = drivers
    run_tests(driver, game_options, index)

def run_tests(driver, game_options, index):
    side = Sidebet(driver)

    if game_options['DT']:
        side.main('DT', index)
    
    if game_options['BACCARAT']:
        side.main('BACCARAT', index)
    
    if game_options['SICBO']:
        side.main('SICBO', index)
    
    if game_options['SEDIE']:
        side.main('SEDIE', index)

    if game_options['3CARDS']:
        side.main('THREE CARDS', index)