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

def navigateTab(driver, tab):
    waitElement(driver, "PRE LOADING")
    waitElement(driver, "LOBBY", "MAIN")
    waitElement(driver, "LOBBY", "MENU")
    waitClickable(driver, "NAV", tab)
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

def waitClickable(driver, *keys, timer=100):
    selector= (By.CSS_SELECTOR, locator(*keys))
    wait = WebDriverWait(driver, timer)
    element = wait.until(EC.element_to_be_clickable(selector))
    element.click()

def waitModClickable(driver, *keys, table=None, timer=100):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, timer).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    element.click()

def waitText(driver, *keys, text, game=None, number=None):
    selector= (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, 600)
    element.until(EC.text_to_be_present_in_element(selector, text_=text))
    # driver.save_screenshot(f"screenshots/{game}-{text}-{number}.png")
    # printTexts('body', 'MESSAGE DISPLAYED: ', text)
    return element

def waitModText(driver, *keys, text, game=None, number=None, table=None, time=600):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, time).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text_ = text))
    # driver.save_screenshot(f"screenshots/{game}-{text}-{number}.png")
    # printTexts('body', 'MESSAGE DISPLAYED: ', text)
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
    str_space = len(caption)
    space = "." * (40-str_space)
    print(f"{caption}{color}{space} {text}")

def editChips(driver, value):
    findElement(driver, "INGAME", "EDIT_CHIP", click=True)
    findElement(driver, "INGAME", "EDIT_BTN", click=True)
    findElement(driver, "INGAME", "CLEAR_CHIP", click=True)
    inputValue(driver, "INGAME", "ENTER_VALUE", value=value)
    findElement(driver, "INGAME", "SAVE_BTN", click=True)
    findElement(driver, "INGAME", "CLOSE_BTN", click=True)

def BettingTimer(driver, tableNum):
    waitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)
    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)
    if intoInt < 5:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

def EditChips(driver, actions, chipValue):
    repeat = True
    while repeat:
        chips = findElements(driver, "MULTI", "CHIP VALUE")
        for chip in range(len(chips)):
            selectedChip = chips[chip]
            actions.move_to_element(selectedChip).perform()
                                        
            if chips[chip].text == str(chipValue):
                selectedChip.click()
                break
            if chip >= 9: editChips(driver, value=chipValue)
        break

def decodeBase64(index, card, gametable):
    image_string = card.value_of_css_property('background-image')
    base64_string = re.search(r'url\("?(.*?)"?\)', image_string).group(1)
    base64_string = base64_string.replace('data:image/png;base64,','')

    return textDecoder(index, gametable, base64_string, 'gametable')

def textDecoder(index, gametable, base64_string, directory):
    image_data = base64.b64decode(base64_string)
    image_data = BytesIO(image_data)
    Image.open(image_data).save(f'decoded_images/{directory}/{gametable}_card{index}.png')

    img = Image.open(f'decoded_images/{directory}/{gametable}_card{index}.png')
    width, height = img.size
    top_y = int(height * 0.08)
    bottom_y = int(height * 0.45)
    crop_img = img.crop((0, top_y, width, bottom_y))
    crop_img.save(f'decoded_images/{directory}/{gametable}_card{index}.png')

    value = pytesseract.image_to_string(crop_img, config='--psm 10')

    card_value = str(value[0].replace('\n' or ' ', ''))
    return card_value

def navigateSettings(driver, where):
    waitClickable(driver, 'MULTI', 'SETTING')
    waitElement(driver, 'MULTI SETTINGS', 'MAIN')
    waitClickable(driver, 'MULTI SETTINGS', where)
    waitElement(driver, 'MULTI HISTORY', 'MAIN')

# SPREADSHEET REPORT STATUSES
def multiReportSheet(report, game, tables, *args):
    assert_statuses = [
        ("Table Switch", args[0]),
        ("Cancel Bet", args[1]),
        ("Balance Deduction", args[2]),
        ("Single Bet", args[3]),
        ("Multiple Bet", args[4]),
        ("All Bet", args[5]),
        ("Bet Successful", args[6]),
        ("No More Bets", args[7]),
        ("Closed Betting Timer", args[8]),
        ("Bet Payout", args[9]),
        ("Empty Betarea", args[10]),
        ("Super Six", args[11]),
        ("Bet Record", args[12]),
        ("Below Bet Limit", args[13]),
        ("Ask B/P", args[14]),
        ("Card Result", args[15]),
        ("Flipped Cards", args[16]),
        ("All In Bet", args[17]),
    ]
    if report:
        cell = locator("CELL", f"{game}")
        num = 0
        for index, (assert_type, assert_list) in enumerate(assert_statuses):
            status = "PASSED"
            space = "." * (30-len(assert_type))
            if assert_list:
                if "FAILED" in assert_list:
                    status = "FAILED"
                    update_spreadsheet(tables[index], f"E{(cell + index)}")
                printTexts('body', f'{assert_type}:', assert_list)
                update_spreadsheet(status, f"D{(cell + index)}")
                assert_list.clear()
                num = index
        tables[num].clear()
    else: print("Report disabled")

def sideReportSheet(report, game, failedTables, *args):
    assert_statuses = [
        ("Bet Placed", args[0]),
        ("Payout Assertion", args[1]),
        ("Empty Betting Area Assertion", args[2])
    ]
    if report:
        cell = locator("CELL", f"{game}")
        for index, (assert_type, assert_list) in enumerate(assert_statuses):
            status = "PASSED"
            if assert_list:
                if "FAILED" in assert_list:
                    status = "FAILED"
                    # update_spreadsheet(failedTables[index], f"J{(cell + index)}")
                print(f"{assert_type}: ", assert_list)
                update_spreadsheet(status, f"I{(cell + index)}")
    else: print("Report disabled")

# ASSERTION
def assertion(driver,assertionTitle, actual, expected, operator, testStatus, failedTables, gameTable):
    space = " " * 5
    space2 = " " * (20 - (7+len(str(actual))))
    space3 = " " * (23 - (10+len(str(expected))))
    try:
        assert operator(actual, expected)
        printTexts('body', f'{assertionTitle}:', f'PASSED {space}Actual: {actual}{space2}Expected: {expected}{space3}Condition: {operator.__name__}')
        testStatus.append("PASSED")
    except AssertionError:
        testStatus.append("FAILED")
        if failedTables is not None: failedTables.append(gameTable)
        printTexts('failed', f'{assertionTitle}:', f'FAILED {space}Actual: {actual}{space2}Expected: {expected}{space3}Condition: {operator.__name__}')
    screenshot(driver, gameTable, assertionTitle)