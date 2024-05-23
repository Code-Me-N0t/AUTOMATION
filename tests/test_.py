from src.modules import *
from src.main import *
from src.gameapp import *

# def test_SINGLEBET(driver):
#     PlayMulti(driver, 'DT',       'singlebet', report=True)
#     PlayMulti(driver, 'BACCARAT', 'singlebet', report=True)
#     PlayMulti(driver, 'SEDIE',    'singlebet', report=True)
#     PlayMulti(driver, 'SICBO',    'singlebet', report=True)

def test_MULTIPLEBET(driver):
    PlayMulti(driver, 'DT',       'multiplebet', report=True)
    PlayMulti(driver, 'BACCARAT', 'multiplebet', report=True)
    PlayMulti(driver, 'SEDIE',    'multiplebet', report=True)
    PlayMulti(driver, 'SICBO',    'multiplebet', report=True)

# def test_BETLIMIT(drivers):
#     driver, index = drivers
#     PlayMulti(driver, 'SEDIE',     'betlimit', report=True, index=index)
#     PlayMulti(driver, 'SICBO',     'betlimit', report=True, index=index)
#     PlayMulti(driver, 'BACCARAT',  'betlimit', report=True, index=index)
#     PlayMulti(driver, 'DT',        'betlimit', report=True, index=index)