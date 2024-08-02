from src.modules import *
from src.element_handler import Handler

'''
    This class, `Tasks`, is designed to handle a variety of tasks related to navigating and interacting with the user interface
    of a web application using the `Handler` class for element interactions. 

    Methods:
    - __init__: Initializes the Tasks instance with a Handler instance.
    - navigateLobby: Navigates to a specified section within the lobby.
    - navigateSettings: Navigates to a specified section within the settings.
    - printText: Prints colored text to the console.
    - printTexts: Prints colored captioned text with a dynamic spacer to the console.
    - waitBetMask: Waits for a betting mask element to become visible and then invisible.
    - bettingTimer: Waits for the betting timer to finish and handles subsequent actions.
    - formatNumber: Formats a number into a more readable string representation.
    - editChips: Edits the chip value in the game interface.
    - decodeText: Decodes base64 encoded text from a game element and saves it as an image.
    - randomBet: Randomly selects a betting area for the game.
    - spacer: Generates a spacer string of a specified length.
    - generateReport: Generates a report based on the test status and updates a spreadsheet accordingly.
'''

class Tasks:
    def __init__(self, handler):
        self.handler = handler
        self.modules = Modules(handler)
        self.time = 60

    @handle_exceptions
    def navigateLobby(self, where):
        self.handler.waitElement('PRE LOADING')
        self.handler.waitElement('LOBBY', 'MAIN')
        self.handler.waitElement('LOBBY', 'MENU')
        self.handler.waitClickable('NAV', where, time=10)
        if where == 'MULTI':
            self.handler.waitElement('MULTI', 'MAIN')
        else: pass
    
    @handle_exceptions
    def navigateSidebet(self, where):
        self.handler.clickElement('INGAME', 'SIDEBET')
        self.handler.waitElement('SIDEBET', 'MAIN')
        self.handler.clickElement('SIDEBET', where)
        self.handler.waitElement('SIDEBET', 'MAIN')

    @handle_exceptions
    def betIngame(self):
        print('inner line 1')
        self.handler.waitElement('INGAME', 'MAIN')
        
        print('inner line 2')
        self.handler.waitElement('INGAME', 'RESULT')
        self.handler.waitElementInvis('INGAME', 'RESULT')
        
        print('inner line 3')
        self.handler.waitClickable('INGAME', 'BET')
        self.handler.clickElement('INGAME BUTTON', 'CONFIRM')

        print('inner line 4')
        self.handler.waitElement('INGAME', 'RESULT')
        print('inner line 4.5')
        self.handler.waitElementInvis('INGAME', 'RESULT')
        print('inner line 5')

    @handle_exceptions
    def sideBettingTimer(self, index):
        while True:
            start_time = time.time()
            timer = self.handler.getText('SIDE TABLES', 'TIMER', index=index)
            
            if int(timer) >= 10: break

            end_time = time.time() - start_time

            if end_time >= 60:
                table_num = self.handler.getText('SIDE TABLES', 'TABLE NUMBER', index=index)
                raise TimeoutException(f'{Fore.RED}{table_num} stays zero for {end_time} seconds')

    @handle_exceptions
    def navigateSettings(self, where):
        self.handler.waitElement('MULTI', 'SETTING')
        self.handler.waitElement('MULTI SETTINGS', 'MAIN')
        self.handler.waitElement('MULTI SETTINGS', where)
        self.handler.waitElement('MULTI HISTORY', 'MAIN')

    @handle_exceptions
    def nextRound(self, index):
        self.handler.waitElement('MULTI TABLE', 'TABLE RESULT', index=index)
        self.handler.waitElementInvis('MULTI TABLE', 'TABLE RESULT', index=index)
    
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
        space = '.' * (40-len(caption))
        color = color_map.get(value)
        print(f'{caption}{color}{space} {text}')

    # @handle_exceptions
    def waitTask(self, where, time, index=None):
        try:
            element = self.handler.getElement('MULTI TABLE', where, index=index)
            if element:
                self.handler.waitElementInvis('MULTI TABLE', where, time=(time*10) or self.time, index=index)
            else: return False
        except NoSuchElementException:
            return False
    
    def splitUpperCase(self, text):
       return re.sub(r'([a-z])([A-Z])', r'\1 \2', text) 
            
    @handle_exceptions
    def waitNextRound(self, index):
        is_true = False
        while True:
            timer = self.handler.getText('SIDE TABLES', 'TIMER', index=index)
            if int(timer) == 0: 
                while True:
                    timer = self.handler.getText('SIDE TABLES', 'TIMER', index=index)
                    if  int(timer) > 0:
                        is_true = True
                        break
            if is_true:
                break

    # @handle_exceptions
    def bettingTimer(self, time, index=None):
        timer = self.handler.getText('MULTI TABLE', 'TABLE TIME', index=index)
        
        if int(timer) < time:
            self.handler.waitElement('MULTI TABLE', 'TABLE RESULT', time=time or self.time, index=index)
            self.handler.waitElementInvis('MULTI TABLE', 'TABLE RESULT', time=time or self.time, index=index)

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
            # check chip selection if desired chip amount is displayed
            chips = self.handler.getElements('MULTI', 'CHIP VALUE')
            for chip in chips:
                actions.move_to_element(chip).perform()
                if chip.text == formatted_num:
                    self.modules.click(chip)
                    repeat = False
                    break

            # check if inner chips if desired chip amount displayed
            if repeat:
                self.handler.clickElement('INGAME', 'EDIT_CHIP')
                chip_select = self.handler.getElements('INGAME', 'CHIP SELECTION')

                for index, inner_chip in enumerate(chip_select):
                    selected_chips = self.handler.getElements('INGAME', 'SELECT CHIP')

                    if formatted_num == inner_chip.text:
                        if len(selected_chips) >= 10:
                            chip_wrap = self.handler.getElements('INGAME', 'CHIP WRAP')
                            for unselect_chip in chip_wrap:
                                if 'chip-selection' in unselect_chip.get_attribute('class'):
                                    self.handler.modules.click(unselect_chip)
                                    break
                        self.handler.modules.click(inner_chip)
                        break
                    elif index == len(chip_select) - 1 and formatted_num != inner_chip.text:
                        self.handler.clickElement('INGAME', 'EDIT_BTN')
                        self.handler.clickElement('INGAME', 'CLEAR_CHIP')
                        self.handler.inputValue('INGAME', 'ENTER_VALUE', value=chip_value)
                        self.handler.waitClickable('INGAME', 'SAVE_BTN')
                        sleep(2)
                        validate = self.handler.findElement('INGAME', 'CHIP VALIDATION')
                        assert validate.text == 'Successfully change the chip amount', f'FAILED: {validate.text}'
                self.handler.clickElement('INGAME', 'CLOSE_BTN')
            else: break

    @handle_exceptions
    def decodeText(self, card_index, base64_string, directory, game, index):
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
    def randomBet(self, game, betarea):
        randomize = locator(f'{betarea}',f'{game}')
        betareas = list(randomize.keys())
        betarea = random.choice(betareas)
        return betarea
    
    @handle_exceptions
    def spacer(self, length=5, element=None):
        space = '.' * (length - len(element)) if element else length
        return Fore.LIGHTBLACK_EX + space
    
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

    @handle_exceptions
    def assertion(self, expected, actual, operator):
        try:
            assert operator(expected, actual)
            result = 'PASSED'
        except AssertionError:
            result = 'FAILED'
            # print(f'Expected Result: {expected}')
            # print(f'Actual Result: {actual}')
        return result