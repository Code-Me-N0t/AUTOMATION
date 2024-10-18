from src.modules import *
from src.handlers.task_handler import Tasks
from src.handlers.element_handler import Handler
from src.handlers.api_handler import GameAPI

class Sidebet:
    def __init__(self, driver):
        self.driver = driver
        self.handler = Handler(driver)
        self.task = Tasks(self.handler)
        self.actions = ActionChains(driver)
        self.api = GameAPI()
        self.chip = 202
        self.betcode = None
        self.betlimit = []
        self.balance = 1000000
        self.index = None
        self.game_found = None
        self.game_number = None
        self.game = None
        self.table = None
        self.results = []
        self.testcases = [
            self.TestEmptyBetarea,
            self.TestConfirmButton,
            self.TestPayout,
            # self.TestAllInBet,
            # self.TestBetLimit,
        ]

    @handle_exceptions
    def main(self, game_type, betcode):
        self.handler.modules.execJS(f'noFullScreen();')
        self.task.navigateLobby(game_type)
        gamelist = locator(game_type)
        self.game = game_type

        self.betcode = betcode
        self.betlimit = list(self.task.getPlayerBalance())
        
        print(f'\n{Fore.LIGHTBLACK_EX}Betlimit: [{betcode}: {self.betlimit[0]} - {self.betlimit[-1]}]')
        
        current_balance = self.api.get_current_balance()
        self.task.printText('gray', f'Balance: {current_balance}')

        self.handler.clickElement('LOBBY', 'ENTER TABLE')

        for game in gamelist:
            print(Fore.LIGHTBLACK_EX + f'\nTable {game}: ', end='')
            for x, test in enumerate(self.testcases):
                testname = self.task.splitUpperCase(test.__name__)
                if 'All In' in testname:
                    balance = 701.57
                else: 
                    balance = self.balance
                
                _ = self.api.update_balance(balance)
                
                self.task.betIngame(self.chip)
                self.task.navigateSidebet('LOBBY')

                game_elements = self.handler.getElements('SIDEBET', 'TABLES')
                if game_elements:
                    for i, side_tables in enumerate(game_elements):
                        self.game_found = False
                        tablenum = locator('SIDE TABLES', 'MAIN') + str(i + 1)
                        self.index = tablenum

                        self.actions.move_to_element(side_tables).perform()

                        if game in side_tables.text:
                            self.game_found = True
                            break

                    if self.game_found:
                        if self.task.shuffling(index=self.index): continue
                        if x == 0:
                            table_name = self.handler.getText('SIDE TABLES', 'TABLE NAME', index=tablenum)
                            table_num = self.handler.getText('SIDE TABLES', 'TABLE NUMBER', index=tablenum)
                            self.game_number = table_num
                            print(Fore.LIGHTBLACK_EX + table_name)
                        
                        self.run_tests(test)
                    else:
                        self.task.printText('red', f'{game} not found')
                else:
                    self.task.printText('red', f'game_elements are empty')
            
                self.handler.clickElement('SIDEBET', 'CLOSE')

        self.task.printText('gray', '\n****************************** End of Code ******************************')

    def run_tests(self, test):
        testname = self.task.splitUpperCase(test.__name__)
        self.handler.modules.displayToast('check-circle', 'green', f'{testname}')

        space = self.task.spacer(length=30, element=testname)
        print(f'{testname}:{space} ', end='')

        result = test()

        self.task.printText(('green' if 'P' in result else 'red') if result else 'gray', result)
        self.results.append(result)

    def TestEmptyBetarea(self):
        tests = []

        try:
            """ Test 1 """
            print('\nTest 1')
            self.task.sideBettingTimer(self.index)
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)

            betarea = self.task.randomBet(self.game, 'SIDE BETAREA')
            self.handler.waitElement('SIDE BETAREA', self.game, betarea, index=self.index)
            self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)

            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test1_1 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test1_1)
            
            self.task.waitNextRound(self.index)
            
            # Test 1.2
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test1_2 = self.task.assertion(str(self.chip), bet, operator.ne)
            tests.append(test1_2)

            """ Test 2 """
            print('\nTest 2')
            self.task.sideBettingTimer(self.index)

            # test 2.1
            self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test2_1 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test2_1)

            # test 2.2
            self.handler.clickElement('SIDE BUTTON', 'CANCEL', index=self.index)
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test2_2 = self.task.assertion(str(self.chip), bet, operator.ne)
            tests.append(test2_2)

            # test 2.3
            self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test2_3 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test2_3)

            # test 2.4
            self.task.waitNextRound(self.index)
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test2_4 = self.task.assertion(str(self.chip), bet, operator.ne)
            tests.append(test2_4)

            """ Test 3 """
            print('\nTest 3')
            while True:
                timer = self.handler.getText('SIDE TABLES', 'TIMER', index=self.index)
                if int(timer) < 1: 
                    sleep(2)
                    break
            print('after while loop')
            class_names = self.handler.getClassAttrib('SIDE TABLES', 'BET BUTTON', index=self.index)
            class_name = class_names.split()[-1]
            test3_1 = self.task.assertion('inactive', class_name, operator.eq)
            tests.append(test3_1)
            print('after test 3')
        
        finally:
            if tests == []: tests.append(None)
            else: pass

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
    
    def TestConfirmButton(self):
        tests = []

        try:
            """ test 1 """
            print('\nTest 1')
            # Test 1.1
            self.task.sideBettingTimer(self.index)
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)

            betarea = self.task.randomBet(self.game, 'SIDE BETAREA')
            self.handler.waitElement('SIDE BETAREA', self.game, betarea, index=self.index)
            self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)

            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test1_1 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test1_1)

            # Test 1.2
            self.handler.clickElement('SIDE BUTTON', 'CONFIRM', index=self.index)

            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test1_2 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test1_2)

            # Test 1.3
            msg = self.handler.getText('MULTI', 'VALIDATION', index=self.index)
            test2_3 = self.task.assertion('Bet Successful!', msg, operator.eq)
            tests.append(test2_3)

            """ Test 3 """
            print('\nTest 2')
            # Test 3.1
            self.task.waitNextRound(self.index)
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)

            betarea = self.task.randomBet(self.game, 'SIDE BETAREA')
            self.handler.waitElement('SIDE BETAREA', self.game, betarea, index=self.index)
            self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)

            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test3_1 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test3_1)

            # Test 3.2
            old_balance = self.handler.getText('INGAME', 'BALANCE')
            expected_balance = float(old_balance.replace(',','')) - float(bet)
            expected_balance = round(expected_balance, 2)
            self.handler.clickElement('SIDE BUTTON', 'CONFIRM', index=self.index)
            sleep(2)

            bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
            bet = bet.split('\n')[-1]
            test3_2 = self.task.assertion(str(self.chip), bet, operator.eq)
            tests.append(test3_2)

            # Test 3.3
            actual_balance = self.handler.getText('INGAME', 'BALANCE')
            actual_balance = round(float(actual_balance.replace(',','')), 2)

            test3_3 = self.task.assertion(expected_balance, actual_balance, operator.eq)
            tests.append(test3_3)

            self.task.waitNextRound(self.index)
            self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)

            # Test 4.1
            print('\nTest 4')
            old_balance = self.handler.getText('INGAME', 'BALANCE')
            old_balance = round(float(old_balance.replace(',','')), 2)

            betareas = locator('SIDE BETAREA', self.game)
            for bet in betareas:
                self.handler.clickElement('SIDE BETAREA', self.game, bet)

            expected_betamount = 0
            for bet in betareas:
                bet_text = self.handler.getText('SIDE BETAREA', self.game, bet)
                bet_amount = bet_text.split('\n')[-1]
                expected_betamount += float(bet_amount)

            self.handler.clickElement('SIDE BUTTON', 'CONFIRM', index=self.index)

            expected_betamount = round(expected_betamount, 2)
            expected_balance = old_balance - expected_betamount

            sleep(2)
            actual_balance = self.handler.getText('INGAME', 'BALANCE')
            actual_balance = round(float(actual_balance.replace(',','')), 2)

            test4_1 = self.task.assertion(expected_balance, actual_balance, operator.eq)
            tests.append(test4_1)
            
        except TimeoutException:
            return None

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
    
    def TestPayout(self):
        tests = []

        """ Test 1 """
        print('\nTest 1')
        self.task.sideBettingTimer(self.index)
        self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
        old_balance = self.handler.getText('INGAME', 'BALANCE')
        old_balance = round(float(old_balance.replace(',','')), 2)

        # print(f'\nOld Balance: {old_balance}')

        betarea = self.task.randomBet(self.game, 'SIDE BETAREA')
        self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)

        odds = bet.replace(' ','').split('\n')[1]
        bet_area = bet.replace(' ','').split('\n')[0]

        winning_odd = float(odds.split(':')[-1])
        losing_odd = float(odds.split(':')[0])

        # Test 1.1
        bet = bet.split('\n')[-1]
        test1_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test1_1)

        # Test 1.2
        self.handler.clickElement('SIDE BUTTON', 'CONFIRM', index=self.index)
        bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_2 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test1_2)

        # Test 1.3
        self.handler.waitElement('SIDE TABLES', 'TABLE RESULT', index=self.index)
        self.handler.waitText('SIDE TABLES', 'VALIDATION', index=self.index, text=f'Table {self.game_number}')

        result_msg = self.handler.getText('SIDE TABLES', 'WINNING MASK', index=self.index)
        winnning_msg = self.handler.getText('SIDE TABLES', 'VALIDATION', index=self.index)

        # print(f'\n{winnning_msg}')
        
        win_msg = winnning_msg.split(' ')[2]
        win = True if win_msg == 'Win' else False

        actual_winnings = float(winnning_msg.split(win_msg)[-1].replace(' ', '').replace(',',''))
        actual_payout = self.chip + (actual_winnings)

        if 'Tie' in result_msg:
            expected_payout = 0.0
        else:
            expected_winnings = float(self.chip) * (winning_odd if win else losing_odd)
            expected_payout = float(self.chip) + (expected_winnings if win else -expected_winnings)

        test1_3 = self.task.assertion(expected_payout, actual_payout, operator.eq)
        tests.append(test1_3)

        # test 1.4
        sleep(2)
        actual_balance = self.handler.getText('INGAME', 'BALANCE')
        actual_balance = float(actual_balance.replace(',',''))

        if win:
            expected_balance = (old_balance - float(self.chip)) + actual_payout
        else:
            expected_balance = old_balance - float(self.chip)
        
        expected_balance = round(expected_balance, 2)


        test1_4 = self.task.assertion(expected_balance, actual_balance, operator.eq)
        tests.append(test1_4)

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
    
    def TestAllInBet(self):
        tests = []

        self.task.waitNextRound(self.index)
        self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
        old_balance = self.handler.getText('INGAME', 'BALANCE')
        old_balance = round(float(old_balance.replace(',','')), 2)

        # test 1
        repeat = True
        for index in range(100):
            betareas = locator('SIDE BETAREA', self.game)
            
            for betarea in betareas:
                self.handler.clickElement('SIDE BETAREA', self.game, betarea)
                msg = self.handler.getNonAssertText('SIDE TABLES', 'VALIDATION', index==self.index)
                print(f'Message: {msg}')
                if msg:
                    repeat = False
                    break

            if repeat == False or index == 99: break

        return 'FAILED' if 'FAILED' in tests else 'PASSED'

    def TestBetLimit(self):
        tests = []

        if self.game != 'DT' and self.game != 'BACCARAT' and self.game != 'THREE CARDS': return None

        """ test 1 """
        actual_min = self.betlimit[0]
        actual_max = self.betlimit[1]

        expected_min = locator('BET LIMIT ID', str(self.betcode), 'MIN')
        expected_max = locator('BET LIMIT ID', str(self.betcode), 'MAX')

        test1_1 = self.task.assertion(expected_min, actual_min, operator.eq)
        test1_2 = self.task.assertion(expected_max, actual_max, operator.eq)
        tests.extend([test1_1, test1_2])

        """ test 2 """
        # test 2.1
        below_minimum_bet = int(self.betlimit[0]) - 1
        self.task.changeBetAmount(int(self.betlimit[0]))
        self.task.navigateCurrentTable(self.game)

        self.task.sideBettingTimer(self.index)
        self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
        
        betarea = self.task.randomBet(self.game, 'SIDE MAIN BETAREA')
        self.handler.clickElement('SIDE MAIN BETAREA', self.game, betarea, index=self.index)

        self.handler.clickElement('SIDE BUTTON', 'CONFIRM', index=self.index)

        bet = self.handler.getText('SIDE MAIN BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_1 = self.task.assertion(str(self.chip), bet, operator.ne)

        below_minimum_msg = self.handler.getText('MULTI', 'VALIDATION', index=self.index)

        test2_2 = self.task.assertion('Below Minimum Limit', below_minimum_msg, operator.eq)

        tests.extend([test2_1, test2_2])

        # test 2.2
        above_maximum_bet = int(self.betlimit[1]) + 1
        self.task.changeBetAmount(above_maximum_bet, int(self.betlimit[-1]))
        self.task.navigateCurrentTable(self.game)

        self.task.sideBettingTimer(self.index)
        self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
        
        betarea = self.task.randomBet(self.game, 'SIDE MAIN BETAREA')
        self.handler.clickElement('SIDE MAIN BETAREA', self.game, betarea, index=self.index)
        self.handler.clickElement('SIDE MAIN BETAREA', self.game, betarea, index=self.index)

        above_minimum_msg = self.handler.getText('MULTI', 'VALIDATION', index=self.index)
        test2_2_1 = self.task.assertion('Over Maximum Limit!', above_minimum_msg, operator.eq)

        self.handler.clickElement('SIDE BUTTON', 'CONFIRM', index=self.index)

        bet = self.handler.getText('SIDE MAIN BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_2_2 = self.task.assertion(str(above_maximum_bet), bet, operator.ne)

        tests.extend([test2_2_1, test2_2_2])

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
