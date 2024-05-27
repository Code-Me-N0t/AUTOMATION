from src.modules import *
from src.main import *
from src.gameapp import *
from src.updatebalance import *

# def test_UPDATESCENARIO(): update_scenarios('all')

# def test_SINGLEBET(driver):
#     PlayMulti(driver, 'DT',       'singlebet', report=False)
    # PlayMulti(driver, 'BACCARAT', 'singlebet', report=False)
#     PlayMulti(driver, 'SEDIE',    'singlebet', report=False)
#     PlayMulti(driver, 'SICBO',    'singlebet', report=False)

# def test_MULTIPLEBET(driver):
#     PlayMulti(driver, 'DT',       'multiplebet', report=False)
    # PlayMulti(driver, 'BACCARAT', 'multiplebet', report=False)
#     PlayMulti(driver, 'SEDIE',    'multiplebet', report=False)
#     PlayMulti(driver, 'SICBO',    'multiplebet', report=False)

def test_ALLIN_baccarat():
    driver = update_balance()
    PlayMulti(driver, 'BACCARAT', 'allinbet', report=False)
    driver.quit()

def test_ALLIN_dt():
    driver = update_balance()
    PlayMulti(driver, 'DT', 'allinbet', report=False)
    driver.quit()

# def test_ALLIN_sicbo():
#     driver = create_bal_driver()
#     try:
#         PlayMulti(driver, 'SICBO', 'allinbet', report=False)
#     finally:
#         driver.quit()

# def test_ALLIN_sedie():
#     driver = create_bal_driver()
#     try:
#         PlayMulti(driver, 'SEDIE', 'allinbet', report=False)
#     finally:
#         driver.quit()

# def test_BETLIMIT(drivers):
#     driver, index = drivers
#     PlayMulti(driver, 'SEDIE',     'betlimit', report=False, index=index)
#     PlayMulti(driver, 'SICBO',     'betlimit', report=False, index=index)
    # PlayMulti(driver, 'BACCARAT',  'betlimit', report=False, index=index)
#     PlayMulti(driver, 'DT',        'betlimit', report=False, index=index)