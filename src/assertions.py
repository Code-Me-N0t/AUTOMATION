from src.helpers import *
from src.modules import *


def TableSwitch(driver, tableNum, gameTable, testcase, table):
    tableName = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)
    while tableName.text == '': continue
    assertion(driver,'Switch Table Assertion', gameTable, tableName.text, operator.eq, testcase, table, gameTable)


def CancelBet(driver, game, gameTable, expected, tableNum, betArea, testcase, table):
    try:    
        waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum, timer=10)
        findModElement(driver, 'MULTI BUTTON', 'CANCEL', click=True, table=tableNum)
        betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
        getText = betPlaced.text.split('\n')
        valuePlaced = getText[-1]
        assertion(driver,'Cancel Bet Assertion', valuePlaced, expected, operator.ne, testcase, table, gameTable)
    except: waitModElementInvis(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)

def BetSuccessful(driver, game, gameTable, tableNum, betArea, testcase, table):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tableNum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tableNum, time=10)
    assertion(driver,'Bet Successful Assertion', validate, True, operator.eq, testcase, table, gameTable)

def BalanceDeduction(driver, gameTable, oldBalance, chip, testcase, table):

    for _ in range(100): newbalance = findElement(driver, "MULTI", "USER BALANCE")

    deductedBalance = oldBalance - chip
    expected_balance = round(deductedBalance, 2)
    actual_balance = round(float(newbalance.text.replace(',','')), 2)
    assertion(driver,'Balance Deducted Assertion', actual_balance, expected_balance, operator.eq, testcase, table, gameTable)

def PlaceBet(driver, bet, title, gameTable, chip, testcase, table):
    getText = bet.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver, (title+f' [{getText[0]}]'), valuePlaced, chip, operator.eq, testcase, table, gameTable)

def NoMoreBets(driver, gameTable, tableNum, testcase, table):
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='No More Bets!', table=tableNum)
    assertion(driver,'No More Bets Assertion', validate, True, operator.eq, testcase, table, gameTable)

def ClosedBetTimer(driver, game, gameTable, tableNum, betArea, testcase, table):
    waitModElement(driver, "SIDEBET", "RESULT", table=tableNum)
    try: 
        findModElement(driver, "MULTI BETTINGAREA", game, betArea, click=True, table=tableNum)
        validate = False
    except ElementClickInterceptedException:validate = True
    assertion(driver,'Bet in Closed Betting Timer', validate, True, operator.eq, testcase, table, gameTable)

def Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, testcase, table, chip):
    newBalance = round(float(balance.text.replace(',','')), 2)
    deductedBalance = oldBalance - chip
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    repeat = True
    while repeat:
        assertWin = waitModElement(driver, "MULTI", "VALIDATION", table=tableNum)
        if assertWin.text != 'No More Bets!' and assertWin.text != '': repeat=False
    payout = locator("PAYOUT", f"{game}", f"{betArea}")
    
    if "Win" in assertWin.text:
        comPay = float(chip) * payout
        addedBalance = comPay + newBalance
        validateAddedBalance = oldBalance - (float(chip)-comPay)
        assertion(driver,'Payout Assertion [WIN]', round(addedBalance, 2), round(validateAddedBalance, 2), operator.eq, testcase, table, gameTable)
    else: assertion(driver,'Payout Assertion [LOSE]', round(newBalance, 2), round(deductedBalance, 2), operator.eq, testcase, table, gameTable)


def EmptyBetarea(driver, gameTable, chip, testcase, table, bet):
    
    getText = bet.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Empty Betarea Assertion', valuePlaced, chip, operator.ne, testcase, table, gameTable)