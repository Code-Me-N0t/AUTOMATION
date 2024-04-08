from src.modules import*
from src.helpers import*

multi_testcase = {
    "switch table": [],
    "cancel bet": [],
    "balance deduction": [],
    "single bet": [],
    "multiple bet": [],
    "all bet": [],
    "bet successful": [],
    "no more bets": [],
    "bet in closed betting timer": [],
    "payout": [],
    "empty betareas on new round": [],
    "bet on super 6": [],
    "record history assert": [],
    "bet within bet pool but in below bet limit": [],
    "ask b/p": [],
    "card result": [],
    "flipped cards": [],
    "all in": [],
}

data = {
    "username": env("USER_NAME"),
    "bet limit": "269",
    "chip value": 201
}

multiTables = [[] for _ in range(len(multi_testcase))]

def PlayMulti(driver, game, report):
    navigateTab(driver, "MULTI")
    gameTable = locator(game)
    actions = ActionChains(driver)

    try:
        for selectedGame in range(len(gameTable)):
            printText('title', f"Finding: {gameTable[selectedGame]}")
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
                balance = findElement(driver, "MULTI", "USER BALANCE")
                oldBalance = round(float(balance.text.replace(',','')), 2)

                printText('title', f'Table {gameTable[selectedGame]} found')
                
                randomize = locator("MULTI BETTINGAREA",f"{game}")
                betAreas = list(randomize.keys())
                if 'SUPER SIX' in betAreas: betAreas.remove('SUPER SIX')
                betArea = random.choice(betAreas)

                EditChips(driver, actions, chipValue=data["chip value"])
                BettingTimer(driver, tableNum)

                # TEST CASES
                TableSwitch(driver, tableNum, gameTable[selectedGame])
                CancelBet(driver, game, gameTable[selectedGame], tableNum, betArea)
                BetSuccessful(driver, game, gameTable[selectedGame], tableNum, betArea)
                BalanceDeduction(driver, gameTable[selectedGame], oldBalance)
                SingleBet(driver, game, gameTable[selectedGame], tableNum, betArea)
                NoMoreBets(driver, gameTable[selectedGame], tableNum)
                ClosedBetTimer(driver, game, gameTable[selectedGame], tableNum, betArea)
                Payout(driver, game, gameTable[selectedGame], tableNum, balance, oldBalance, betArea)

                if game == 'BACCARAT' or game == 'DT': gameResult(driver, game, gameTable[selectedGame], tableNum)

                waitModElementInvis(driver, "MULTI TABLE", "RESULT TITLE", table=tableNum)

                # betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
                # getText = betPlaced.text.split('\n')
                # valuePlaced = getText[-1]
                # assertion(driver,'Empty Betarea Assertion', 
                #         valuePlaced, 
                #         str(data["chip value"]), 
                #         operator.ne, 
                #         multi_testcase["empty betareas on new round"], 
                #         multiTables[10], 
                #         gameTable
                # )                
                
            if not game_found: printText('failed', f'Table {gameTable[selectedGame]} not found')
            
            elements = findElement(driver, "MULTI", "MULTI TABLE")
        printText('body', '\n************************** end of code **************************')
        # report
        multiReportSheet(report, game, multiTables, *multi_testcase.values())

        waitClickable(driver, "NAV", "FEATURED")
        waitElement(driver, "LOBBY", "MAIN")
        gameTable = locator(game)
    except Exception as e:
        print(f'[ERROR]: {str(e)}')
        driver.save_screenshot(f"screenshots/{gameTable[selectedGame]}_{date.today()}_{datetime.now().second}.png")

def gameResult(driver, game, gameTable, tableNum):
    
    waitModElement(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
    card_dict = locator("CARDS", game)
    betarea = list(locator("MULTI BETTINGAREA", game).keys())
    list_name = ''
    blue_points = red_points = list_value = 0
    index = 1

    cards = findModElements(driver, 'MULTI TABLE', 'RESULT TITLE', table=tableNum)
    for card in cards:
        card_value = decodeBase64(index, card, gameTable)
        
        for key, value in card_dict.items():
            if card_value in key:
                list_name = key
                list_value = value
                break
        
        # list_index = card_names.index(list_name)
        # print(f'Card Value: {card_value}')
        # print(f'Card Index: {list_index}')
        # print(f'Card Name: {list_name}')
        # print(f'Card Value: {list_value}\n')

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

    assertion(driver, f'{betarea[0]} Result Assertion', actual_bpoints, blue_points, operator.eq, multi_testcase["card result"], multiTables, gameTable)
    assertion(driver, f'{betarea[1]} Result Assertion', actual_rpoints, red_points, operator.eq, multi_testcase["card result"], multiTables, gameTable)

def sample(driver):
    cards = locator("CARDS", 'BACCARAT')
    card_names = list(locator("CARDS", 'BACCARAT').keys())
    card_value = 'O'
    list_name = ''
    list_value = 0
    
    for key, value in cards.items():
        if card_value in key:
            list_name = key
            list_value = value

    list_index = card_names.index(list_name) #get the value name index
    print(f'List Index: {list_index}')
    print(f'List Name: {list_name}')
    print(f'List Value: {list_value}')
    # list_value = cards[5].index(str(card_value)) #get the value index
    # print(f'List Value: {list_value}')
    # num_card_value = cards[list_index][list_value]
    # print(list_index, num_card_value)

    # key = cards[]

    # card_point = cards
    # print(card_point)

# ASSERTION METHODS
def TableSwitch(driver, tableNum, gameTable):
    tableName = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)
    while tableName.text == '': continue
    assertion(driver,'Switch Table Assertion', 
              gameTable,
              tableName.text, 
              operator.eq,
              multi_testcase["switch table"], 
              multiTables[0], 
              gameTable
    )
    
def CancelBet(driver, game, gameTable, tableNum, betArea):
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum)
    findModElement(driver, 'MULTI BUTTON', 'CANCEL', click=True, table=tableNum)
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    getText = betPlaced.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Cancel Bet Assertion', 
              valuePlaced, 
              str(data["chip value"]), 
              operator.ne, 
              multi_testcase["cancel bet"], 
              multiTables[1], 
              gameTable
    )
    
def BalanceDeduction(driver, gameTable, oldBalance):
    for i in range(30): newbalance = findElement(driver, "MULTI", "USER BALANCE")
    deductedBalance = oldBalance - data['chip value']
    assertion(driver,'Balance Deducted Assertion', 
              round(deductedBalance, 2), 
              round(float(newbalance.text.replace(',','')), 2), 
              operator.eq, 
              multi_testcase['balance deduction'], 
              multiTables[2], 
              gameTable
    )

def SingleBet(driver, game, gameTable, tableNum, betArea):
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    getText = betPlaced.text.split('\n')
    valuePlaced = getText[-1]
    assertion(driver,'Single Bet Assertion', 
              valuePlaced, 
              str(data['chip value']), 
              operator.eq, 
              multi_testcase['single bet'], 
              multiTables[3], 
              gameTable
    )
    
def BetSuccessful(driver, game, gameTable, tableNum, betArea):
    waitModClickable(driver, 'MULTI BETTINGAREA', f'{game}', f'{betArea}', table=tableNum)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tableNum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tableNum, time=10)
    assertion(driver,'Bet Successful Assertion', 
              validate, 
              True, 
              operator.eq, 
              multi_testcase["bet successful"], 
              multiTables[6], 
              gameTable
    )

def NoMoreBets(driver, gameTable, tableNum):
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='No More Bets!', table=tableNum)
    assertion(driver,'No More Bets Assertion', 
              validate, 
              True, 
              operator.eq, 
              multi_testcase['no more bets'], 
              multiTables[7], 
              gameTable
    )

def ClosedBetTimer(driver, game, gameTable, tableNum, betArea):
    waitModElement(driver, "SIDEBET", "RESULT", table=tableNum)
    try: 
        waitModClickable(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
        validate = False
    except ElementClickInterceptedException:validate = True
    assertion(driver,'Bet in Closed Betting Timer', 
              validate, 
              True, 
              operator.eq, 
              multi_testcase['bet in closed betting timer'], 
              multiTables[8], 
              gameTable
    )

def Payout(driver, game, gameTable, tableNum, balance, oldBalance, betArea):
    newBalance = round(float(balance.text.replace(',','')), 2)
    deductedBalance = oldBalance - data["chip value"]
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    repeat = True
    while repeat:
        assertWin = waitModElement(driver, "MULTI", "VALIDATION", table=tableNum)
        if assertWin.text != 'No More Bets!' and assertWin.text != '': repeat=False
    payout = locator("PAYOUT", f"{game}", f"{betArea}")
    # print(assertWin.text)
    # printTexts('body', 'Payout: ', f'1:{payout}')
    if "Win" in assertWin.text:
        comPay = float(data["chip value"]) * payout
        addedBalance = comPay + newBalance
        validateAddedBalance = oldBalance - (float(data["chip value"])-comPay)
        assertion(driver,'Win Assertion', 
                  round(addedBalance, 2), 
                  round(validateAddedBalance, 2), 
                  operator.eq, 
                  multi_testcase["payout"], 
                  multiTables[9], 
                  gameTable
    )
    else: assertion(driver,'Lose Assertion', 
                    round(newBalance, 2), 
                    round(deductedBalance, 2), 
                    operator.eq, 
                    multi_testcase["payout"], 
                    multiTables[9], 
                    gameTable
    )