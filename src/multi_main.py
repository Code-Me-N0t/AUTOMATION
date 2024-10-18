from src.modules import *
from src.handlers.task_handler import Tasks
from src.handlers.element_handler import Handler
from src.handlers.api_handler import GameAPI

class Multi:
    def __init__(self, driver):
        self.handler = Handler(driver)
        self.task = Tasks(self.handler)
        self.actions = ActionChains(driver)
        self.api = GameAPI()
        self.chip = 201
        self.betlimit = 84
        self.balance = 1000000
        self.index = None
        self.wasClicked = None
        self.game_found = None
        self.game = None
        self.table = None
        self.results = []
        self.testcases = [
            self.TestSwitchTable,
            self.TestEmptyBetarea,
            self.TestCancelButton,
            self.TestConfirmButton,
        ]

    @handle_exceptions
    def main(self, game_type):
        self.task.navigateLobby('MULTI')
        gamelist = locator(game_type)
        self.game = game_type

        for game in range(len(gamelist)):
            self.api.update_balance(self.balance)
            self.handler.driver.refresh()

            in_selection = False
            self.wasClicked = None
            game_elements = self.handler.getElements('MULTI', 'MULTI TABLE')

            if game_elements:
                for i in range(len(game_elements)):
                    multi_tables = game_elements[i]
                    self.game_found = False
                    tablenum = locator('MULTI TABLE', 'MAIN') + str(i + 1)
                    self.index = tablenum

                    if gamelist[game] not in multi_tables.text and not in_selection:
                        self.handler.waitClickable('MULTI', 'TABLE SWITCH', index=tablenum)
                        select = self.handler.getElements('MULTI', 'MINI TABLECARD')

                        for x in range(len(select)):
                            tableselection = select[x]
                            self.actions.move_to_element(tableselection).perform()
                            in_selection = True

                            if gamelist[game] in tableselection.text:
                                self.wasClicked = self.handler.modules.click(tableselection)
                                self.game_found = True
                                self.table = gamelist[game]
                                break
                    elif gamelist[game] not in multi_tables.text and in_selection:
                        continue
                    else:
                        self.game_found = True
                    
                    if self.game_found:
                        table_details = self.handler.getText('MULTI TABLE', 'TABLE DETAILS', index=tablenum)
                        print(Fore.LIGHTBLACK_EX + table_details)
                        break
                    elif not self.game_found and in_selection:
                        self.handler.clickElement('MULTI', 'CLOSE SIDETABLE')
                
                if self.game_found:
                    self.run_tests(self.testcases)
                    print()
                else:
                    self.task.printText('red', f'{gamelist[game]} not found')
            else:
                self.task.printText('red', f'game_elements are empty')

            game_elements = self.handler.getElements('MULTI', 'MULTI TABLE')

        self.handler.waitClickable('NAV', 'FEATURED')
        self.handler.waitElement('LOBBY', 'MAIN')

    def run_tests(self, tests):
        max_testname_length = max([len(self.task.splitUpperCase(test.__name__)) for test in tests])

        results = []
        
        for test in tests:
            testname = self.task.splitUpperCase(test.__name__)
            self.handler.modules.displayToast('check-circle', 'green', f'{testname}')

            space = self.task.spacer(length=30, element=testname)
            print(f'{testname}:{space} ', end='')

            result = test()
            
            self.task.printText(('green' if 'P' in result else 'red') if result else 'gray', result)
            if result:
                result_str = '✅' if 'P' in result else '❌'
                
                spacee = '.' * (max_testname_length - len(testname))
                
                results.append({
                    'testname': testname,
                    'result': f'{spacee}{result_str}'
                })
        
        # self.handler.modules.sendTG(results)
        return self.results
    
    def TestSwitchTable(self):
        if self.wasClicked:
            table = self.handler.getText('MULTI TABLE', 'TABLE NAME', index=self.index)
            result = self.task.assertion(self.table, table, operator.eq)
        else: result = None
        return result
  
    def TestEmptyBetarea(self):
        tests = []

        """ Test 1 """
        self.task.nextRound(self.index)
        self.task.editChips(self.chip)

        # Test 1.1
        betarea = self.task.randomBet(self.game, 'BETAREA')

        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test1_1)

        self.task.nextRound(self.index)

        # Test 1.2
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_2 = self.task.assertion(str(self.chip), bet, operator.ne)
        tests.append(test1_2)

        """ Test 2 """
        self.task.nextRound(self.index)

        # test 2.1
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_1)

        # test 2.2
        self.handler.clickElement('BUTTON', 'CANCEL', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_2 = self.task.assertion(str(self.chip), bet, operator.ne)
        tests.append(test2_2)

        # test 2.3
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_3 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_3)

        # test 2.4
        self.task.nextRound(index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_4 = self.task.assertion(str(self.chip), bet, operator.ne)
        tests.append(test2_4)

        """ Test 3 """
        
        # Test 3.1
        self.handler.waitElement('MULTI TABLE', 'TABLE RESULT', time=20, index=self.index)
        msg = self.handler.getText('MULTI', 'VALIDATION', index=self.index)
        test3_1 = self.task.assertion('No More Bets!', msg, operator.eq)
        tests.append(test3_1)

        # Test 3.2
        element = self.handler.getElements('MULTI TABLE', 'BET MASK', index=self.index)
        test3_2 = self.task.assertion(len(element), 0, operator.ne)
        tests.append(test3_2)

        return 'FAILED' if 'FAILED' in tests else 'PASSED' 
        
    def TestCancelButton(self):
        tests = []

        self.task.nextRound(self.index)
        self.task.editChips(self.chip)
        betarea = self.task.randomBet(self.game, 'BETAREA')

        """ CANCEL """
        # Test 1.1
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test1_1)

        # Test 1.2
        self.handler.clickElement('BUTTON', 'CANCEL', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_2 = self.task.assertion(str(self.chip), bet, operator.ne)
        tests.append(test1_2)

        self.task.nextRound(self.index)
        # Test 2.1
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_1)

        # Test 2.2
        self.handler.clickElement('BUTTON', 'CANCEL', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_2 = self.task.assertion(str(self.chip), bet, operator.ne)
        tests.append(test2_2)

        # Test 2.3
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_3 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_3)

        # Test 2.4
        self.handler.clickElement('BUTTON', 'CONFIRM', index=self.index)
        msg = self.handler.getText('MULTI', 'VALIDATION', index=self.index)
        test2_4 = self.task.assertion('Bet Successful!', msg, operator.eq)
        tests.append(test2_4)

        # Test 2.5
        self.handler.clickElement('BUTTON', 'CANCEL', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_5 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_5)

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
    
    def TestConfirmButton(self):
        """
            • CONFIRM
                Test 1: Validate 'Bet Successful' display when confirmed
                    - place bet
                    - check if bet was placed
                    - confirm the bet
                    - check if bet was placed
                    - check if 'bet successful' displays
                    Assertions:
                        Test 1.1: Assert bet was placed
                        Test 1.2: Assert bet was placed after confirming
                        Test 1.3: Assert message displayed

                Test 2: Confirmed bet should retain even when the dealing phase ends
                    - place bet
                    - check if bet was placed
                    - confirm bet
                    - check if bet was placed
                    - wait for dealing phase to end
                    - check if the bet was retained
                    Assertions:
                        Test 2.1: Assert bet was placed
                        Test 2.2: Assert bet was placed after confirming
                        Test 2.3: Assert bet retained after dealing phase

                Test 3: Confirmed bet should deduct correctly for single bet
                    - check balance
                    - place bet
                    - check if bet was placed
                    - confirm bet
                    - check if bet was placed
                    - check if the balance was deducted correctly
                    Assertions:
                        Test 3.1: Assert bet was placed
                        Test 3.2: Assert bet was placed after confirming
                        Test 3.3: Assert balance was correctly deducted

                Test 4: Confirmed bet should deduct correctly for multiple bet
                    - check balance
                    - place bet on all betting areas
                    - check if all bets was placed
                    - confirm all bets
                    - check if all bets was placed after confirming
                    - check if the balance was deducted correctly
                    Assertions:
                        Test 4.1: Assert bets was placed
                        Test 4.2: Assert bets was placed after confirming
                        Test 4.3: Assert bets was correctly deducted

                Test 5: Should deduct balance correctly for multiple confirmed bets
                Test 6: Confirmed bet should deduct correctly for all in bet
        """
        tests = []

        self.task.nextRound(self.index)
        self.task.editChips(self.chip)
        betarea = self.task.randomBet(self.game, 'BETAREA')

        # """ Test 1 """

        # Test 1.1
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test1_1)

        # Test 1.2
        self.handler.clickElement('BUTTON', 'CONFIRM', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test1_2 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test1_2)

        # Test 1.3
        msg = self.handler.getText('MULTI', 'VALIDATION', index=self.index)
        test1_3 = self.task.assertion('Bet Successful!', msg, operator.eq)
        tests.append(test1_3)

        """ Test 2 """
        self.task.nextRound(self.index)

        # Test 2.1
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_1)

        # Test 2.2
        self.handler.clickElement('BUTTON', 'CONFIRM', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test2_2 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test2_2)

        # Test 2.3
        bet = self.handler.getElement('BETAREA', self.game, betarea, index=self.index)
        user_bet = bet.find_element( 
            By.CSS_SELECTOR, ':scope > div:nth-child(1) > div:nth-child(3)'
        )
        if 'hidden-chip' not in user_bet.get_attribute('class'):
            test2_3 = 'PASSED'
        else:
            test2_3 = 'FAILED'
        tests.append(test2_3)

        """ Test 3 """
        self.task.nextRound(self.index)
        balance = self.handler.getText('MULTI', 'BALANCE')
        old_balance = round(float(balance.replace(',','')), 2)

        # Test 3.1
        betarea = self.task.randomBet(self.game, 'BETAREA')
        self.handler.clickElement('BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test3_1 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test3_1)

        # Test 3.2
        self.handler.clickElement('BUTTON', 'CONFIRM', index=self.index)
        bet = self.handler.getText('BETAREA', self.game, betarea, index=self.index)
        bet = bet.split('\n')[-1]
        test3_2 = self.task.assertion(str(self.chip), bet, operator.eq)
        tests.append(test3_2)

        # Test 3.3
        sleep(2)
        new_balance = self.handler.getText('MULTI', 'BALANCE')
        actual_balance = round(float(new_balance.replace(',','')), 2)

        bet_amount = old_balance - actual_balance if old_balance > actual_balance else actual_balance - old_balance
        bet_amount = round(bet_amount, 2)
        test3_3 = self.task.assertion(float(self.chip), bet_amount, operator.eq)
        tests.append(test3_3)

        """ Test 4 """
        balance = self.handler.getText('MULTI', 'BALANCE')
        old_balance = round(float(balance.replace(',','')), 2)
        print(f'\nOld Balance: {old_balance}')
        self.task.nextRound(self.index)
        
        # Test 4.1
        betareas = self.handler.getElements('BETAREAS', self.game, index=self.index)
        for bet in betareas:
            self.handler.modules.click(bet)
        
        for bet in betareas:
            placed_bet = bet.text.split('\n')[-1]
            test4_1 = self.task.assertion(str(self.chip), placed_bet, operator.eq)
            tests.append(test4_1)

        # Test 4.2
        self.handler.clickElement('BUTTON', 'CONFIRM', index=self.index)

        for bet in betareas:
            placed_bet = bet.text.split('\n')[-1]
            test4_2 = self.task.assertion(str(self.chip), placed_bet, operator.eq)
            tests.append(test4_2)

        # Test 4.3
        sleep(2)
        for bet in range(len(betareas)):
            bet_amount = self.chip * (bet + 1)

        balance = self.handler.getText('MULTI', 'BALANCE')
        actual_balance = round(float(balance.replace(',','')), 2)
        print(f'Actual Balance: {actual_balance}')
        bet_placed = old_balance - actual_balance
        test4_3 = self.task.assertion(float(bet_amount), float(bet_placed), operator.eq)

        if test4_3 == 'FAILED':
            print(f'\nExpected: {bet_placed}\nActual: {float(bet_amount)}')
        tests.append(test4_3)

        self.task.nextRound(self.index)

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
