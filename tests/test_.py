
from src.modules import *
from src.main import *

def test_RUN(driver):
    playMulti(driver, "BACCARAT", "BET LIMIT", report=True)
    # playMulti(driver, "BACCARAT", "PLACE BET", report=True)
    # playMulti(driver, "DT", "BET LIMIT", report=True)
    # playMulti(driver, "DT", "PLACE BET", report=True)
    # playMulti(driver, "SICBO", "BET LIMIT", report=True)
    # playMulti(driver, "SICBO", "PLACE BET", report=True)
    # playMulti(driver, "SEDIE", "BET LIMIT", report=True)
    # playMulti(driver, "SEDIE", "PLACE BET", report=True)

    # betOnRoulette(driver)