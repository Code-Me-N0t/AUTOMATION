from src.modules import*
from src.helpers import*
from src.assertions import*

data = {
    "username": env("username"),
    "chip value": 201,
    "betlimit": [84]
}

test_status = {key: [] for key in scenarios.keys()}

# multiTables = [[] for _ in range(len(test_status))]

def update_scenarios(games):
    if games == 'all': games = ['BACCARAT', 'DT', 'SICBO', 'SEDIE']

    for game in games:
        cell = locator("CELL", f"{game}")
        print(f'{Fore.GREEN}Updated game scenario: {game}')

        for index, (name, values) in enumerate(scenarios.items()):
            if values and name:
                if game not in ['BACCARAT', 'DT'] and name in ['Card Result', 'Flipped Cards', 'Bet Within Bet Pool']: continue
                if name == 'Bet On Super Six' and game != 'BACCARAT': continue
                
                update_spreadsheet(values, f"C{(cell + index)}")

def PlayMulti(driver, game, test, report=None, index=None, balance=None):
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
                allInBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, )
            else: print(Fore.RED+'Invalid test parameters') 

            # end of code
        if not game_found: printText('failed', f'Table {gameTable[selectedGame]} not found')
        
        elements = findElement(driver, "MULTI", "MULTI TABLE")
    printText('body', '\n************************** report summary **************************')

    # report
    if report is not None: multiReportSheet(report, game, test_status)

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

    assertion(driver, 'Correct Bet Limit Assertion', actual_min, expected_min, operator.eq, test_status['Correct Bet Limit'], gametable, scenarios['Correct Bet Limit'])
    assertion(driver, 'Correct Bet Limit Assertion', actual_max, expected_max, operator.eq, test_status['Correct Bet Limit'], gametable, scenarios['Correct Bet Limit'])
    
    findElement(driver, 'PLAYER', 'CLOSE', click=True)

    # assert can bet with lowest and highest bet
    WithinBetLimit(driver, f'Bet within bet limit [MIN: {actual_min}]', game, gametable, tablenum, betarea, actual_min, test_status, scenarios)
    WithinBetLimit(driver, f'Bet within bet limit [MAX: {actual_max}]', game, gametable, tablenum, betarea, actual_max, test_status, scenarios)

    # place below && over betlimit
    BelowAboveBetlimit(driver, 'Below Minimum Limit', game, gametable, tablenum, betarea, actual_min, test_status, scenarios)
    BelowAboveBetlimit(driver, 'Over Maximum Limit!', game, gametable, tablenum, betarea, actual_max, test_status, scenarios)

    # place below betlimit but within betpool
    if game == 'BACCARAT' or game == 'DT': WithinBetPool(driver, gametable, tablenum, actual_min, test_status, scenarios)
    else: printText('body', f'Bet Within Bet Pool is not available in {game}')

def singleBet(driver, game, gametable, tablenum, chip, balance, betArea):
    displayToast(driver, 'SINGLE BET')
    printText('title', 'TEST: SINGLE BET')
    EditChips(driver, chipValue=chip)
    oldBalance = round(float(balance.text.replace(',','')), 2)

    TableSwitch(driver, tablenum, gametable, test_status,scenarios)
    CancelBet(driver, game, gametable, chip, tablenum, betArea, test_status,scenarios)
    UnconfirmedBet(driver, game, gametable, tablenum, chip, betArea, test_status,scenarios)
    BetSuccessful(driver, game, gametable, tablenum, betArea, test_status,scenarios)
    BalanceDeduction(driver, gametable, oldBalance, chip, test_status,scenarios)
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tablenum,)
    PlaceBet(driver, betPlaced, 'Single Bet Assertion', gametable, str(chip), test_status['Single Bet'],scenarios['Single Bet'])
    NoMoreBets(driver, gametable, tablenum, test_status,scenarios)
    ClosedBetTimer(driver, game, gametable, tablenum, betArea, test_status,scenarios)
    if game == 'BACCARAT' or game == 'DT': b, r = GameResult(driver, game, gametable, tablenum)
    Payout(driver, game, gametable, tablenum, balance, oldBalance, betArea, test_status,chip, scenarios)
    EmptyBetarea(driver, gametable, chip, test_status, betPlaced, scenarios)
    if game == 'BACCARAT' or game == 'DT': BetRecord(driver, game, gametable, b, r, tablenum)
    if game == 'BACCARAT': superSix(driver, gametable, tablenum, test_status, scenarios)
        
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
    assertion(driver,'Bet Successful Assertion', validate, True, operator.eq, test_status['Bet Successful'],gameTable, scenarios['Bet Successful'])
            
    for bets in range(len(betarea)): betamount = chip * (bets+1)

    BalanceDeduction(driver, gameTable, oldBalance, betamount, test_status,scenarios)
    for bet in betarea: PlaceBet(driver, bet, 'Multiple Bet Assertion', gameTable, str(chip), test_status['Multiple Bet'],scenarios['Multiple Bet'])
    NoMoreBets(driver, gameTable, tableNum, test_status,scenarios)
    ClosedBetTimer(driver, game, gameTable, tableNum, betArea, test_status,scenarios)
    Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, test_status,betamount, scenarios)

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
        # print(f'Result: {result[x].text}')
        if shoe in result[x].text:
            # print(f'Shoe: {shoe}')
            
            waitModClickable(driver, 'MULTI HISTORY', 'BET CODE', table=betNum)
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

    assertion(driver, f'Bet History Assertion [{betarea[0]}]', b, blue_points, operator.eq, test_status['Record History'], gameTable, scenarios['Record History'])
    assertion(driver, f'Bet History Assertion [{betarea[1]}]', r, red_points, operator.eq, test_status['Record History'], gameTable, scenarios['Record History'])

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
                assertion(driver, f'Flip Cards Assertion', f'{list_name}', 'e', operator.ne, test_status['Flipped Cards'], gametable, scenarios['Flipped Cards'])

        if game == 'DT':
            blue_points += list_value if index == 1 else 0
            red_points += list_value if index == 2 else 0
            assertion(driver, 'Flip Cards Assertion', f'{list_name}', 'e', operator.ne, test_status['Flipped Cards'], gametable, scenarios['Flipped Cards'])
        index += 1
        cards = findModElements(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)

    if game == 'BACCARAT':
        blue_points %= 10 
        red_points %= 10

    actual_bpoints = int(findModElement(driver, 'MULTI TABLE', 'CARD POINTS 1', table=tableNum).text[-2:].replace(' ', ''))
    actual_rpoints = int(findModElement(driver, 'MULTI TABLE', 'CARD POINTS 2', table=tableNum).text[-2:].replace(' ', ''))

    assertion(driver, f'Card Result Assertion [{betarea[0]}]', actual_bpoints, blue_points, operator.eq, test_status["Card Result"], gametable, scenarios["Card Result"])
    assertion(driver, f'Card Result Assertion [{betarea[1]}]', actual_rpoints, red_points, operator.eq, test_status["Card Result"], gametable, scenarios["Card Result"])

    return actual_bpoints, actual_rpoints

def allInBet(driver, game, gametable, tablenum, chip, balance):
    displayToast(driver, 'ALL IN BET')
    printText('title', 'TEST: ALL IN BET')
    EditChips(driver, chipValue=chip)

    # scenario 1: validate 'Insufficient Bet' displayed
    validation_message = getInsufficientText(driver, game, tablenum)
    
    # scenario 2: all in then cancel, validate betarea is empty
    has_chip = False
    waitModClickable(driver, 'MULTI BUTTON', 'CANCEL', table=tablenum)

    sleep(2)

    bet_placed = findModElements(driver, 'MULTI TABLE', 'BET PLACED', table=tablenum)
    for bet_area in bet_placed:
        if 'hidden-chip' not in bet_area.get_attribute('class'): has_chip = True

    # scenario 3: all in then do not confirm, validate next round betting area is empty
    not_empty = False
    _ = getInsufficientText(driver, game, tablenum)

    waitModElement(driver, 'MULTI TABLE', 'RESULT TITLE', table=tablenum)
    waitModElementInvis(driver, 'MULTI TABLE', 'RESULT TITLE', table=tablenum)

    bet_placed = findModElements(driver, 'MULTI TABLE', 'BET PLACED', table=tablenum)
    for bet_area in bet_placed:
        if 'hidden-chip' not in bet_area.get_attribute('class'): not_empty = True

    # scenario 4: all in bet then click confirm, validate bet successful displayed
    _ = getInsufficientText(driver, game, tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'CONFIRM', table=tablenum)

    for _ in range(100):
        validate = findModElement(driver, 'MULTI', 'VALIDATION', table=tablenum)
        validate_bet = validate.text
        if validate_bet == "Bet Successful!": break
        sleep(.5)

    # scenario 5: validate balance remaining should be zero
    waitModElement(driver, 'MULTI TABLE', 'RESULT TITLE', table=tablenum)
    remaining_balance = round(float(balance.text.replace(',','')), 2)

    # assertion: assert all scenarios passed
    assertion(driver, 'All In Bet', 
              [validation_message, has_chip, not_empty, validate_bet, remaining_balance], 
              ['Insufficient Balance', False, False, 'Bet Successful!', 0], 
              operator.eq, 
              test_status['All In Bet'], 
              gametable, 
              scenarios['All In Bet'])


def getInsufficientText(driver, game, tablenum):
    repeat = True
    for index in range(100):
        betarea = findModElements(driver, 'MULTIPLE BETTINGAREA', game, table=tablenum)
        for bet in betarea: 
            bet.click()
            message = findModElement(driver, 'MULTI', 'VALIDATION', table=tablenum)
            validation_message = message.text
            if message.text == 'Insufficient Balance': 
                repeat = False
                break
        if repeat != True or index == 99: return validation_message
