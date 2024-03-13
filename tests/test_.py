
from src.modules import *
from src.main import *
from src.helpers import sampleReport

def test_RUN(driver):
    # playMulti(driver, "SICBO", "BET LIMIT", report=False)
    # playMulti(driver, "SICBO", "PLACE BET", report=False)

    # playMulti(driver, "SEDIE", "BET LIMIT", report=False)
    # playMulti(driver, "SEDIE", "PLACE BET", report=False)

    # playMulti(driver, "BACCARAT", "BET LIMIT", report=False)
    # playMulti(driver, "BACCARAT", "PLACE BET", report=False)

    # playMulti(driver, "DT", "BET LIMIT", report=False)
    # playMulti(driver, "DT", "PLACE BET", report=False)

    playMulti(driver, "BACCARAT", "SUPER SIX", report=False)

    # sideBar(driver, "BACCARAT")