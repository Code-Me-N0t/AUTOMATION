from src.modules import *
from src.main import *

def test_RUN(driver):
    # sample(driver)
    PlayMulti(driver, 'SICBO', report=False)
    # PlayMulti(driver, 'SEDIE', report=False)
    # PlayMulti(driver, 'BACCARAT', report=False)
    # PlayMulti(driver, 'DT', report=False)
    