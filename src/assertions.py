from src.helpers import *
from src.modules import *


def TableSwitch(driver, tableNum, gameTable, testcase, table, scenario):
    tableName = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)
    while tableName.text == '': continue
    assertion(driver,'Switch Table Assertion', gameTable, tableName.text, operator.eq, testcase['Switch Table'], table, gameTable, scenario['Switch Table'])

def CancelBet(driver, game, gameTable, expected, tableNum, betArea, testcase, table, scenario):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum, timer=10)
    findModElement(driver, 'MULTI BUTTON', 'CANCEL', click=True, table=tableNum)
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    getText = betPlaced.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Cancel Bet Assertion', valuePlaced, expected, operator.ne, testcase['Cancel Bet'], table, gameTable, scenario['Cancel Bet'])

def BetSuccessful(driver, game, gameTable, tableNum, betArea, testcase, table, scenario):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tableNum)
    for _ in range(100):
        validate = findModElement(driver, 'MULTI', 'VALIDATION', table=tableNum)
        validate = validate.text
        if validate != "": break
        sleep(.5)

    assertion(driver,'Bet Successful Assertion', validate, 'Bet Successful!',  operator.eq, testcase['Bet Successful'], table, gameTable, scenario['Bet Successful'])

def BalanceDeduction(driver, gameTable, oldBalance, chip, testcase, table, scenario):
    prev_balance = None
    same_balance_count = 0
    for _ in range(100):
        newbalance_element = findElement(driver, "MULTI", "USER BALANCE")
        newbalance = newbalance_element.text
        if newbalance == prev_balance: same_balance_count += 1
        else: same_balance_count = 0
        prev_balance = newbalance
        if same_balance_count >= 100: break

    deductedBalance = oldBalance - chip
    expected_balance = round(deductedBalance, 2)
    actual_balance = round(float(newbalance.replace(',','')), 2)
    assertion(driver,'Balance Deducted Assertion', actual_balance, expected_balance, operator.eq, testcase['Balance Deduction'], table, gameTable, scenario['Balance Deduction'])

def PlaceBet(driver, bet, title, gameTable, chip, testcase, table, scenario):
    getText = bet.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver, (title+f' [{getText[0]}]'), valuePlaced, chip, operator.eq, testcase, table, gameTable, scenario)

def NoMoreBets(driver, gameTable, tableNum, testcase, table, scenario):
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='No More Bets!', table=tableNum)
    assertion(driver,'No More Bets Assertion', validate, True, operator.eq, testcase['No More Bets'], table, gameTable, scenario['No More Bets'])

def ClosedBetTimer(driver, game, gameTable, tableNum, betArea, testcase, table, scenario):
    try: 
        findModElement(driver, "MULTI BETTINGAREA", game, betArea, click=True, table=tableNum)
        validate = False
    except ElementClickInterceptedException:validate = True
    assertion(driver,'Bet in Closed Betting Timer', validate, True, operator.eq, testcase['Bet In Closed Betting Timer'], table, gameTable, scenario['Bet In Closed Betting Timer'])

def Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, testcase, table, chip, scenarios):
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
        assertion(driver,'Payout Assertion [WIN]', round(addedBalance, 2), round(validateAddedBalance, 2), operator.eq, testcase['Payout'], table, gameTable, scenarios['Payout'])
    else: assertion(driver,'Payout Assertion [LOSE]', round(newBalance, 2), round(deductedBalance, 2), operator.eq, testcase['Payout'], table, gameTable, scenarios['Payout'])


def EmptyBetarea(driver, gameTable, chip, testcase, table, bet, scenario):
    getText = bet.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Empty Betarea Assertion', valuePlaced, chip, operator.ne, testcase['Empty Bet Area'], table, gameTable, scenario['Empty Bet Area'])

def UnconfirmedBet(driver, game, gameTable, tableNum, chip, betArea, testcase, table, scenario):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum, timer=10)
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    valuePlaced = betPlaced.text.split('\n')[-1]
    assertion(driver,'Unconfirmed Bet Assertion', valuePlaced, chip, operator.ne, testcase['Unconfirmed Bet'], table, gameTable, scenario['Unconfirmed Bet'])