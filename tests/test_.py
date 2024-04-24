from src.modules import *
from src.main import *
from src.gameapp import *

# def test_RUN(driver):
#     # PlayMulti(driver, 'SEDIE')
#     # PlayMulti(driver, 'SICBO')
#     PlayMulti(driver, 'BACCARAT')
#     PlayMulti(driver, 'DT')

def test_BETLIMIT(drivers):
    driver, index = drivers
    # PlayMulti(driver, 'SEDIE', index=index)
    # PlayMulti(driver, 'SICBO', index=index)
    # PlayMulti(driver, 'BACCARAT', index=index)
    PlayMulti(driver, 'DT', index=index)