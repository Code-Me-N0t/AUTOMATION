from src.modules import *
from src.main import Multi

def test_multi(driver):
    multi = Multi(driver)
    multi.main('DT')
    multi.main('BACCARAT')
    multi.main('SICBO')
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