from src.modules import *
from src.main import *

def test_RUN(driver):
    # PlayMulti(driver, 'BACCARAT', report=False)
    PlayMulti(driver, 'DT', report=True)
    PlayMulti(driver, 'SEDIE', report=True)
    PlayMulti(driver, 'SICBO', report=True)