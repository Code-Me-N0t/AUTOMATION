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

def findChildElement(driver, *keys, click=False, mod=None):
    selector = locator(*keys)+f':nth-child({mod})'
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
    waitElement(driver, "MULTI", "MAIN", time=10)

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
    except: return False

def waitBetMask(driver, *keys, table=None):
    selector = table + " " + locator(*keys)
    try:
        element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        
        WebDriverWait(driver, 600).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
        return element
    except: return False

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

def waitText(driver, *keys, text):
    selector= (By.CSS_SELECTOR, locator(*keys))
    element = WebDriverWait(driver, 600)
    element.until(EC.text_to_be_present_in_element(selector, text_=text))
    return element

def waitModText(driver, *keys, text, table=None, time=600):
    selector = table + " " + locator(*keys)
    element = WebDriverWait(driver, time).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text_ = text))
    return element

def inputValue(driver, *keys, value):
    selector = (By.CSS_SELECTOR, locator(*keys))
    input_element = driver.find_element(*selector)
    if value:input_element.send_keys(value)
    else:return value

def printText(value, text):
    color_map = {
        'title': f'{Fore.CYAN}',
        'body': Fore.LIGHTBLACK_EX,
        'failed': Fore.RED,
        'passed': Fore.GREEN
    }
    color = color_map.get(value)
    print(f"{color}{text}")

def printTexts(value, caption, text):
    color_map = {
        'title': f'{Fore.CYAN}',
        'body': Fore.LIGHTBLACK_EX,
        'failed': Fore.RED,
        'passed': Fore.GREEN
    }
    color = color_map.get(value)
    str_space = len(caption)
    space = "." * (40-str_space)
    print(f"{caption}{color}{space} {text}")

def BettingTimer(driver, tableNum, timer=5):
    waitShuffling(driver, "MULTI", "SHUFFLING_TEXT", table=tableNum)
    time = findModElement(driver, "MULTI TABLE", "TABLE TIME", table=tableNum)
    intoInt = int(time.text)
    if intoInt < timer:
        waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)
        waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tableNum)

def EditChips(driver, chipValue):
    formatted_num = FormatNumber(chipValue)

    actions = ActionChains(driver)
    # print(f'formatted num: {formatted_num}')
    repeat = True
    while repeat:
        chips = findElements(driver, "MULTI", "CHIP VALUE")
        for chip in chips:
            actions.move_to_element(chip).perform()         
            if chip.text == formatted_num:
                chip.click()
                repeat = False
                return
            
        findElement(driver, "INGAME", "EDIT_CHIP", click=True)
        chip_select = findElements(driver, 'INGAME', 'CHIP SELECTION')

        for index in range(len(chip_select)):
            inner_chip = chip_select[index]

            selected_chips = findElements(driver, 'INGAME', 'SELECT CHIP')
            
            if formatted_num == inner_chip.text:
                if len(selected_chips) >= 10:
                    chip_wrap = findElements(driver, 'INGAME', 'CHIP WRAP')
                    for unselect_chip in chip_wrap:
                        if 'chip-selection' in unselect_chip.get_attribute('class'):
                            unselect_chip.click()
                            break
                inner_chip.click()
                break
            elif index == len(chip_select) -1 and formatted_num != inner_chip.text:
                edit_chip(driver, chipValue)

        findElement(driver, "INGAME", "CLOSE_BTN", click=True)
        
def edit_chip(driver, num):
    findElement(driver, "INGAME", "EDIT_BTN", click=True)
    findElement(driver, "INGAME", "CLEAR_CHIP", click=True)
    inputValue(driver, "INGAME", "ENTER_VALUE", value=num)
    findElement(driver, "INGAME", "SAVE_BTN", click=True)
    sleep(2)
    validate = findElement(driver, 'INGAME', 'CHIP VALIDATION')
    assert validate.text == 'Successfully change the chip amount', f'FAILED: {validate.text}'

def FormatNumber(num):
    if num >= 10000000: 
        truncated_num = int(num / 10000)
        formatted_num = '{:.1f}M'.format(truncated_num / 10)
    elif num >= 1000000: 
        truncated_num = int(num / 100000)
        formatted_num = '{:.1f}M'.format(truncated_num / 10)
    elif num >= 1000: 
        truncated_num = int(num / 100)
        formatted_num = '{:.1f}K'.format(truncated_num / 10)
    else: formatted_num = str(num)
    formatted_num = formatted_num.replace('.0','')
    return formatted_num

def textDecoder(index, gametable, base64_string, directory, game):
    dir = f'decoded_images/{game}/{directory}/{gametable}/'
    card = f'card{index}.png'
    create_files(dir)
    if 'card-hidden' in base64_string: card_value = 'e'
    else:
        image_data = base64.b64decode(base64_string)
        image_data = BytesIO(image_data)
        Image.open(image_data).save(f'{dir}{card}')

        img = Image.open(f'{dir}{card}')
        width, height = img.size
        top_y = int(height * 0.08)
        bottom_y = int(height * 0.45)
        crop_img = img.crop((0, top_y, width, bottom_y))
        crop_img.save(f'{dir}{card}')

        value = pytesseract.image_to_string(crop_img, config='--psm 10')

        card_value = str(value[0])
    return card_value

def getShoe(driver, tablenum):
    shoe = findModElement(driver, 'MULTI TABLE', 'SHOE ROUND', table=tablenum)
    shoe_text = shoe.text.split(' ')[-1].strip()
    return shoe_text

def randomizeBetarea(game):
    randomize = locator("MULTI BETTINGAREA",f"{game}")
    betAreas = list(randomize.keys())
    betArea = random.choice(betAreas)
    return betArea

def navigateSettings(driver, where):
    waitClickable(driver, 'MULTI', 'SETTING')
    waitElement(driver, 'MULTI SETTINGS', 'MAIN')
    waitClickable(driver, 'MULTI SETTINGS', where)
    waitElement(driver, 'MULTI HISTORY', 'MAIN')

# SPREADSHEET REPORT STATUSES
def multiReportSheet(report, game, test_status):
    if report:
        cell = locator("CELL", f"{game}")
        for index, (names, values) in enumerate(test_status.items()):
            if values and names:
                space = "." * (39-len(names))
                status = "PASSED"
                if 'FAILED' in values: status = "FAILED"                
                if game != 'BACCARAT' and game != 'DT': 
                    if names == 'Card Result' or names == 'Flipped Cards' or names == 'Bet Within Bet Pool': continue
                if names == 'Bet On Super Six' and game != 'BACCARAT': continue
                update_spreadsheet(status, f"D{(cell + index)}")
                printText('body',f'{names}:{space} {status}')
    else: print("Report disabled")

# ASSERTION
def assertion(driver, assertionTitle, actual, expected, op, testStatus, failedTables, gameTable, scenario):
    space = " " * 5
    space2 = " " * (80 - (10 + len(str(scenario))))
    space3 = " " * (30 - (10+len(str(actual))))
    if op is not None:
        condition = ''
        if op is operator.eq: condition = 'EQUAL'
        if op is operator.ne: condition = 'NOT EQUAL'
    try:
        assert op(actual, expected)
        printTexts('body', f'{assertionTitle}:', f'PASSED {space}{scenario}')
        testStatus.append("PASSED")
    except AssertionError:
        testStatus.append("FAILED")
        if failedTables is not None: failedTables.append(gameTable)
        printTexts('failed', f'{assertionTitle}:', f'FAILED {space}{scenario}{space2}Actual: {actual}{space3}Expected: {expected}')
    
    create_files(f'screenshots/assertion')
    driver.save_screenshot(f'screenshots/assertion/[{gameTable}][{assertionTitle}].png')