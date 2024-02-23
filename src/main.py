from src.modules import *
from src.helpers import *

def playMulti(driver, game, test, report):
    try:
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
        status = "PASSED"

        for selectedGame in range(len(gameTable)):
            print(Fore.CYAN + "Finding: ", gameTable[selectedGame] + Fore.RESET)
            game_found = False

            for i in range(len(elements)):
                tableNum = locator("MULTI TABLE","TABLE NUMBER")+str(i+1)+")"

                name = elements[i]
                print(Fore.GREEN + "Table:", (i+1), Fore.RESET)

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
                            print(Fore.RESET+"Table Found\nTable Switched")
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
                # finding in multi tables

            if game_found: #PLACE BET

                intoText = findModElement(driver, "MULTI TABLE", "TABLE NAME", table=tableNum)

                assertTableSwitch(gameTable, assertTableSwitchStatus, selectedGame, intoText)

                randomize = locator("MULTI BETTINGAREA",f"{game}")
                betArea = random.choice(list(randomize))
                
                if test == "BET LIMIT":
                    multiBetLimit(driver, game, assertBelowLimitStatus, assertOverLimitStatus, tableNum, intoText, betArea)
                elif test == "PLACE BET":
                    print(Fore.CYAN+"\nPlace Single Bet"+Fore.RESET)

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

                    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
                    intoInt = int(time.text)

                    if intoInt < 5:
                        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
                        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

                    print("PLACE BET: "+Fore.LIGHTBLACK_EX+betArea+Fore.RESET)
                    waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
                    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)
                    
                    assertBetPlaced = waitModText(driver, "MULTI", "VALIDATION", text='Bet Successful!', table=tableNum, time=10)
                    
                    try: 
                        assert assertBetPlaced
                        assertBetPlacedStatus.append("PASSED")
                        print(f"Bet Placed Assertion: {Fore.RED}FAILED{Fore.RESET}")
                    except AssertionError:
                        print(f"Bet Placed Assertion: {Fore.RED}FAILED{Fore.RESET}")
                        assertBetPlacedStatus.append("FAILED")

                    deductedBalance = oldBalance - 201

                    try:
                        assert round(deductedBalance, 2) == round(float(playerBalance.text.replace(',', '')), 2)
                        print(f"Balance Deducted Assertion: {Fore.LIGHTBLACK_EX}PASSED{Fore.RESET}")
                        assertDeductedBalanceStatus.append("PASSED")
                    except AssertionError:
                        print(f"Balance Deducted Assertion: {Fore.RED}FAILED{Fore.LIGHTBLACK_EX}\n{round(deductedBalance,2):.2f} != {playerBalance.text.replace(',','')}{Fore.RESET}")
                        assertDeductedBalanceStatus.append("FAILED")

                    newBalance = round(float(playerBalance.text.replace(',','')), 2)

                    # print("Old Balance: ", oldBalance)
                    # print("New Balance: ", newBalance)
                    # print("Computed Balance: ", deductedBalance)

                    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
                    assertWin = waitElement(driver, "MULTI", "TOAST")
                    payout = locator("PAYOUT", f"{game}", f"{betArea}")
                    print(assertWin.text)
                    print(f"Payout: {Fore.LIGHTBLACK_EX}1:{payout}{Fore.RESET}")

                    if "Win" in assertWin.text:
                        
                        addedBalance = (201 * payout) + newBalance
                        validateAddedBalance = oldBalance - (201-(201*payout))
                        print("Added Balance: ", addedBalance)
                        try:
                            assert round(addedBalance, 2) == round(validateAddedBalance, 2)
                            print(f"Won Assertion: {Fore.LIGHTBLACK_EX}PASSED{Fore.RESET}\n{round(addedBalance, 2)} == {round(validateAddedBalance, 2)}")
                            assertAddedBalanceStatus.append("PASSED")
                        except AssertionError:
                            print(f"Won Assertion: {Fore.RED}FAILED{Fore.RESET}\n{round(addedBalance, 2)} != {round(validateAddedBalance, 2)}")
                            assertAddedBalanceStatus.append("FAILED")
                    else:
                        try:
                            assert round(deductedBalance, 2) == round(newBalance, 2)
                            print(f"Lose Assertion: {Fore.LIGHTBLACK_EX}PASSED{Fore.RESET}")
                            assertAddedBalanceStatus.append("PASSED")
                        except AssertionError:
                            print(f"Lose Assertion: {Fore.RED}FAILED{Fore.LIGHTBLACK_EX}\n{round(deductedBalance, 2)} != {round(newBalance, 2)}{Fore.RESET}")
                            assertAddedBalanceStatus.append("FAILED")

            if not game_found:
                print(Fore.RED+"Game not found:", gameTable[selectedGame]+Fore.RESET)
            print(Fore.LIGHTBLACK_EX+"**************************")

        # REPORT STATUS
        reportSheet(game, report, gameTable, assertTableSwitchStatus, assertBelowLimitStatus, assertOverLimitStatus, assertBetPlacedStatus, assertDeductedBalanceStatus, assertAddedBalanceStatus, selectedGame)

        waitClickable(driver, "NAV", "FEATURED")
        waitElement(driver, "LOBBY", "MAIN")

    except:
        if StaleElementReferenceException:
            print(StaleElementReferenceException)
            elements = findElements(driver, "MULTI", "MULTI TABLE")
            name = elements[i]
            driver.save_screenshot("screenshots/StaleElementReferenceException.png")
        else:
            print(Exception)
            driver.save_screenshot(f"screenshots/{Exception}-{gameTable[selectedGame]}.png")

def multiBetLimit(driver, game, assertBelowLimitStatus, assertOverLimitStatus, tableNum, intoText, betArea):
    print(Fore.CYAN+"\nMinimum Bet Limit"+Fore.RESET)
    print(Fore.RESET+"Table Name: \033[1;30m",intoText.text,"\033[0m")

    try:
        minLocator = "//div[@class='chip-value' and text()='1']"
        driver.find_element(By.XPATH, minLocator).click()
        print("TRY:\033[1;30m FOUND CHIP 1\033[0m")
    except TimeoutException:
        WaitShuffling(driver, "MULTI", "SHUFFLING TEXT", table=tableNum)
        print("Shuffling...")
    except:
        print("CATCH:\033[1;30m EDIT CHIP\033[0m")
        editChips(driver, value=1)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)

    if intoInt < 10:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    print(f"ACTION: \033[1;30mPLACE BET")

    # if not findModElement(driver, "MULTI", "SHUFFLING TEXT", table=tableNum):

    WaitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)
                
    waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)

    # assert validation displayed == 'Below Minimum Limit'
    assertBelowLimit(driver, tableNum, assertBelowLimitStatus)

    # //////////////////////////////////////////////////////////

    print(Fore.CYAN+"\nMaximum Bet Limit"+Fore.RESET)
    try:
        minLocator = "//div[@class='chip-value' and text()='10K']"
        driver.find_element(By.XPATH, minLocator).click()
        print("TRY:\033[1;30m FOUND CHIP 10K\033[0m")
    except TimeoutException:
        WaitShuffling(driver, "MULTI", "SHUFFLING TEXT", table=tableNum)
        print("Shuffling...")
    except:
        print("CATCH:\033[1;30m EDIT CHIP\033[0m")
        editChips(driver, value=10009)

    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)

    if intoInt < 10:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

    print("ACTION: \033[1;30mPLACE BET")
    repeat = True

    print(Fore.RESET+"PLACE BET:\033[1;30m",betArea,"\033[0m")
                
    while repeat:
        try:
            waitModClickable(driver, "MULTI BETTINGAREA", f"{game}", f"{betArea}", table=tableNum)
            assertOverLimit = waitModText(driver, "MULTI", "VALIDATION", table=tableNum, time=1, text="Over Maximum Limit!")

            if assertOverLimit:
                assertAboveLimit(assertOverLimitStatus, assertOverLimit)
                repeat = False
        except: repeat = True

    findModElement(driver, "MULTI BUTTON", "CONFIRM BUTTON", click=True, table=tableNum)


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