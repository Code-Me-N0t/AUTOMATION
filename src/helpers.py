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
    selector = (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, 600).until(EC.presence_of_all_elements_located(selector))
    return element

def findModElements(driver, *keys, table=None):
    selector= table + " " + locator(*keys)
    element = driver.find_elements(By.CSS_SELECTOR, selector)
    return element

def waitElement(driver, *keys, time=600):
    selector = (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, time).until(EC.visibility_of_element_located(selector))
    return element

def navigateMulti(driver):
    waitElement(driver, "PRE LOADING")
    waitElement(driver, "LOBBY", "MAIN")
    waitElement(driver, "LOBBY", "MENU")
    waitClickable(driver, "NAV", "MULTI")
    waitElement(driver, "MULTI", "MAIN")

def waitModElement(driver, *keys, table=None):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    return element

def waitShuffling(driver, *keys, table=None):
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
    selector = table + " " + locator(*keys)
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

def editChips(driver, value):
    findElement(driver, "INGAME", "EDIT_CHIP", click=True)
    findElement(driver, "INGAME", "EDIT_BTN", click=True)
    findElement(driver, "INGAME", "CLEAR_CHIP", click=True)
    inputValue(driver, "INGAME", "ENTER_VALUE", value=value)
    findElement(driver, "INGAME", "SAVE_BTN", click=True)
    findElement(driver, "INGAME", "CLOSE_BTN", click=True)

# SPREADSHEET REPORT STATUSES
def reportSheet(*args):
    assert_statuses = [
        ("Table Switch", args[0]),
        ("Below Limit", args[1]),
        ("Over Limit", args[2]),
        ("Bet Placed", args[3]),
        ("Deducted Balance", args[4]),
        ("Added Balance", args[5]),
        ("Bet Limit", args[6])
    ]
    for (assert_type, assert_list) in assert_statuses:
        if assert_list:
            print(f"{assert_type}: {assert_list}")
    # if report:
    #     status = "PASSED"
    #     cell = locator("CELL", f"{game}")
    #     for index, (assert_type, assert_list) in enumerate(assert_statuses):
    #         if assert_list:
    #             if "FAILED" in assert_list:
    #                 status = "FAILED"
    #             print(f"{assert_type}: ", assert_list)
    #             update_spreadsheet(status, f"D{(cell + index)}")
    #         # if failedTables:
    #         #     update_spreadsheet(failedTables, f"D{(cell + index)}")
    # else: 
    #     print("Report disabled")


# ASSERTIONS
def assertWinAdded(driver, game, testStatus, tableNum, betArea, playerBalance, oldBalance, deductedBalance, failedTables, gameTable, selectedGame, betValue):
    newBalance = round(float(playerBalance.text.replace(',','')), 2)
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
    assertWin = waitElement(driver, "MULTI", "TOAST")
    payout = locator("PAYOUT", f"{game}", f"{betArea}")
    print(assertWin.text)
    printTexts('body', 'Payout: ', f'1:{payout}')

    if "Win" in assertWin.text:
        addedBalance = (betValue * payout) + newBalance
        validateAddedBalance = oldBalance - (betValue-(betValue*payout))
        assertion('Win Assertion', round(addedBalance, 2), round(validateAddedBalance, 2), operator.eq, testStatus, failedTables, gameTable, selectedGame)
    else: assertion('Lose Assertion', round(newBalance, 2), round(deductedBalance, 2), operator.eq, testStatus, failedTables, gameTable, selectedGame)

def assertion(assertionTitle, actual, expected, operator, testStatus, failedTables, gameTable, selectedGame):
    try:
        assert operator(actual, expected)
        printTexts('body', assertionTitle, ': PASSED')
        testStatus.append("PASSED")
    except AssertionError:
        testStatus.append("FAILED")
        failedTables.append(gameTable[selectedGame])
        printTexts('body', assertionTitle, ': FAILED')

def sampleReport(*args):
    samples = [
        ("sample 1", args[0]),
        ("sample 2", args[1]),
        ("sample 3", args[2]),
        ("sample 4", args[3]),
        ("sample 5", args[4]),
        ("sample 6", args[5]),
        ("sample 7", args[6]),
    ]
    for (sample_list, sample_value) in samples:
        if sample_value:
            print(f"{sample_list}: {sample_value}")