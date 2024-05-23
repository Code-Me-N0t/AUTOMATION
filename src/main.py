from src.modules import*
from src.helpers import*
from src.assertions import*

data = {
    "username": env("username"),
    "chip value": 201,
    "betlimit": [84]
}

test_status = {key: [] for key in scenarios.keys()}

multiTables = [[] for _ in range(len(test_status))]

def PlayMulti(driver, game, test, report=None, index=None):
    # update_scenarios(game, scenarios)
    navigateTab(driver, "MULTI")
    gameTable = locator(game)
    actions = ActionChains(driver)

    # try:
    for selectedGame in range(len(gameTable)):
        printText('title', f"\nFinding: {gameTable[selectedGame]}")
        
        game_found = False
        elements = findElements(driver, "MULTI", "MULTI TABLE")
        for i in range(len(elements)):
            name = elements[i]
            tableNum = locator("MULTI TABLE","MAIN")+str(i+1)+")"

            while name.text == '': continue

            if gameTable[selectedGame] not in name.text:
                # print("Table is not",gameTable[selectedGame])
                waitModClickable(driver, "MULTI", "TABLE SWITCH", table=tableNum)
                select = findElements(driver, "MULTI", "MINI TABLECARD")
                for x in range(len(select)):
                    actions.move_to_element(select[x]).perform()
                    if gameTable[selectedGame] in select[x].text:
                        select[x].click()
                        game_found = True
                        break
                    else: continue
                elements = findElements(driver, "MULTI", "MULTI TABLE")
                name = elements[i]
                if gameTable[selectedGame] not in name.text and game_found == False:
                    waitClickable(driver, "MULTI", "CLOSE SIDETABLE")
                if game_found: break
            else:
                game_found = True
                break

        if game_found: #PLACE BET
            chip = int(data['chip value'])
            balance = findElement(driver, "MULTI", "USER BALANCE")

            printText('title', f'Table {gameTable[selectedGame]} found')
            betArea = randomizeBetarea(game)

            BettingTimer(driver, tableNum)

            # TEST CASES
            if test == 'betlimit' and index is not None:
                betLimit(driver, game, index, gameTable[selectedGame], tableNum, betArea)
            elif test == 'singlebet':
                singleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)
            elif test == 'multiplebet':
                multipleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)
            elif test == 'allinbet':
                multipleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)
            else: print(Fore.RED+'Invalid test parameters') 

            # end of code
        if not game_found: printText('failed', f'Table {gameTable[selectedGame]} not found')
        
        elements = findElement(driver, "MULTI", "MULTI TABLE")
    printText('body', '\n************************** report summary **************************')

    # report
    if report is not None: 
        multiReportSheet(report, game, test_status)

    waitClickable(driver, "NAV", "FEATURED")
    waitElement(driver, "LOBBY", "MAIN")

    # except Exception as e:
    #     print(f'[ERROR]: {str(e)}')
    #     driver.save_screenshot(f"screenshots/{gameTable[selectedGame]}_{date.today()}_{datetime.now().second}.png")

def betLimit(driver, game, index, gametable, tablenum, betarea):
    findElement(driver, 'PLAYER', 'AVATAR', click=True)
    waitElement(driver, 'PLAYER', 'MAIN')
    betlimit = findElement(driver, 'PLAYER', 'BET LIMIT')
    getText = betlimit.text.split(' ')
    actual_min = int(getText[0])
    actual_max = int(getText[-1])
    expected_min = locator('BET LIMIT ID', str(index), 'MIN')
    expected_max = locator('BET LIMIT ID', str(index), 'MAX')

    assertion(driver, 'Correct Bet Limit Assertion', actual_min, expected_min, operator.eq, test_status['Correct Bet Limit'], multiTables[14], gametable, scenarios['Correct Bet Limit'])
    assertion(driver, 'Correct Bet Limit Assertion', actual_max, expected_max, operator.eq, test_status['Correct Bet Limit'], multiTables[14], gametable, scenarios['Correct Bet Limit'])
    
    findElement(driver, 'PLAYER', 'CLOSE', click=True)

    # assert can bet with lowest and highest bet
    WithinBetLimit(driver, f'Bet within bet limit [MIN: {actual_min}]', game, gametable, tablenum, betarea, actual_min)
    WithinBetLimit(driver, f'Bet within bet limit [MAX: {actual_max}]', game, gametable, tablenum, betarea, actual_max)

    # place below && over betlimit
    BelowAboveBetlimit(driver, 'Below Minimum Limit', game, gametable, tablenum, betarea, actual_min)
    BelowAboveBetlimit(driver, 'Over Maximum Limit!', game, gametable, tablenum, betarea, actual_max)

    # place below betlimit but within betpool
    if game == 'BACCARAT' or game == 'DT': WithinBetPool(driver, gametable, tablenum, actual_min)
    else: printText('body', f'Bet Within Bet Pool is not available in {game}')

def WithinBetPool(driver, gametable, tablenum, amount):
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

    assertion(driver, 'Bet Within Bet Pool', valuePlaced, amount, operator.eq, test_status['Bet Within Bet Pool'], multiTables[15], gametable, scenarios['Bet Within Bet Pool'])

def BelowAboveBetlimit(driver, title, game, gametable, tablenum, betarea, amount):
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
    assertion(driver, title, message.text, title, operator.eq, test_status['Bet Below/Above Bet Limit'], multiTables[17], gametable, scenarios['Bet Below/Above Bet Limit'])

def WithinBetLimit(driver, title, game, gametable, tablenum, betarea, amount):
    waitModElement(driver, "SIDEBET", "RESULT", table=tablenum)
    waitModElementInvis(driver, "SIDEBET", "RESULT", table=tablenum)
    EditChips(driver, chipValue=amount)
    BettingTimer(driver, tableNum=tablenum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tablenum)
    waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tablenum, time=10)
    placed_bet = findModElement(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
    bet_amount = float(placed_bet.text.split('\n')[-1].replace(',',''))

    assertion(driver, title, amount, bet_amount, operator.eq, test_status['Bet Within Bet Limit'], multiTables[15], gametable, scenarios['Bet Within Bet Limit'])

def singleBet(driver, game, gameTable, tableNum, chip, balance, betArea):
    displayToast(driver, 'SINGLE BET')
    printText('title', 'TEST: SINGLE BET')
    EditChips(driver, chipValue=chip)
    oldBalance = round(float(balance.text.replace(',','')), 2)

    TableSwitch(driver, tableNum, gameTable, test_status, multiTables[0], scenarios)
    CancelBet(driver, game, gameTable, chip, tableNum, betArea, test_status, multiTables[1], scenarios)
    UnconfirmedBet(driver, game, gameTable, tableNum, chip, betArea, test_status, multiTables[2], scenarios)
    BetSuccessful(driver, game, gameTable, tableNum, betArea, test_status, multiTables[3], scenarios)
    BalanceDeduction(driver, gameTable, oldBalance, chip, test_status, multiTables[4], scenarios)
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum,)
    PlaceBet(driver, betPlaced, 'Single Bet Assertion', gameTable, str(chip), test_status['Single Bet'], multiTables[5], scenarios['Single Bet'])
    NoMoreBets(driver, gameTable, tableNum, test_status, multiTables[7], scenarios)
    ClosedBetTimer(driver, game, gameTable, tableNum, betArea, test_status, multiTables[8], scenarios)
    if game == 'BACCARAT' or game == 'DT': b, r = GameResult(driver, game, gameTable, tableNum)
    Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, test_status, multiTables[9], chip, scenarios)
    EmptyBetarea(driver, gameTable, chip, test_status, multiTables[12], betPlaced, scenarios)
    if game == 'BACCARAT' or game == 'DT': BetRecord(driver, game, gameTable, b, r, tableNum)  

def multipleBet(driver, game, gameTable, tableNum, chip, balance, betArea):
    displayToast(driver, 'MULTIPLE BET')
    print('\n')
    printText('title', 'TEST: MULTIPLE BET')
    EditChips(driver, chipValue=chip)

    oldBalance = round(float(balance.text.replace(',','')), 2)
    BettingTimer(driver, tableNum, timer=14)

    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    betarea = findModElements(driver, 'MULTIPLE BETTINGAREA', game, table=tableNum)
    for bet in betarea: bet.click()
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tableNum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tableNum, time=10)
    assertion(driver,'Bet Successful Assertion', validate, True, operator.eq, test_status['Bet Successful'], multiTables[3], gameTable, scenarios['Bet Successful'])
            
    for bets in range(len(betarea)): betamount = chip * (bets+1)

    BalanceDeduction(driver, gameTable, oldBalance, betamount, test_status, multiTables[4], scenarios)
    for bet in betarea: PlaceBet(driver, bet, 'Multiple Bet Assertion', gameTable, str(chip), test_status['Multiple Bet'], multiTables[6], scenarios['Multiple Bet'])
    NoMoreBets(driver, gameTable, tableNum, test_status, multiTables[7], scenarios)
    ClosedBetTimer(driver, game, gameTable, tableNum, betArea, test_status, multiTables[8], scenarios)
    Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, test_status, multiTables[9], betamount, scenarios)

def BetRecord(driver, game, gameTable, b, r, tablenum):
    shoe = getShoe(driver, tablenum)
    card_dict = locator("CARDS", game)
    betarea = list(locator("MULTI BETTINGAREA", game).keys())
    blue_points = red_points = list_value = 0
    index = 1
    navigateSettings(driver, 'HISTORY')

    result = findElements(driver, 'MULTI HISTORY', 'RESULTS')
    for x in range(len(result)):
        betNum = locator("MULTI HISTORY","RESULTS")+str(locator('MULTI HISTORY', 'CON'))+str(x+1)+")"
        print(f'Result: {result[x].text}')
        if shoe in result[x].text:
            # print(f'Shoe: {shoe}')
            
            waitModClickable(driver, 'MULTI HISTORY', 'BET CODE', table=betNum)
            # sleep(10)
            cards = findElements(driver, 'MULTI HISTORY', 'CARD RESULT')
            for x in range(len(cards)):
                attrib = cards[x].get_attribute('class')
                start = attrib.find('base64,') + 7
                base64_string = attrib[start:]

                card_value = textDecoder(index, gameTable, base64_string, 'history', game)

                # print(f'Card Value: {card_value}')

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

    assertion(driver, f'Bet History Assertion [{betarea[0]}]', b, blue_points, operator.eq, test_status['Record History'], multiTables[15], gameTable, scenarios['Record History'])
    assertion(driver, f'Bet History Assertion [{betarea[1]}]', r, red_points, operator.eq, test_status['Record History'], multiTables[15], gameTable, scenarios['Record History'])

    waitClickable(driver, 'MULTI HISTORY', 'CLOSE')

def GameResult(driver, game, gametable, tableNum):
    waitModElement(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
    card_dict = locator("CARDS", game)
    betarea = list(locator("MULTI BETTINGAREA", game).keys())
    list_name = ''
    blue_points = red_points = list_value = 0
    index = 1

    cards = findModElements(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
    for card in cards:
        card_value = ''
        if 'card-hidden' in card.get_attribute('class'):
            card_value = 'e'
        else:
            repeat = True
            while repeat:
                image_string = card.find_element(By.CSS_SELECTOR, ':nth-child(2)').value_of_css_property('background-image')
                base64_string = re.search(r'url\("?(.*?)"?\)', image_string).group(1)
                base64_string = base64_string.replace('data:image/png;base64,','')
                card_value = textDecoder(index, gametable, base64_string, 'gametable', game)
                if card_value != 'e': repeat = False
        
        for key, value in card_dict.items():
            if card_value in key:
                list_name = key
                list_value = value
                break

        if game == 'BACCARAT':
            blue_points += list_value if index < 4 else 0
            red_points += list_value if index > 3 else 0
            if index != 3 and index != 6:
                while list_name == 'e': continue
                assertion(driver, f'Flip Cards Assertion', f'{list_name}', 'e', operator.ne, test_status['Flipped Cards'], multiTables[16], gametable, scenarios['Flipped Cards'])

        if game == 'DT':
            blue_points += list_value if index == 1 else 0
            red_points += list_value if index == 2 else 0
            assertion(driver, 'Flip Cards Assertion', f'{list_name}', 'e', operator.ne, test_status['Flipped Cards'], multiTables[16], gametable, scenarios['Flipped Cards'])
        index += 1
        cards = findModElements(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)

    if game == 'BACCARAT':
        blue_points %= 10 
        red_points %= 10

    actual_bpoints = int(findModElement(driver, 'MULTI TABLE', 'CARD POINTS 1', table=tableNum).text[-2:].replace(' ', ''))
    actual_rpoints = int(findModElement(driver, 'MULTI TABLE', 'CARD POINTS 2', table=tableNum).text[-2:].replace(' ', ''))

    assertion(driver, f'Card Result Assertion [{betarea[0]}]', actual_bpoints, blue_points, operator.eq, test_status["Card Result"], multiTables[15], gametable, scenarios["Card Result"])
    assertion(driver, f'Card Result Assertion [{betarea[1]}]', actual_rpoints, red_points, operator.eq, test_status["Card Result"], multiTables[15], gametable, scenarios["Card Result"])

    return actual_bpoints, actual_rpoints