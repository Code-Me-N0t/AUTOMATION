from src.modules import *
from src.element_handler import Handler
from src.element_handler import click_highlighter as clicker

class Tasks:
    def __init__(self, handler):
        self.handler = handler
        self.time = 600
        self.index = None

    @handle_exceptions
    def navigateLobby(self, where):
        self.handler.waitElement('PRE LOADING')
        self.handler.waitElement('LOBBY', 'MAIN')
        self.handler.waitElement('LOBBY', 'MENU')
        self.handler.waitClickable('NAV', where)
        self.handler.waitElement('MULTI', 'MAIN')

    @handle_exceptions
    def navigateSettings(self, where):
        self.handler.waitElement('MULTI', 'SETTING')
        self.handler.waitElement('MULTI SETTINGS', 'MAIN')
        self.handler.waitElement('MULTI SETTINGS', where)
        self.handler.waitElement('MULTI HISTORY', 'MAIN')
    
    @handle_exceptions
    def printText(self, value, text):
        color_map = {
            'cyan': Fore.CYAN,
            'gray': Fore.LIGHTBLACK_EX,
            'red': Fore.RED,
            'green': Fore.GREEN,
        }
        color = color_map.get(value)
        print(f'{color}{text}')

    @handle_exceptions
    def printTexts(self, value, caption, text):
        color_map = {
            'cyan': Fore.CYAN,
            'gray': Fore.LIGHTBLACK_EX,
            'red': Fore.RED,
            'green': Fore.GREEN,
        }
        color = color_map.get(value)
        space = "." * (40-len(caption))
        color = color_map.get(value)
        print(f'{caption}{color}{space} {text}')

    @handle_exceptions
    def waitBetMask(self, time=10, index=None):
        try: 
            self.handler.waitElement('MULTI TABLE', 'BET MASK', time=time, index=index)
            self.handler.waitElementInvis('MULTI TABLE', 'BET MASK', time=time, index=index)
        except NoSuchElementException: return False

    @handle_exceptions
    def bettingTimer(self, time=10, index=None):
        self.waitBetMask()
        time = self.handler.getText('MULTI TABLE', 'TABLE TIME', index=self.index)
        while time == '': continue
        if int(time) < self.time:
            self.handler.waitElement('MULTI TABLE', 'TABLE RESULT', time=time, index=index)
            self.handler.waitElementInvis('MULTI TABLE', 'TABLE RESULT', time=time, index=index)

    @handle_exceptions
    def formatNumber(self, num):
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
    
    @handle_exceptions
    def editChips(self, chip_value):
        formatted_num = self.formatNumber(chip_value)
        actions = ActionChains(self.handler.driver)
        repeat = True

        while repeat:
            chips = self.handler.getElements("MULTI", "CHIP VALUE")
            for chip in chips:
                actions.move_to_element(chip).perform()
                if chip.text == formatted_num:
                    self.handler.clicker(chip)
                    repeat = False
                    return

            self.handler.clickElement("INGAME", "EDIT_CHIP")
            chip_select = self.handler.getElements("INGAME", "CHIP SELECTION")

            for index, inner_chip in enumerate(chip_select):
                selected_chips = self.handler.getElements("INGAME", "SELECT CHIP")

                if formatted_num == inner_chip.text:
                    if len(selected_chips) >= 10:
                        chip_wrap = self.handler.getElements("INGAME", "CHIP WRAP")
                        for unselect_chip in chip_wrap:
                            if 'chip-selection' in unselect_chip.get_attribute('class'):
                                self.handler.clicker(unselect_chip)
                                break
                    self.handler.clicker(inner_chip)
                    break
                elif index == len(chip_select) - 1 and formatted_num != inner_chip.text:
                    self.handler.clicker("INGAME", "EDIT_BTN")
                    self.handler.clicker("INGAME", "CLEAR_CHIP")
                    self.handler.inputValue("INGAME", "ENTER_VALUE", value=chip_value)
                    self.handler.clicker("INGAME", "SAVE_BTN")
                    sleep(2)
                    validate = self.handler.findElement("INGAME", "CHIP VALIDATION")
                    assert validate.text == 'Successfully change the chip amount', f'FAILED: {validate.text}'

            self.handler.clicker("INGAME", "CLOSE_BTN")

    @handle_exceptions
    def decodeText(self, card_index, base64_string, directory, game, index=None):
        dir = f'decoded_images/{game}/{directory}/{index}/'
        card = f'card{card_index}.png'
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

            # print(f'Card {card_index}: {card_value}')
        return card_value
    
    @handle_exceptions
    def randomBet(self, game):
        randomize = locator("MULTI BETTINGAREA",f"{game}")
        betareas = list(randomize.keys())
        betarea = random.choice(betareas)
        return betarea
    
    @handle_exceptions
    def spacer(self, length=5, element=None):
        space = "." * (length - len(element)) if element else "." * length
        return space
    
    @handle_exceptions
    def generateReport(self, report, game, test_status):
        if report:
            cell = locator('CELL', game)
            spacer = self.spacer(39, name)
            exempt = ['Card Result', 'Flippped Cards', 'Bet Within Bet Pool']
            for index, (name, values) in enumerate(test_status.items()):
                if values and name:
                    status = 'FAILED' if 'FAILED' in values else 'PASSED'
                    if game != 'BACCARAT' and game != 'DT':
                        if name in exempt: continue
                    if 'Super Six' in name and game != 'BACCARAT': continue

                    update_spreadsheet(status, f'D{(cell + index)}')
                    self.printText('red', f'{name}:{spacer} {status}')
        else: self.printText('gray', 'Report disabled')