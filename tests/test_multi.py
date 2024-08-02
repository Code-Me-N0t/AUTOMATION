from src.modules import *
from src.main import Multi

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

# @pytest.mark.update_scenario
# def test_UPDATESCENARIO(): update_scenarios('all')

# @pytest.mark.single_bet
# def test_SINGLEBET(driver):
#     PlayMulti(driver, 'SEDIE',    'singlebet', report=True)
#     PlayMulti(driver, 'SICBO',    'singlebet', report=True)
#     PlayMulti(driver, 'DT',       'singlebet', report=True)
#     PlayMulti(driver, 'BACCARAT', 'singlebet', report=True)

# @pytest.mark.multiple_bet
# def test_MULTIPLEBET(driver):
#     PlayMulti(driver, 'DT',       'multiplebet', report=True)
#     PlayMulti(driver, 'BACCARAT', 'multiplebet', report=True)
#     PlayMulti(driver, 'SEDIE',    'multiplebet', report=True)
#     PlayMulti(driver, 'SICBO',    'multiplebet', report=True)

# @pytest.mark.betlimit
# def test_BETLIMIT(drivers):
#     driver, index = drivers
#     PlayMulti(driver, 'SEDIE',     'betlimit', report=True, index=index)
#     PlayMulti(driver, 'SICBO',     'betlimit', report=True, index=index)
#     PlayMulti(driver, 'BACCARAT',  'betlimit', report=True, index=index)
#     PlayMulti(driver, 'DT',        'betlimit', report=True, index=index)

# @pytest.mark.allin
# def test_ALLIN(driver):
#     PlayMulti(driver, 'DT',       'allinbet', report=True, new_balance=1750.35)
#     PlayMulti(driver, 'BACCARAT', 'allinbet', report=True, new_balance=1750.35)
#     PlayMulti(driver, 'SEDIE',    'allinbet', report=True, new_balance=1750.35)
#     PlayMulti(driver, 'SICBO',    'allinbet', report=True, new_balance=1750.35)