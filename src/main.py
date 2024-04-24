multi_testcase = {
    "switch table":                               [],
    "cancel bet":                                 [],
    "unconfirmed bet":                            [],
    "bet successful":                             [],
    "balance deduction":                          [],
    "single bet":                                 [],
    "multiple bet":                               [],
    "no more bets":                               [],
    "bet in closed betting timer":                [],
    "payout":                                     [],
    "empty betareas on new round":                [],
    "record history assert":                      [],
    "correct bet limit":                          [],
    "bet within bet limit":                       [],
    "bet within bet pool":                        [],
    "bet below/above bet limit":                  [],
    "card result":                                [],
    "flipped cards":                              [],
    "all in":                                     [],
    "bet on super 6":                             [],
}

from src.modules import*
from src.helpers import*
from src.assertions import*

data = {
    "username": env("username"),
    "chip value": 201,
    "betlimit": [1]
}

multiTables = [[] for _ in range(len(multi_testcase))]

def PlayMulti(driver, game, report=None, index=None):
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
            chip = data['chip value']
            balance = findElement(driver, "MULTI", "USER BALANCE")

            printText('title', f'Table {gameTable[selectedGame]} found')
            randomize = locator("MULTI BETTINGAREA",f"{game}")
            betAreas = list(randomize.keys())
            betArea = random.choice(betAreas)

            EditChips(driver, actions, chipValue=data["chip value"])
            BettingTimer(driver, tableNum)

            shoe = findModElement(driver, 'MULTI TABLE', 'SHOE ROUND', table=tableNum)
            shoe = shoe.text[-5:].replace(' ', '')

            # TEST CASES
            if index is not None: betLimit(driver, game, index, gameTable[selectedGame], tableNum, betArea)
            # singleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)
            # multipleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)

            

            # EmptyBetarea(driver, game, gameTable[selectedGame], tableNum, betArea)

            # if game == 'BACCARAT' or game == 'DT': BetRecord(driver, game, gameTable, selectedGame, shoe, b, r)   


            # end of code
        if not game_found: printText('failed', f'Table {gameTable[selectedGame]} not found')
        
        elements = findElement(driver, "MULTI", "MULTI TABLE")
    printText('body', '\n************************** end of code **************************')

    # report
    if report is not None: multiReportSheet(report, game, *multi_testcase.items())

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

    assertion(driver, 'Correct Bet Limit Assertion', actual_min, expected_min, operator.eq, multi_testcase['bet within bet pool'], multiTables[16], gametable)
    assertion(driver, 'Correct Bet Limit Assertion', actual_max, expected_max, operator.eq, multi_testcase['bet within bet pool'], multiTables[16], gametable)
    
    findElement(driver, 'PLAYER', 'CLOSE', click=True)

    # assert can bet with lowest and highest bet
    actions = ActionChains(driver)
    EditChips(driver, actions, chipValue=actual_min)
    BettingTimer(driver, tableNum=tablenum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tablenum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tablenum, time=10)
    assertion(driver,'Bet Within Bet Limit [Min]', validate, True, operator.eq, multi_testcase['bet within bet limit'], multiTables[15], gametable)

    EditChips(driver, actions, chipValue=actual_max)
    BettingTimer(driver, tableNum=tablenum)
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betarea}', table=tablenum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tablenum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tablenum, time=10)
    assertion(driver,'Bet Within Bet Limit [Max]', validate, True, operator.eq, multi_testcase['bet within bet limit'], multiTables[15], gametable)

    # assert 
    
    

def singleBet(driver, game, gameTable, tableNum, chip, balance, betArea):
    displayToast(driver, 'SINGLE BET')
    printText('title', 'TEST: SINGLE BET')

    oldBalance = round(float(balance.text.replace(',','')), 2)

    TableSwitch(driver, tableNum, gameTable, multi_testcase['switch table'], multiTables[0])
    CancelBet(driver, game, gameTable, chip, tableNum, betArea, multi_testcase['cancel bet'], multiTables[1])
    BetSuccessful(driver, game, gameTable, tableNum, betArea, multi_testcase['bet successful'], multiTables[3])
    BalanceDeduction(driver, gameTable, oldBalance, chip, multi_testcase['balance deduction'], multiTables[4])
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    PlaceBet(driver, betPlaced, 'Single Bet Assertion', gameTable, str(chip), multi_testcase['single bet'], multiTables[5])
    NoMoreBets(driver, gameTable, tableNum, multi_testcase['no more bets'], multiTables[7])
    ClosedBetTimer(driver, game, gameTable, tableNum, betArea, multi_testcase['bet in closed betting timer'], multiTables[8])
    Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, multi_testcase['payout'], multiTables[9], chip)

    if game == 'BACCARAT' or game == 'DT': b, r = gameResult(driver, game, gameTable, tableNum)

    EmptyBetarea(driver, gameTable, chip, multi_testcase['empty betareas on new round'], multiTables[12], betPlaced)

def multipleBet(driver, game, gameTable, tableNum, chip, balance, betArea):
    displayToast(driver, 'MULTIPLE BET')
    print('\n')
    printText('title', 'TEST: MULTIPLE BET')

    oldBalance = round(float(balance.text.replace(',','')), 2)
    BettingTimer(driver, tableNum, timer=14)

    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tableNum)
    betarea = findModElements(driver, 'MULTIPLE BETTINGAREA', game, table=tableNum)
    for bet in betarea: bet.click()
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tableNum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tableNum, time=10)
    assertion(driver,'Bet Successful Assertion', validate, True, operator.eq, multi_testcase['bet successful'], multiTables[3], gameTable)
            
    for bets in range(len(betarea)): betamount = chip * (bets+1)

    BalanceDeduction(driver, gameTable, oldBalance, betamount, multi_testcase['balance deduction'], multiTables[4])
    for bet in betarea: PlaceBet(driver, bet, 'Multiple Bet Assertion', gameTable, str(chip), multi_testcase['multiple bet'], multiTables[6])
    NoMoreBets(driver, gameTable, tableNum, multi_testcase['no more bets'], multiTables[7])
    ClosedBetTimer(driver, game, gameTable, tableNum, betArea, multi_testcase['bet in closed betting timer'], multiTables[8])
    Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea, multi_testcase['payout'], multiTables[9], betamount)

    # if game == 'BACCARAT' or game == 'DT': b, r = gameResult(driver, game, gameTable, tableNum)

    # for bet in betarea:
    #     EmptyBetarea(driver, gameTable, chip, multi_testcase['empty betareas on new round'], multiTables[12], bet)

    # for bets in range(len(betarea)): EmptyBetarea(driver, game, gameTable, tableNum, bets, chip, multi_testcase['empty betareas on new round'], multiTables[12])


def BetRecord(driver, game, gameTable, selectedGame, shoe, b, r):
    card_dict = locator("CARDS", game)
    betarea = list(locator("MULTI BETTINGAREA", game).keys())
    blue_points = red_points = list_value = 0
    index = 1
    navigateSettings(driver, 'HISTORY')

    result = findElements(driver, 'MULTI HISTORY', 'RESULTS')
    for x in range(len(result)):
        tableNum = locator("MULTI HISTORY","RESULTS")+str(locator('MULTI HISTORY', 'CON'))+str(x+1)+")"
        if shoe in result[x].text:
            waitModClickable(driver, 'MULTI HISTORY', 'BET CODE', table=tableNum)
            
            cards = findElements(driver, 'MULTI HISTORY', 'CARD RESULT')
            
            for x in range(len(cards)):
                attrib = cards[x].get_attribute('class')
                start = attrib.find('base64,') + 7
                base64_string = attrib[start:]

                card_value = textDecoder(index, gameTable[selectedGame], base64_string, 'history', game)

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

    assertion(driver, f'Bet Result Assertion [{betarea[0]}]', b, blue_points, operator.eq, multi_testcase['record history assert'], multiTables[15], gameTable[selectedGame])
    assertion(driver, f'Bet Result Assertion [{betarea[1]}]', r, red_points, operator.eq, multi_testcase['record history assert'], multiTables[15], gameTable[selectedGame])

    waitClickable(driver, 'MULTI HISTORY', 'CLOSE')

def gameResult(driver, game, gameTable, tableNum):
    waitModElement(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
    card_dict = locator("CARDS", game)
    betarea = list(locator("MULTI BETTINGAREA", game).keys())
    list_name = ''
    blue_points = red_points = list_value = 0
    index = 1

    cards = findModElements(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
    for card in cards:
        card_value = decodeBase64(index, card, gameTable, game)
        
        for key, value in card_dict.items():
            if card_value in key:
                list_name = key
                list_value = value
                break

        if game == 'BACCARAT':
            blue_points += list_value if index < 4 else 0
            red_points += list_value if index > 3 else 0
            if index != 3 and index != 6:
                assertion(driver, f'Flip Cards Assertion', f'{list_name}', 'e', operator.ne, multi_testcase["flipped cards"], multiTables[16], gameTable)
        if game == 'DT':
            blue_points += list_value if index == 1 else 0
            red_points += list_value if index == 2 else 0
            assertion(driver, f'Flip Cards Assertion', f'{list_name}', 'e', operator.ne, multi_testcase["flipped cards"], multiTables[16], gameTable)
        index += 1

    if game == 'BACCARAT':
        blue_points %= 10 
        red_points %= 10

    actual_bpoints = int(findModElement(driver, 'MULTI TABLE', 'CARD POINTS 1', table=tableNum).text[-2:].replace(' ', ''))
    actual_rpoints = int(findModElement(driver, 'MULTI TABLE', 'CARD POINTS 2', table=tableNum).text[-2:].replace(' ', ''))

    assertion(driver, f'Bet Result Assertion [{betarea[0]}]', actual_bpoints, blue_points, operator.eq, multi_testcase["card result"], multiTables[15], gameTable)
    assertion(driver, f'Bet Result Assertion [{betarea[1]}]', actual_rpoints, red_points, operator.eq, multi_testcase["card result"], multiTables[15], gameTable)

    return actual_bpoints, actual_rpoints

# ASSERTION METHODS