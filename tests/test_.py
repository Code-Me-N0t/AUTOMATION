from src.modules import *
from src.main import *

def test_RUN(driver):
    # USER_NAME = QAUSERTEST1128
    playSidebet(driver, "SICBO", "test", report=False)
    playSidebet(driver, "SEDIE", "test", report=False)
    playSidebet(driver, "DT", "test", report=False)
    playSidebet(driver, "BACCARAT", "test", report=False)

    # USER_NAME = QAUSERTEST99
    # playMulti(driver, "SICBO", "PLACE BET", report=True)
    # playMulti(driver, "SEDIE", "PLACE BET", report=True)
    # playMulti(driver, "DT", "PLACE BET", report=True)
    # playMulti(driver, "BACCARAT", "PLACE BET", report=True)

    # USER_NAME = QAUSERTEST299
    # playMulti(driver, "SICBO", "BET LIMIT", report=True)
    # playMulti(driver, "SEDIE", "BET LIMIT ", report=True)
    # playMulti(driver, "DT", "BET LIMIT", report=True)
    # playMulti(driver, "BACCARAT", "BET LIMIT", report=True)

    # USER_NAME = QAUSERTEST399
    # playMulti(driver, "BACCARAT", "SUPER SIX", report=True)