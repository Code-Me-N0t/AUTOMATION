from src.modules import *

def findElement(driver, *keys, click=False):
    selector=locator(*keys)
    element = driver.find_element(By.CSS_SELECTOR, selector)
    if click: element.click()
    else: return element

def findModElement(driver, *keys, click=False, table=None):
    selector = table+" "+locator(*keys)
    element = driver.find_element(By.CSS_SELECTOR, selector)
    if click: element.click()
    else: return element

def findElements(driver, *keys):
    selector=locator(*keys)
    element = driver.find_elements(By.CSS_SELECTOR, selector)
    return element

def findModElements(driver, *keys, table=None):
    selector= table + " " + locator(*keys)
    element = driver.find_elements(By.CSS_SELECTOR, selector)
    return element

def waitElement(driver, *keys, time=60):
    selector = (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, time).until(EC.visibility_of_element_located(selector))
    return element

def waitModElement(driver, *keys, table=None):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    return element

def WaitShuffling(driver, *keys, table=None):
    selector = table + " " + locator(*keys)
    try:
        element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        print("Shuffling...")
        WebDriverWait(driver, 600).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
        return element
    except: 
        return False

def presenceElement(driver, *keys):
    selector = (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, 600)
    element.until(EC.presence_of_element_located(selector))
    return element

def waitElementInvis(driver, *keys):
    selector= (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, 600)
    element.until(EC.invisibility_of_element_located(selector))
    return element

def waitModElementInvis(driver, *keys, table=None):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
    return element

def waitClickable(driver, *keys):
    selector= (By.CSS_SELECTOR, locator(*keys))
    wait = WebDriverWait(driver, 100)
    element = wait.until(EC.element_to_be_clickable(selector))
    element.click()

def waitModClickable(driver, *keys, table=None):
    selector= table + " " + locator(*keys)
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    element.click()

def waitText(driver, *keys, text, game=None, number=None):
    selector= (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, 600)
    element.until(EC.text_to_be_present_in_element(selector, text_=text))
    driver.save_screenshot(f"screenshots/{game}-{text}-{number}.png")
    printTexts('body', 'MESSAGE DISPLAYED: ', text)
    return element

def waitModText(driver, *keys, text, game=None, number=None, table=None, time=600):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, time).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text_ = text))
    driver.save_screenshot(f"screenshots/{game}-{text}-{number}.png")
    printTexts('body', 'MESSAGE DISPLAYED: ', text)
    return element

def inputValue(driver, *keys, value):
    selector = (By.CSS_SELECTOR, locator(*keys))
    input_element = driver.find_element(*selector)
    if value:input_element.send_keys(value)
    else:return value

def printText(value, text):
    color_map = {
        'title': f'\n{Fore.CYAN}',
        'body': Fore.LIGHTBLACK_EX,
        'failed': Fore.RED,
        'passed': Fore.GREEN
    }
    color = color_map.get(value)
    print(f"{color}{text}")

def printTexts(value, caption, text):
    color_map = {
        'title': f'\n{Fore.CYAN}',
        'body': Fore.LIGHTBLACK_EX,
        'failed': Fore.RED,
        'passed': Fore.GREEN
    }
    color = color_map.get(value)
    print(f"{caption}{color}{text}")

def editChips(driver,value):
    findElement(driver, "INGAME", "EDIT_CHIP", click=True)
    findElement(driver, "INGAME", "EDIT_BTN", click=True)
    findElement(driver, "INGAME", "CLEAR_CHIP", click=True)
    inputValue(driver, "INGAME", "ENTER_VALUE", value=value)
    findElement(driver, "INGAME", "SAVE_BTN", click=True)
    findElement(driver, "INGAME", "CLOSE_BTN", click=True)

# SPREADSHEET REPORT STATUSES
def reportSheet(game, report, gameTable, assertTableSwitchStatus, assertBelowLimitStatus, assertOverLimitStatus, assertBetPlacedStatus, assertDeductedBalanceStatus, assertAddedBalanceStatus, selectedGame):
    assert_statuses = [
            ("Table Switch", assertTableSwitchStatus),
            ("Below Limit", assertBelowLimitStatus),
            ("Over Limit", assertOverLimitStatus),
            ("Bet Placed", assertBetPlacedStatus),
            ("Deducted Balance", assertDeductedBalanceStatus),
            ("Added Balance", assertAddedBalanceStatus)
        ]
    if report:
        status = "PASSED"
        cell = locator("CELL", f"{game}")
        for index, (assert_type, assert_list) in enumerate(assert_statuses):
            if assert_list:
                if "FAILED" in assert_list:
                    status = "FAILED"
                    # add table to remarks cell
                    update_spreadsheet(gameTable[selectedGame], f"E{(cell + index)}")
                else: update_spreadsheet("", f"E{(cell + index)}")
                print(f"{assert_type}: ", assert_list)
                update_spreadsheet(status, f"D{(cell + index)}")
    else:
        print("Report disabled")


# ASSERTIONS
def assertBelowLimit(driver, tableNum, assertBelowLimitStatus):
    validate = waitModElement(driver, "MULTI", "VALIDATION", table=tableNum)
    try:
        assert 'Below Minimum Limit' == validate.text
        printTexts('body', 'Below Minimum Assertion: ', 'PASSED')
        assertBelowLimitStatus.append("PASSED")
    except AssertionError:
        printTexts('body', 'Below Minimum Assertion: ', f" FAILED\nMessage: {validate.text}")
        assertBelowLimitStatus.append("FAILED")

def assertTableSwitch(gameTable, assertTableSwitchStatus, selectedGame, intoText):
    try:
        assert gameTable[selectedGame] == intoText.text
        printTexts('body', 'Table Switch Assertion: ', 'PASSED')
        assertTableSwitchStatus.append("PASSED")
    except AssertionError:
        printTexts('body', 'Table Switch Assertion: ', f"FAILED\nTable Switched: {intoText.text}")
        print("Table Switch Assertion: "+Fore.LIGHTBLACK_EX+f"FAILED\nTable Switched: {intoText.text}")
        assertTableSwitchStatus.append("FAILED")

def assertAboveLimit(assertOverLimitStatus, assertOverLimit):
    try: 
        assert assertOverLimit
        printTexts('body', 'Over Limit Assertion: ', 'PASSED')
        assertOverLimitStatus.append("PASSED")
    except AssertionError:
        printTexts('body', 'Over Limit Assertion: ', 'FAILED')
        assertOverLimitStatus.append("FAILED")

def assertWinAdded(driver, game, assertAddedBalanceStatus, tableNum, betArea, playerBalance, oldBalance, deductedBalance):
    newBalance = round(float(playerBalance.text.replace(',','')), 2)

    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    assertWin = waitElement(driver, "MULTI", "TOAST")
    payout = locator("PAYOUT", f"{game}", f"{betArea}")
    print(assertWin.text)
    printTexts('body', 'Payout: ', f'1:{payout}')

    if "Win" in assertWin.text:
        addedBalance = (201 * payout) + newBalance
        validateAddedBalance = oldBalance - (201-(201*payout))
                                        # print("Added Balance: ", addedBalance)
        try:
            assert round(addedBalance, 2) == round(validateAddedBalance, 2)
            printTexts('body', 'Won Assertion: ', 'PASSED')
            assertAddedBalanceStatus.append("PASSED")
        except AssertionError:
            printTexts('body', 'Won Assertion: ', f'FAILED\n{round(addedBalance, 2)} != {round(validateAddedBalance, 2)}')
            assertAddedBalanceStatus.append("FAILED")
    else:
        try:
            assert round(deductedBalance, 2) == round(newBalance, 2)
            printTexts('body', 'Lose Assertion: ', 'PASSED')
            assertAddedBalanceStatus.append("PASSED")
        except AssertionError:
            printTexts('body', 'Lose Assertion: ', f'FAILED\n{round(deductedBalance, 2)} != {round(newBalance, 2)}')
            assertAddedBalanceStatus.append("FAILED")

def assertDeductedBalance(assertDeductedBalanceStatus, playerBalance, oldBalance):
    deductedBalance = oldBalance - 201
    try:
        assert round(deductedBalance, 2) == round(float(playerBalance.text.replace(',', '')), 2)
        printTexts('body', 'Balance Deducted Assertion: ', 'PASSED')
        assertDeductedBalanceStatus.append("PASSED")
    except AssertionError:
        print(f"Balance Deducted Assertion: {Fore.RED}FAILED{Fore.LIGHTBLACK_EX}\n{round(deductedBalance,2):.2f} != {playerBalance.text.replace(',','')}")
        printTexts('body', 'Balance Deducted Assertion: ', f'FAILED\n{round(deductedBalance,2):.2f} != {playerBalance.text.replace(',','')}')
        assertDeductedBalanceStatus.append("FAILED")
    return deductedBalance

def assertBetPlaced(driver, assertBetPlacedStatus, tableNum):
    assertBetPlaced = waitModText(driver, "MULTI", "VALIDATION", text='Bet Successful!', table=tableNum, time=10)
    try: 
        assert assertBetPlaced
        assertBetPlacedStatus.append("PASSED")
        printTexts('body', 'Bet Placed Assertion: ', 'PASSED')
    except AssertionError:
        printTexts('body', 'Bet Placed Assertion: ', 'FAILED')
        assertBetPlacedStatus.append("FAILED")