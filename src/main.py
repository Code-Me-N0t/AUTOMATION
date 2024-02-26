from src.modules import *
from src.helpers import *

def playMulti(driver, game, test, report):
    waitElement(driver, "LOBBY", "MAIN")
    waitElement(driver, "LOBBY", "MENU")
    waitClickable(driver, "NAV", "MULTI")
    waitElement(driver, "MULTI", "MAIN")
    elements = findElements(driver, "MULTI", "MULTI TABLE")
    gameTable = locator(game)
    assertTableSwitchStatus = [] 
    assertBelowLimitStatus = [] 
    assertOverLimitStatus = [] 
    assertBetPlacedStatus = [] 
    assertDeductedBalanceStatus = [] 
    assertAddedBalanceStatus = []

    for selectedGame in range(len(gameTable)):
        printText('title', f"Finding: {gameTable[selectedGame]}")
        game_found = False

        for i in range(len(elements)):
            tableNum = locator("MULTI TABLE","TABLE NUMBER")+str(i+1)+")"

            name = elements[i]
            printText('passed', f'Table: {(i+1)}')

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
                        print("Table Found")
                        break
                    else: continue
                # finding in mini side tables

                elements = findElements(driver, "MULTI", "MULTI TABLE")
                name = elements[i]

                if gameTable[selectedGame] not in name.text and game_found == False:
                    waitClickable(driver, "MULTI", "CLOSE SIDETABLE")

                if game_found: break

            else:
                game_found = True
                break 

        if game_found: #PLACE BET

            intoText = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)

            assertTableSwitch(gameTable, assertTableSwitchStatus, selectedGame, intoText)
            randomize = locator("MULTI BETTINGAREA",f"{game}")
            betArea = random.choice(list(randomize))
            if test == "BET LIMIT":
                multiBetLimit(driver, game, assertBelowLimitStatus, assertOverLimitStatus, tableNum, intoText, betArea)

            elif test == "PLACE BET":
                multiPlaceSingle(driver, game, assertBetPlacedStatus, assertDeductedBalanceStatus, assertAddedBalanceStatus, tableNum, betArea)
            elif test == "PLACE ALL":
                print("Do Something")
            elif test == "SUPER SIX" and game == 'BACCARAT':
                betArea = locator("MULTI BETTINGAREA","BACCARAT","SUPER SIX")
                printText('title','Place Bet On Super Six')

                chips = findElements(driver, "MULTI", "CHIP VALUE")
                try:
                    for chip in range(len(chips)):
                        selectedChip = chips[chip]
                        if chips[chip].text == "201":
                            break
                except:
                    editChips(driver, value=201)
                selectedChip.click()

                WaitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

                time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
                intoInt = int(time.text)

                if intoInt < 5:
                    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
                    waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

                waitModClickable(driver, "MULTI BUTTON", "SUPER SIX", table=tableNum)

                printTexts('body', 'PLACE BET: ', 'SUPER SIX')
                waitModClickable(driver, betArea, table=tableNum)
                findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)

            else: print("BET LIMIT, PLACE BET, PLACE ALL, SUPER SIX")

        if not game_found:
            printText('failed', f'Game not found: {gameTable[selectedGame]}')
        printText('body', '\n**************************\n')

        elements = findElements(driver, "MULTI", "MULTI TABLE")
    gameTable = locator(game)

    # REPORT STATUS
    reportSheet(game, report, gameTable, assertTableSwitchStatus, assertBelowLimitStatus, assertOverLimitStatus, assertBetPlacedStatus, assertDeductedBalanceStatus, assertAddedBalanceStatus, selectedGame)

    waitClickable(driver, "NAV", "FEATURED")
    waitElement(driver, "LOBBY", "MAIN")

def multiBetLimit(driver, game, assertBelowLimitStatus, assertOverLimitStatus, tableNum, intoText, betArea):
    printText('title', 'Minimum Bet Limit')
    printTexts('body', 'Table Name: ', intoText.text)

    chips = findElements(driver, "MULTI", "CHIP VALUE")
    try:
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            if chips[chip].text == "1":
                printTexts('body', "TRY: ", "FOUND CHIP 1")
                break
    except:
        printTexts('body', "CATCH: ", "EDIT CHIP")
        editChips(driver, value=1)
    selectedChip.click()

    WaitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)
    if intoInt < 10:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    printTexts('body', 'PLACE BET: ', betArea)
                                            
    waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)

                                # assert validation displayed == 'Below Minimum Limit'
    assertBelowLimit(driver, tableNum, assertBelowLimitStatus)

                                # //////////////////////////////////////////////////////////

    printText('title', 'Maximum Bet Limit')
                                
    chips = findElements(driver, "MULTI", "CHIP VALUE")
    try:
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            if chips[chip].text == "10K":
                printTexts('body', "TRY: ", "FOUND CHIP 10K")
                break
    except:
        printTexts('body', "CATCH: ", "EDIT CHIP")
        editChips(driver, value=10001)
    selectedChip.click()

    WaitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)

    if intoInt < 10:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    printTexts('body', 'PLACE BET: ', betArea)
                                            
    repeat = True
    while repeat:
        try:
            waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
            assertOverLimit = waitModText(driver, "MULTI", "VALIDATION", table=tableNum, time=1, text="Over Maximum Limit!",game=game)

            if assertOverLimit:
                assertAboveLimit(assertOverLimitStatus, assertOverLimit)
                repeat = False
        except: repeat = True

    waitModClickable(driver, "MULTI BUTTON", "CONFIRM BUTTON", table=tableNum)
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    waitElement(driver, "MULTI", "TOAST")

def multiPlaceSingle(driver, game, assertBetPlacedStatus, assertDeductedBalanceStatus, assertAddedBalanceStatus, tableNum, betArea):
    printText('title', 'Place Single Bet')

    playerBalance = findElement(driver, "MULTI", "USER BALANCE")
    oldBalance = round(float(playerBalance.text.replace(',','')), 2)
    # print(oldBalance)

    # PLACE BET
    chips = findElements(driver, "MULTI", "CHIP VALUE")
    try:
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            if chips[chip].text == "201":
                break
    except:
        editChips(driver, value=201)
    selectedChip.click()

    WaitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)

    if intoInt < 5:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    printTexts('body', 'PLACE BET: ', betArea)
    waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)
                    
    assertBetPlaced(driver, assertBetPlacedStatus, tableNum)

    deductedBalance = assertDeductedBalance(assertDeductedBalanceStatus, playerBalance, oldBalance)

    assertWinAdded(driver, game, assertAddedBalanceStatus, tableNum, betArea, playerBalance, oldBalance, deductedBalance)

def betOnRoulette(driver):
    waitElement(driver, "LOBBY", "MAIN", time=600)
    waitElement(driver, "LOBBY", "MENU")
    waitClickable(driver, "NAV", "ROULETTE")

    elements = findElements(driver, "LOBBY", "TABLE")

    for i in range(len(elements)):
        table = elements[i]
        if "P8" in table.text:
            table.click()
            break
        elements = findElements(driver, "LOBBY", "TABLE")

    execJS(driver, 'noFullScreen();')
    sleep(2)
    chips = findElements(driver, "MULTI", "CHIP VALUE")
    for chip in range(len(chips)):
        chipValue = chips[chip]
        if "100" in chipValue.text:
            chipValue.click()
            break

    timer = findElement(driver, "ROULETTE", "TIMER")
    if timer.text == 'CLOSED' or int(timer.text) < 10:
        waitText(driver, "ROULETTE", "TIMER", text='25')
    
    betArea = findElements(driver, "ROULETTE", "BET AREA")
    for i in range(len(betArea)):
        singlebet = locator("ROULETTE", "BET AREA") + str(i+1)
        driver.find_element(By.CSS_SELECTOR, singlebet).click()

        if i == 23: 
            waitClickable(driver, "ROULETTE", "CONFIRM")
            break
        betArea = findElements(driver, "ROULETTE", "BET AREA")

    # waitElement(driver, "ROULETTE", "RESULT BOARD")
    # result = waitElement(driver, "ROULETTE", "TOAST")
    # print(result.text)
    print("end of code")