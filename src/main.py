from src.modules import *
from src.helpers import *

test_case = {
    "Table Switch Assertion": [], 
    "Below Minimum Limit": [], 
    "Over Maximum Limit": [], 
    "Bet Placed Assertion": [], 
    "Balance deduction after confirming bet": [], 
    "Payout Assertion: Balance after win/lose bet": [],
    "Bet Limit Assertion": []
}

data = {
    "Username": "QAUSERTEST1128",
    "Bet code": "8",
    "Chip Value": "201"
}

sampleData = {
    "sample1": [],
    "sample2": [],
    "sample3": [],
    "sample4": [],
    "sample5": [],
    "sample6": [],
    "sample7": [],
}
def playMulti(driver, game, test, report):
    navigateMulti(driver)
    playerBalance = findElement(driver, "MULTI", "USER BALANCE")
    oldBalance = round(float(playerBalance.text.replace(',','')), 2)

    elements = findElements(driver, "MULTI", "MULTI TABLE")
    gameTable = locator(game)
    
    failedTables = []

    try:
        for selectedGame in range(len(gameTable)):
            printText('title', f"Finding: {gameTable[selectedGame]}")
            game_found = False
            for i in range(len(elements)):
                name = elements[i]
                tableNum = locator("MULTI TABLE","MAIN")+str(i+1)+")"

                while name.text == '': continue

                if gameTable[selectedGame] not in name.text:
                    print("Table is not",gameTable[selectedGame],"\nSwitching Table...")
                    waitModClickable(driver, "MULTI", "TABLE SWITCH", table=tableNum)
                    select = findElements(driver, "MULTI", "MINI TABLECARD")
                    for x in range(len(select)):
                        selectText = select[x]
                        driver.execute_script("arguments[0].scrollIntoView();", selectText)
                        if gameTable[selectedGame] in selectText.text:
                            selectText.click()
                            game_found = True
                            break
                        else: continue
                    # finding in mini side tables
                    elements = findElements(driver, "MULTI", "MULTI TABLE")
                    name = elements[i]
                    if gameTable[selectedGame] not in name.text and game_found == False:
                        waitClickable(driver, "MULTI", "CLOSE SIDETABLE")
                    if game_found: break
                else:
                    print("Table Found")
                    game_found = True
                    break 

            if game_found: #PLACE BET
                intoText = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)
                while intoText.text == '': continue

                assertion('Table Switch Assertion', intoText, gameTable[selectedGame], operator.ne, test_case["Table Switch Assertion"], failedTables, gameTable, selectedGame)
                
                randomize = locator("MULTI BETTINGAREA",f"{game}")
                betAreas = list(randomize.keys())
                if 'SUPER SIX' in betAreas: betAreas.remove('SUPER SIX')
                betArea = random.choice(betAreas)

                displayToast(driver, f'TEST: {test}')
                
                if test == "BET LIMIT":
                    multiBetLimit(driver, game, gameTable, failedTables, selectedGame, tableNum, intoText, betArea, 
                        test_case["Below Minimum Limit"], 
                        test_case["Over Maximum Limit"], 
                        test_case["Bet Placed Assertion"])
                elif test == "PLACE BET":
                    multiPlaceSingle(driver, game, tableNum, betArea, failedTables, gameTable, selectedGame, 
                        test_case["Bet Placed Assertion"], 
                        test_case["Bet Limit Assertion"], 
                        test_case["Balance deduction after confirming bet"], 
                        test_case["Payout Assertion: Balance after win/lose bet"])
                elif test == "PLACE ALL":
                    printText('title','Place bet in all betting area')
                    break
                elif test == "SUPER SIX":
                    betArea = test
                    printText('title','Place Bet On Super Six')
                    printTexts('body', 'Table Name: ', intoText.text)

                    actions = ActionChains(driver)
                    repeat = True
                    while repeat:
                        chips = findElements(driver, "MULTI", "CHIP VALUE")
                        for chip in range(len(chips)):
                            selectedChip = chips[chip]
                            actions.move_to_element(selectedChip).perform()
                            
                            if chips[chip].text == data[1]:
                                selectedChip.click()
                                break
                            if chip >= 9: editChips(driver, value=201)
                        break
                    waitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

                    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
                    intoInt = int(time.text)

                    if intoInt < 5:
                        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
                        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
                    printTexts('body', 'PLACE BET: ', 'SUPER SIX')
                    repeat = True
                    while repeat: 
                        try:
                            findModElement(driver, "MULTI BUTTON", "SUPER SIX", click=True, table=tableNum)
                            findModElement(driver, "MULTI BETTINGAREA", game, betArea, click=True, table=tableNum)
                            repeat = False
                        except: continue
                            
                    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)
                    waitModText(driver, "MULTI", "VALIDATION", text='Bet Successful!', table=tableNum, time=10)
                    assertBetPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
                    getText = assertBetPlaced.text.split('\n')
                    valuePlaced = getText[-1]
                    assertion('Bet Placed Assertion', valuePlaced, '', operator.ne, test_case["Bet Placed Assertion"], failedTables, gameTable, selectedGame)

                    assertBetLimit = int(valuePlaced) * int(locator("PAYOUT", "BACCARAT", "SUPER SIX"))
                    assertion('Bet Limit Assertion', assertBetLimit, int(locator("BET LIMIT", "MAX")), operator.le, test_case["Bet Limit Assertion"], failedTables, gameTable, selectedGame)

                    deductedBalance = oldBalance - int(valuePlaced)
                    assertWinAdded(driver, game, test_case["Payout Assertion: Balance after win/lose bet"], tableNum, betArea, playerBalance, oldBalance, deductedBalance, failedTables, gameTable, selectedGame, valuePlaced)

                else: print("BET LIMIT, PLACE BET, PLACE ALL, SUPER SIX")

            if not game_found:
                printText('failed', f'Game not found: {gameTable[selectedGame]}')
            printText('body', '\n**************************')

            elements = findElements(driver, "MULTI", "MULTI TABLE")
        gameTable = locator(game)

        # REPORT STATUS
        reportSheet(*test_case.values())

        for i, key in enumerate(test_case):
            reportSheet(game, report, failedTables, test_case[key])

        waitClickable(driver, "NAV", "FEATURED")
        waitElement(driver, "LOBBY", "MAIN")
    except Exception as e:
        print(f'FAILED: {str(e)}')
        driver.save_screenshot(f"screenshots/{gameTable[selectedGame]}_{date.today()}_{datetime.now().second}.png")

def multiBetLimit(driver, game, gameTable, failedTables, selectedGame, tableNum, intoText, betArea, belowLimit, overLimit, betPlaced):
    printText('title', 'Minimum Bet Limit')
    printTexts('body', 'Table Name: ', intoText.text)
    actions = ActionChains(driver)
    repeat = True
    while repeat:
        chips = findElements(driver, "MULTI", "CHIP VALUE")
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            actions.move_to_element(selectedChip).perform()
                            
            if chips[chip].text == "1":
                selectedChip.click()
                break
            if chip >= 9: editChips(driver, value=1)
        break
                    
    waitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)
    if intoInt < 5:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    printTexts('body', 'PLACE BET: ', betArea)        
    waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)
                    
                    # assert validation displayed == 'Below Minimum Limit'
    validate = waitModElement(driver, "MULTI", "VALIDATION", table=tableNum)
    assertion('Below Minimum Assertion', validate.text, 'Below Minimum Limit', operator.eq, belowLimit, failedTables, gameTable, selectedGame)
                    
    # //////////////////////////////////////////////////////////

    printText('title', 'Maximum Bet Limit')
                                                
    repeat = True
    while repeat:
        chips = findElements(driver, "MULTI", "CHIP VALUE")
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            actions.move_to_element(selectedChip).perform()
                            
            if chips[chip].text == "10K":
                selectedChip.click()
                break
            if chip >= 9: editChips(driver, value=10001)
        break

    waitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)
    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)

    if intoInt < 5:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    printTexts('body', 'PLACE BET: ', betArea)
                                                            
    repeat = True
    while repeat:
        try:
            waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
            assertOverLimit = waitModText(driver, "MULTI", "VALIDATION", table=tableNum, time=1, text="Over Maximum Limit!",game=game)
            if assertOverLimit:
                assertion('Over Limit Assertion', assertOverLimit, True, operator.eq, overLimit, failedTables, gameTable, selectedGame)
                repeat = False
        except: repeat = True

    waitModClickable(driver, "MULTI BUTTON", "CONFIRM BUTTON", table=tableNum)
    waitModText(driver, "MULTI", "VALIDATION", text='Bet Successful!', table=tableNum, time=10)
    assertBetPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    getText = assertBetPlaced.text.split('\n')
    valuePlaced = getText[-1]

    assertion('Bet Placed Assertion', valuePlaced, '', operator.ne, betPlaced, failedTables, gameTable, selectedGame)

    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    waitElement(driver, "MULTI", "TOAST")


def multiPlaceSingle(driver, game, tableNum, betArea, failedTables, gameTable, selectedGame, betPlaced, betLimit, betDeducted, betAdded):
    printText('title', 'Place Single Bet')

    playerBalance = findElement(driver, "MULTI", "USER BALANCE")
    oldBalance = round(float(playerBalance.text.replace(',','')), 2)

    # PLACE BET
    actions = ActionChains(driver)
    repeat = True
    while repeat:
        chips = findElements(driver, "MULTI", "CHIP VALUE")
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            actions.move_to_element(selectedChip).perform()
            
            if chips[chip].text == "201":
                selectedChip.click()
                break
            if chip >= 9: editChips(driver, value=201)
        break

    waitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)

    if intoInt < 5:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    printTexts('body', 'PLACE BET: ', betArea)
    waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)
    waitModText(driver, "MULTI", "VALIDATION", text='Bet Successful!', table=tableNum, time=10)

    assertBetPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tableNum)
    getText = assertBetPlaced.text.split('\n')
    valuePlaced = getText[-1]
    assertion('Bet Placed Assertion', valuePlaced, '', operator.ne, betPlaced, failedTables, gameTable, selectedGame)

    assertBetLimit = int(valuePlaced) * int(locator("PAYOUT", game, betArea))
    assertion('Bet Limit Assertion', assertBetLimit, int(locator("BET LIMIT", "MAX")), operator.le, betLimit, failedTables, gameTable, selectedGame)

    deductedBalance = oldBalance - 201
    assertion('Balance Deducted Assertion', round(deductedBalance, 2), round(float(playerBalance.text.replace(',', '')), 2), operator.eq, betDeducted, failedTables, gameTable, selectedGame)
    
    assertWinAdded(driver, game, betAdded, tableNum, betArea, playerBalance, oldBalance, deductedBalance, failedTables, gameTable, selectedGame, 201)

def sideBar(driver, game):
    waitElement(driver, "PRE LOADING")
    waitElement(driver, "LOBBY", "MAIN")
    execJS(driver, 'noFullScreen();')
    waitClickable(driver, "LOBBY", "ENTER TABLE")
    waitElement(driver, "INGAME", "MAIN")
    timer = findElement(driver, "INGAME", "TIMER")
    if timer.text == 'CLOSED' or int(timer.text) < 5:
        waitElement(driver, "INGAME", "RESULT")
        waitElementInvis(driver, "INGAME", "RESULT")
    
    waitClickable(driver, "BETTING AREA", game)
    findElement(driver, "INGAME", "CONFIRM", click=True)
    waitText(driver, "INGAME", "VALIDATION", text='Bet Successful')

    waitClickable(driver, "INGAME", "SIDEBET")
    waitElement(driver, "SIDEBET", "MAIN")
    waitElement(driver, "SIDEBET", "LOBBY")

    tables = findElements(driver, "SIDEBET", "TABLES")