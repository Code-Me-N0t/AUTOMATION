from src.task_handler import Tasks
from src.element_handler import Handler
from src.modules import *

class Assert:
    def __init__(self, handler):
        self.handler = handler
        self.task = Tasks(self.handler)
        self.test = test_status

    @handle_exceptions
    def assertion(self, title, expected_result, actual_result, operator):
        print('a line 1')
        spacer = self.task.spacer()
        print('a line 2')

        try:
            print('a line 3')
            assert operator(expected_result, actual_result)
            status = 'PASSED'
            info = ''
        except AssertionError:
            print('a line 4')
            status = 'FAILED'
            info = f' Expected: {expected_result} Actual: {actual_result}'
        
        print('a line 5')
        
        self.task.printTexts('green' if status == 'PASSED' else 'red', title, f'{status}')
        print('test status next')
        test_status.append(status)
        print('screenshot next')
        create_files('screenshots/assertion')
        # self.handler.driver.save_screenshot(f'screenshots/[{self.game}][{title}].png')

        return status

    
        

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

def Payout(driver, game, gametable, balance, old_balance, betarea, testcase, chip, scenario):
    actual_new_balance = round(float(balance.text.replace(',','')), 2)
    expected_new_balance = old_balance - chip
    payout = locator("PAYOUT", f"{game}", f"{betarea}")

    if game != 'BACCARAT' or game != 'DT': waitElement(driver, 'MULTI TABLE', 'RESULT TITLE')
    actual_new_balance = round(float(balance.text.replace(',','')), 2)

    if actual_new_balance > old_balance:
        result = 'WIN'
        actual = actual_new_balance - old_balance
        expected = float(chip) * payout

    elif actual_new_balance < old_balance:
        result = 'LOSE'
        actual = actual_new_balance
        expected = expected_new_balance

    else:
        result = 'TIE'
        actual = actual_new_balance
        expected = old_balance

    assertion(driver,f'Payout Assertion [{result}]', round(actual, 2), round(expected, 2), operator.eq, testcase['Payout'], gametable, scenario['Payout'])

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
    BettingTimer(driver, tablenum)
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'SUPER SIX', table=tablenum)
    betareas = findModElements(driver, 'SUPER SIX', 'BET AREA', table=tablenum)

    for betarea in betareas:
        open_s6 = betarea.text
        if open_s6 == 'S6': break

    # scenario 2
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'SUPER SIX', table=tablenum)
    betareas = findModElements(driver, 'SUPER SIX', 'BET AREA', table=tablenum)

    for betarea in betareas:
        last_betarea = betareas[-2].text
        if 'bet-odds' in betarea.get_attribute('class'): continue
        hidden_s6 = betarea.text
        if hidden_s6 == 'S6': break
        
    # scenario 3
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tablenum)
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
    
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)
    waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)
    
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
    
    if 'Below' in title: 
        waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
        waitModClickable(driver, 'MULTI BUTTON', 'CONFIRM', table=tablenum)
        message = findModElement(driver, 'MULTI', 'VALIDATION', click=False, table=tablenum)
        while message.text == '': continue
        if title in message.text: pass
    else: 
        while True:
            waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
            message = findModElement(driver, 'MULTI', 'VALIDATION', click=False, table=tablenum)
            if message.text == '': continue
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

def sample_func(driver, game, gametable, tableNum, testcase):
    try:
        card_dict = locator("CARDS", game)
        expected_bpoints = expected_rpoints = 0
        betarea = list(locator("MULTI BETTINGAREA", game).keys())

        waitModElement(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
        waitModElement(driver, 'MULTI', 'WINNING MASK', table=tableNum)

        blue_elements = findModElements(driver, 'PLAYER CARDS', table=tableNum)
        red_elements = findModElements(driver, 'BANKER CARDS', table=tableNum)

        index = 1
        for blue_element, red_element in zip(blue_elements, red_elements):
            blue_attrib = blue_element.get_attribute('style')
            red_attrib = red_element.get_attribute('style')
            
            blue_match = re.search(r'url\("data:image/[^;]+;base64,([^"]+)"\)', blue_attrib)
            red_match = re.search(r'url\("data:image/[^;]+;base64,([^"]+)"\)', red_attrib)

            if blue_match: 
                blue_base64_string = blue_match.group(1)
                blue_card_value = textDecoder(index, gametable, blue_base64_string, 'result', game)
                for key, value in card_dict.items():
                    if blue_card_value in key:
                        blue_value = value
                        blue_name = key
                        break
            
            if red_match: 
                red_base64_string = red_match.group(1)
                red_card_value = textDecoder(index, gametable, red_base64_string, 'result', game)
                for key, value in card_dict.items():
                    if red_card_value in key:
                        red_value = value
                        red_name = key
                        break

            # flipped cards assertion
            if game == 'BACCARAT':
                if blue_name:
                    expected_bpoints = (expected_bpoints + blue_value) % 10
                    if index != 3:
                        assertion(driver, f'Flip Cards Assertion', f'{blue_name}', 'e', operator.ne, testcase['Flipped Cards'], gametable, scenarios['Flipped Cards'])
                if red_name:
                    expected_rpoints = (expected_rpoints + red_value) % 10
                    if index != 3:
                        assertion(driver, f'Flip Cards Assertion', f'{red_name}', 'e', operator.ne, testcase['Flipped Cards'], gametable, scenarios['Flipped Cards'])

            if game == 'DT':
                if blue_name:
                    expected_bpoints = blue_value
                    assertion(driver, f'Flip Cards Assertion', f'{blue_name}', 'e', operator.ne, testcase['Flipped Cards'], gametable, scenarios['Flipped Cards'])
                if red_name:
                    expected_rpoints = red_value
                    assertion(driver, f'Flip Cards Assertion', f'{red_name}', 'e', operator.ne, testcase['Flipped Cards'], gametable, scenarios['Flipped Cards'])

            index+=1

        blue_points = findModElement(driver, 'MULTI TABLE', 'CARD POINTS 1', table=tableNum)
        red_points = findModElement(driver, 'MULTI TABLE', 'CARD POINTS 2', table=tableNum)
        actual_bpoints = int(blue_points.text.split(':')[-1])
        actual_rpoints = int(red_points.text.split(':')[-1])

        assertion(driver, f'Card Result Assertion [{betarea[0]}]', actual_bpoints, expected_bpoints, operator.eq, testcase["Card Result"], gametable, scenarios["Card Result"])
        assertion(driver, f'Card Result Assertion [{betarea[1]}]', actual_rpoints, expected_rpoints, operator.eq, testcase["Card Result"], gametable, scenarios["Card Result"])

        return actual_bpoints, actual_rpoints
    except: 
        print(Fore.RED+"Skipping Test: Result time too short")
        return

def BetRecord(driver, game, gameTable, b, r, tablenum, testcase):
    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tablenum)
    shoe = getShoe(driver, tablenum)
    # print(f'Shoe: {shoe}')
    card_dict = locator("CARDS", game)
    betarea = list(locator("MULTI BETTINGAREA", game).keys())
    blue_points = red_points = list_value = 0
    index = 1
    navigateSettings(driver, 'HISTORY')

    result = findElements(driver, 'MULTI HISTORY', 'RESULTS')
    
    for x in range(len(result)):
        betNum = locator("MULTI HISTORY","RESULTS")+str(locator('MULTI HISTORY', 'CON'))+str(x+1)+")"
        
        while 'No Result' in result[x].text: sleep(2)

        if shoe in result[x].text:
            findModElement(driver, 'MULTI HISTORY', 'BET CODE', click=True, table=betNum)

            cards = findElements(driver, 'MULTI HISTORY', 'CARD RESULT')
            for x in range(len(cards)):
                attrib = cards[x].get_attribute('class')
                start = attrib.find('base64,') + 7
                base64_string = attrib[start:]

                card_value = textDecoder(index, gameTable, base64_string, 'history', game)

                for key, value in card_dict.items():
                    if card_value in key:
                        list_value = value
                        break
                            
                if game == 'BACCARAT':
                    if index <= 3: blue_points += list_value
                    if index >= 4: red_points += list_value
                    blue_points %= 10 
                    red_points %= 10
                elif game == 'DT':
                    if index == 3: blue_points += list_value
                    if index == 4: red_points += list_value
                index += 1
            break

    assertion(driver, f'Bet History Assertion [{betarea[0]}]', b, blue_points, operator.eq, testcase['Record History'], gameTable, scenarios['Record History'])
    assertion(driver, f'Bet History Assertion [{betarea[1]}]', r, red_points, operator.eq, testcase['Record History'], gameTable, scenarios['Record History'])

    waitClickable(driver, 'MULTI HISTORY', 'CLOSE')

