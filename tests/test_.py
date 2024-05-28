from src.modules import *
from src.main import *

def test_ALLIN_dt(bal_driver):
    driver = bal_driver
    PlayMulti(driver, 'DT', 'allinbet', report=True, bal_driver=bal_driver)
    driver.quit()

# def test_UPDATESCENARIO(): update_scenarios('all')

# def test_SINGLEBET(driver):
#     PlayMulti(driver, 'DT',       'singlebet', report=True)
#     PlayMulti(driver, 'BACCARAT', 'singlebet', report=True)
#     PlayMulti(driver, 'SEDIE',    'singlebet', report=True)
#     PlayMulti(driver, 'SICBO',    'singlebet', report=True)

# def test_MULTIPLEBET(driver):
#     PlayMulti(driver, 'DT',       'multiplebet', report=True)
#     PlayMulti(driver, 'BACCARAT', 'multiplebet', report=True)
#     PlayMulti(driver, 'SEDIE',    'multiplebet', report=True)
#     PlayMulti(driver, 'SICBO',    'multiplebet', report=True)
    
# def test_ALLIN_baccarat(driver):
#     PlayMulti(driver, 'BACCARAT', 'allinbet', report=True)

# def test_ALLIN_dt():
#     driver = update_balance()
#     PlayMulti(driver, 'SICBO',    'allinbet', report=True)
#     driver.quit()

# def test_ALLIN_dt():
#     driver = update_balance()
#     PlayMulti(driver, 'SEDIE',    'allinbet', report=True)
#     driver.quit()

# def test_BETLIMIT(drivers):
#     driver, index = drivers
#     PlayMulti(driver, 'SEDIE',     'betlimit', report=True, index=index)
#     PlayMulti(driver, 'SICBO',     'betlimit', report=True, index=index)
#     PlayMulti(driver, 'BACCARAT',  'betlimit', report=True, index=index)
#     PlayMulti(driver, 'DT',        'betlimit', report=True, index=index)