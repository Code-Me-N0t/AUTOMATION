from src.modules import *
from src.main import *

def test_RUN(driver):
    # PlayMulti(driver, 'SICBO', report=True)
    # PlayMulti(driver, 'SEDIE', report=True)
    PlayMulti(driver, 'BACCARAT', report=True)
    PlayMulti(driver, 'DT', report=True)