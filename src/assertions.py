from src.helpers import *
from src.modules import *

def TableSwitch(driver, tableNum, gameTable, testcase, scenario):
    tableName = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)
    while tableName.text == '': continue
    assertion(driver,'Switch Table Assertion', gameTable, tableName.text, operator.eq, testcase['Switch Table'], gameTable, scenario['Switch Table'])

def CancelBet(driver, game, gameTable, expected, tableNum, betArea, testcase, scenario):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum, timer=10)
    findModElement(driver, 'MULTI BUTTON', 'CANCEL', click=True, table=tableNum)
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    getText = betPlaced.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Cancel Bet Assertion', valuePlaced, expected, operator.ne, testcase['Cancel Bet'], gameTable, scenario['Cancel Bet'])

def BetSuccessful(driver, game, gameTable, tableNum, betArea, testcase, scenario):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tableNum)
    for _ in range(100):
        validate = findModElement(driver, 'MULTI', 'VALIDATION', table=tableNum)
        validate = validate.text
        if validate != "": break
        sleep(.5)

    assertion(driver,'Bet Successful Assertion', validate, 'Bet Successful!',  operator.eq, testcase['Bet Successful'], gameTable, scenario['Bet Successful'])

def BalanceDeduction(driver, gameTable, oldBalance, chip, testcase, scenario):
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
    assertion(driver,'Balance Deducted Assertion', actual_balance, expected_balance, operator.eq, testcase['Balance Deduction'], gameTable, scenario['Balance Deduction'])

def PlaceBet(driver, bet, title, gameTable, chip, testcase, scenario):
    getText = bet.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver, (title+f' [{getText[0]}]'), valuePlaced, chip, operator.eq, testcase, gameTable, scenario)

def NoMoreBets(driver, gameTable, tableNum, testcase, scenario):
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='No More Bets!', table=tableNum)
    assertion(driver,'No More Bets Assertion', validate, True, operator.eq, testcase['No More Bets'], gameTable, scenario['No More Bets'])

def ClosedBetTimer(driver, game, gameTable, tableNum, betArea, testcase, scenario):
    try: 
        findModElement(driver, "MULTI BETTINGAREA", game, betArea, click=True, table=tableNum)
        validate = False
    except ElementClickInterceptedException:validate = True
    assertion(driver,'Bet in Closed Betting Timer', validate, True, operator.eq, testcase['Bet In Closed Betting Timer'], gameTable, scenario['Bet In Closed Betting Timer'])

def Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, testcase, chip, scenarios):
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
        assertion(driver,'Payout Assertion [WIN]', round(addedBalance, 2), round(validateAddedBalance, 2), operator.eq, testcase['Payout'], gameTable, scenarios['Payout'])
    else: assertion(driver,'Payout Assertion [LOSE]', round(newBalance, 2), round(deductedBalance, 2), operator.eq, testcase['Payout'], gameTable, scenarios['Payout'])

def EmptyBetarea(driver, gameTable, chip, testcase, bet, scenario):
    getText = bet.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Empty Betarea Assertion', valuePlaced, chip, operator.ne, testcase['Empty Bet Area'], gameTable, scenario['Empty Bet Area'])

def UnconfirmedBet(driver, game, gameTable, tableNum, chip, betArea, testcase, scenario):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum, timer=10)
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    valuePlaced = betPlaced.text.split('\n')[-1]
    assertion(driver,'Unconfirmed Bet Assertion', valuePlaced, chip, operator.ne, testcase['Unconfirmed Bet'], gameTable, scenario['Unconfirmed Bet'])

def superSix(driver, gametable, tablenum, testcase, scenario):
    """
    super six scenario
    scenario 1: 
        • switch s6 on
        • s6 betarea should display
    scenario 2: 
        • switch s6 off
        • s6 betarea should be hidden
    scenario 3: 
        • switch s6 on
        • place a bet on s6 betarea
        • validate bet has been successful
    assertion: assert all scenario passed
    """
    # scenario 1
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'SUPER SIX', table=tablenum)
    betareas = findModElements(driver, 'SUPER SIX', 'BET AREA', table=tablenum)

    for betarea in betareas:
        open_s6 = betarea.text
        if open_s6 == 'S6': break

    # scenario 2
    waitModClickable(driver, 'MULTI BUTTON', 'SUPER SIX', table=tablenum)
    betareas = findModElements(driver, 'SUPER SIX', 'BET AREA', table=tablenum)

    for betarea in betareas:
        last_betarea = betareas[-2].text
        if 'bet-odds' in betarea.get_attribute('class'): continue
        hidden_s6 = betarea.text
        if hidden_s6 == 'S6': break
        
    # scenario 3
    waitModClickable(driver, 'MULTI BUTTON', 'SUPER SIX', table=tablenum)
    waitModClickable(driver, 'MULTI TABLE', 'SUPER SIX', table=tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'CONFIRM', table=tablenum)

    for _ in range(100):
        validate = findModElement(driver, 'MULTI', 'VALIDATION', table=tablenum)
        validate_bet = validate.text
        if validate_bet != "": break
        sleep(.5)
        
    # assertion
    assertion(driver, 'Bet On Super Six', 
                [open_s6, hidden_s6, validate_bet], 
                ['S6', last_betarea, 'Bet Successful!'], 
                operator.eq, 
                testcase['Bet On Super Six'], 
                gametable,
                scenario['Bet On Super Six']
            )
    
def WithinBetPool(driver, gametable, tablenum, amount, testcase, scenario):
    waitModElement(driver, "SIDEBET", "RESULT", table=tablenum)
    waitModElementInvis(driver, "SIDEBET", "RESULT", table=tablenum)
    amount-=1
    EditChips(driver, chipValue=amount)
    BettingTimer(driver, tableNum=tablenum)

    waitModClickable(driver, 'MULTI TABLE', 'TIE', table=tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'CONFIRM', table=tablenum)

    for _ in range(100):
        validate = findModElement(driver, 'MULTI', 'VALIDATION', table=tablenum)
        validate = validate.text
        if validate != "": break
        sleep(.5)
        
    assert 'Bet Successful!' == validate, 'Bet Successful did not display'

    bet = findModElement(driver, 'MULTI TABLE', 'TIE', table=tablenum)
    getText = bet.text.split('\n')
    valuePlaced = int(getText[-1])

    assertion(driver, 'Bet Within Bet Pool', valuePlaced, amount, operator.eq, testcase['Bet Within Bet Pool'],  gametable, scenario['Bet Within Bet Pool'])

def BelowAboveBetlimit(driver, title, game, gametable, tablenum, betarea, amount, testcase, scenario):
    waitModElement(driver, "SIDEBET", "RESULT", table=tablenum)
    waitModElementInvis(driver, "SIDEBET", "RESULT", table=tablenum)

    if 'Below' in title: amount-=1
    else: amount+=1

    EditChips(driver, chipValue=amount)
    BettingTimer(driver, tableNum=tablenum)

    while True:
        waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
        message = findModElement(driver, 'MULTI', 'VALIDATION', click=False, table=tablenum)
        if title in message.text: break
        waitModClickable(driver, 'MULTI BUTTON', 'CONFIRM', table=tablenum)
    assertion(driver, title, message.text, title, operator.eq, testcase['Bet Below/Above Bet Limit'], gametable, scenario['Bet Below/Above Bet Limit'])

def WithinBetLimit(driver, title, game, gametable, tablenum, betarea, amount, testcase, scenario):
    waitModElement(driver, "SIDEBET", "RESULT", table=tablenum)
    waitModElementInvis(driver, "SIDEBET", "RESULT", table=tablenum)
    EditChips(driver, chipValue=amount)
    BettingTimer(driver, tableNum=tablenum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tablenum)
    waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tablenum, time=10)
    placed_bet = findModElement(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
    bet_amount = float(placed_bet.text.split('\n')[-1].replace(',',''))

    assertion(driver, title, amount, bet_amount, operator.eq, testcase['Bet Within Bet Limit'], gametable, scenario['Bet Within Bet Limit'])

