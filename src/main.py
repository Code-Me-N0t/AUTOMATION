from src.modules import *
from src.task_handler import Tasks
from src.element_handler import Handler
from src.updatebalance import update_balance

class Sidebet:
    def __init__(self, driver):
        self.driver = driver
        self.handler = Handler(driver)
        self.task = Tasks(self.handler)
        self.actions = ActionChains(driver)
        self.chip = 202
        self.betlimit = 84
        self.balance = 1000000
        self.index = None
        self.wasClicked = None
        self.game_found = None
        self.game_number = None
        self.game = None
        self.table = None
        self.results = []
        self.testcases = [
            # self.TestEmptyBetarea,
            # self.TestConfirmButton,
            self.TestPayout,
        ]

    @handle_exceptions
    def main(self, game_type):
        self.handler.modules.execJS(f'noFullScreen();')
        self.task.navigateLobby(game_type)
        gamelist = locator(game_type)
        self.game = game_type

        self.handler.clickElement('LOBBY', 'ENTER TABLE')

        for game in gamelist:
            print(Fore.LIGHTBLACK_EX + f'\nTable {game}: ', end='')

            for x, test in enumerate(self.testcases):
                self.task.betIngame()
                
                balance = self.handler.getText('PLAYER', 'BALANCE')

                self.task.editChips(self.chip)
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

        print(Fore.LIGHTBLACK_EX + '\n****************************** End of Code ******************************')

    def run_tests(self, test):
        testname = self.task.splitUpperCase(test.__name__)
        self.handler.modules.displayToast('check-circle', 'green', f'{testname}')

        space = self.task.spacer(length=30, element=testname)
        print(f'{testname}:{space} ', end='')

        result = test()

        self.task.printText(('green' if 'P' in result else 'red') if result else 'gray', result)
        self.results.append(result)

    def TestEmptyBetarea(self):
        """
            Description: Handles the empty betarea assertions

            Test 1: bet placed should not retain when not confirmed
                - places a bet on a random bet area but would not confirm the bet
                - checks the betting area if the bet was placed
                - waits for the round to end
                - checks again if the bet was retained

                Assertions:
                    Test 1.1: Assert bet is placed before the round ends
                    Test 1.2: Assert bet was wiped after the round ends

            Test 2: bet placed should not retain when not confirmed even when canceled once then placed again
                - places a bet on a random bet area but would not confirm
                - checks if the bet was placed
                - cancel the bet
                - checks if the bet was removed
                - place the bet again
                - checks if the bet was placed again
                - waits for the round to end
                - checks again if the bet was retained

                Assertions:
                    Test 2.1: Assert bet is placed before cancel
                    Test 2.2: Assert bet is removed when canceled
                    Test 2.3: Assert bet is placed after cancel
                    Test 2.4: Assert bet is wiped after the round ends

            Test 3: Bet should not be placed when betting in closed betting timer
                - wait for the dealing phase to end
                - check if 'no more bets' displays
                - click a betarea
                - check if there's a chip placed in the betarea

                Assertions:
                    Test 3.1: Assert 'No More Bets' displays
                    Test 3.2: Assert no bet has been placed
        """
        tests = []

        """ Test 1 """
        
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
        while True:
            timer = self.handler.getText('SIDE TABLES', 'TIMER', index=self.index)
            if int(timer) <= 0: 
                sleep(2)
                break

        class_names = self.handler.getClassAttrib('SIDE TABLES', 'BET BUTTON', index=self.index)
        class_name = class_names.split()[-1]
        test3_1 = self.task.assertion('inactive', class_name, operator.eq)
        tests.append(test3_1)

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
    
    def TestConfirmButton(self):
        """
            CONFIRM
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

            Test 2: Confirmed bet should retain even when the dealing phase ends (TBF)
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
        """
        tests = []

        """ test 1 """
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

        return 'FAILED' if 'FAILED' in tests else 'PASSED'
    
    def TestPayout(self):
        """
            Description: Handles the validation of the correct payout of Single, Multiple, and ALL bet area bets

                Test 1: Validate correct payout for SINGLE BET
                - check balance
                - place bet on a single random bet area
                - check if the bet was placed
                - confirm bet
                - check if the bet was retained after confirming
                - wait for the result
                - compute the expected payout
                - get the balance and compute the actual payout
                Assertions:
                    Test 1.1: Assert bet was placed
                    Test 1.2: Assert bet was placed after confirm
                    Test 1.3: Assert payout is correct
                    Test 1.4: Assert balance deduction/addition is correct based on the payout

        """
        tests = []

        """ Test 1 """
        self.task.sideBettingTimer(self.index)
        self.handler.clickElement('SIDE TABLES', 'BET BUTTON', index=self.index)
        old_balance = self.handler.getText('INGAME', 'BALANCE')
        old_balance = round(float(old_balance.replace(',','')), 2)

        # Test 1.1
        betarea = self.task.randomBet(self.game, 'SIDE BETAREA')
        self.handler.clickElement('SIDE BETAREA', self.game, betarea, index=self.index)
        bet = self.handler.getText('SIDE BETAREA', self.game, betarea, index=self.index)

        odds = bet.replace(' ','').split('\n')[1]
        bet_area = bet.replace(' ','').split('\n')[0]

        winning_odd = float(odds.split(':')[-1])
        losing_odd = float(odds.split(':')[0])

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
        
        win_msg = winnning_msg.split(' ')[2]
        win = True if win_msg == 'Win' else False

        actual_winnings = float(winnning_msg.split(win_msg)[-1].replace(' ', '').replace(',',''))
        actual_payout = self.chip + (actual_winnings)

        if 'Tie' in result_msg:
            expected_payout = 0.0
        else:
            expected_winnings = float(self.chip) * (winning_odd if win else losing_odd)
            expected_payout = float(self.chip) + (expected_winnings if win else -expected_winnings)
        
        # if result_msg != 'Win':
        print(f'\n{winnning_msg}')
        print(f'Won?: {win_msg}')
        print(f'Bet Area: {bet_area}')
        print(f'Odds: {odds}')
        print(f'Result Message: {result_msg}')
        print(f'Actual Payout: {actual_payout}\nExpected Payout: {expected_payout}')

        test1_3 = self.task.assertion(expected_payout, actual_payout, operator.eq)
        tests.append(test1_3)

        # test 1.4
        actual_balance = self.handler.getText('INGAME', 'BALANCE')
        actual_balance = float(actual_balance.replace(',',''))

        if win:
            expected_balance = old_balance + actual_payout
        else:
            expected_balance = old_balance - float(self.chip)
        
        expected_balance = round(expected_balance, 2)

        print(f'Old Balance: {old_balance}')
        print(f'Actual Balance: {actual_balance}')
        print(f'Expected Balance: {expected_balance}')

        test1_4 = self.task.assertion(expected_balance, actual_balance, operator.eq)
        tests.append(test1_4)

        return 'FAILED' if 'FAILED' in tests else 'PASSED'

class Multi:
    def __init__(self, driver):
        """ Handles the initialization of the variables and handlers needed """
        self.handler = Handler(driver)
        self.task = Tasks(self.handler)
        self.actions = ActionChains(driver)
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
            # self.TestSwitchTable,
            # self.TestEmptyBetarea,
            # self.TestCancelButton,
            self.TestConfirmButton,
        ]

    @handle_exceptions
    def main(self, game_type):
        """
        Navigates to the game lobby, selects a game table, and runs tests.

        Args:
            game_type (str): Type of game to locate and select.

        Steps:
            1. Navigate to the game lobby.
            2. Retrieve and iterate over the game list.
            3. Update balance and initialize selection state.
            4. For each game, retrieve multi table elements and search for the game.
            5. If game is found, click the table and retrieve table details.
            6. Run test cases if the game is found.
            7. Print a message if the game is not found.
            8. Handle empty game elements.
            9. Wait for navigation to the featured section and lobby main.
        """
        self.task.navigateLobby('MULTI')
        gamelist = locator(game_type)
        self.game = game_type

        for game in range(len(gamelist)):
            update_balance(self.handler.driver, self.balance)
            in_selection = False
            self.wasClicked = None
            print(Fore.LIGHTBLACK_EX+f'Table {gamelist[game]}: ', end='')
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
                else:
                    self.task.printText('red', f'{gamelist[game]} not found')
            else:
                self.task.printText('red', f'game_elements are empty')

            game_elements = self.handler.getElements('MULTI', 'MULTI TABLE')

        self.handler.waitClickable('NAV', 'FEATURED')
        self.handler.waitElement('LOBBY', 'MAIN')

    def run_tests(self, tests):
        """
            Description: Handles the testing of the Testcases

            Function: This will iterate on the list of tests 'self.testcases' and handles the status output of each tests
                TestSwitchTable:
        """
        for test in tests:
            testname = self.task.splitUpperCase(test.__name__)
            self.handler.modules.displayToast('check-circle', 'green', f'{testname}')

            space = self.task.spacer(length=30, element=testname)
            print(f'{testname}:{space} ', end='')
            
            result = test()

            self.task.printText(('green' if 'P' in result else 'red') if result else 'gray', result)
            self.results.append(result)
        return self.results
    
    def TestSwitchTable(self):
        """
            Description: Handles the switch table assertion

            Function: It checks first if the table has been selected through tableselection and stored in wasClicked
                wasClicked is True:
                    • It will do the Switch Table Test
                was Clicked is None:
                    • Will skip the Test since 
                    Reason might be: 
                        - Table was found in Multi displayed table
                        - The table was not found in both Multi tables and Table Selection
        """
        if self.wasClicked:
            table = self.handler.getText('MULTI TABLE', 'TABLE NAME', index=self.index)
            result = self.task.assertion(self.table, table, operator.eq)
        else: result = None
        return result
  
    def TestEmptyBetarea(self):
        """
            Description: Handles the empty betarea assertions

            Test 1: bet placed should not retain when not confirmed
                - places a bet on a random bet area but would not confirm the bet
                - checks the betting area if the bet was placed
                - waits for the round to end
                - checks again if the bet was retained

                Assertions:
                    Test 1.1: Assert bet is placed before the round ends
                    Test 1.2: Assert bet was wiped after the round ends

            Test 2: bet placed should not retain when not confirmed even when canceled once then placed again
                - places a bet on a random bet area but would not confirm
                - checks if the bet was placed
                - cancel the bet
                - checks if the bet was removed
                - place the bet again
                - checks if the bet was placed again
                - waits for the round to end
                - checks again if the bet was retained

                Assertions:
                    Test 2.1: Assert bet is placed before cancel
                    Test 2.2: Assert bet is removed when canceled
                    Test 2.3: Assert bet is placed after cancel
                    Test 2.4: Assert bet is wiped after the round ends

            Test 3: Bet should not be placed when betting in closed betting timer
                - wait for the dealing phase to end
                - check if 'no more bets' displays
                - click a betarea
                - check if there's a chip placed in the betarea

                Assertions:
                    Test 3.1: Assert 'No More Bets' displays
                    Test 3.2: Assert no bet has been placed
        """
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
        """
            Description: Tests the Function Buttons: Cancel, Confirm, and Supersix for Baccarat

            Functions:
                • CANCEL
                    Test 1: Bet should be wiped when unconfirmed bet was canceled
                        - Place bet
                        - check if bet was placed
                        - cancel bet
                        - check if bet was removed
                        Assertions:
                            Test 1.1: Assert bet was placed
                            Test 1.2: Assert bet was removed

                    Test 2: Bet should not be canceled when confirmed
                        - place bet
                        - check if bet was placed
                        - cancel bet
                        - check if bet was removed
                        - place bet again
                        - confirm bet
                        - click cancel button
                        - check if bet retains
                        Assertions:
                            Test 2.1: assert bet was placed
                            Test 2.2: assert bet was removed
                            Test 2.3: assert bet was placed again
                            Test 2.4: assert 'bet successful' displays when confirmed
                            Test 2.5: assert bet retains
        """
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

        """ Test 1 """

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
            tests.append('PASSED')
        else:
            tests.append('FAILED')

        """ Test 3 """
        self.task.nextRound(self.index)
        balance = self.handler.getText('MULTI', 'BALANCE')
        old_balance = round(float(balance.replace(',','')), 2)
        print(f'Test 3: Old Balance: {old_balance}')

        # Test 3.1
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
        balance = self.handler.getText('MULTI', 'BALANCE')
        actual_balance = round(float(balance.replace(',','')), 2)
        bet_placed = old_balance - actual_balance
        test3_3 = self.task.assertion(float(self.chip), bet_placed, operator.eq)
        tests.append(test3_3)

        print(f'Test 3: New Balance: {actual_balance}')

        """ Test 4 """
        # balance = self.handler.getText('MULTI', 'BALANCE')
        # old_balance = round(float(balance.replace(',','')), 2)
        # self.task.nextRound(self.index)
        
        # # Test 4.1
        # betareas = self.handler.getElements('BETAREAS', self.game, index=self.index)
        # for bet in betareas:
        #     self.handler.modules.click(bet)
        
        # for bet in betareas:
        #     placed_bet = bet.text.split('\n')[-1]
        #     test4_1 = self.task.assertion(str(self.chip), placed_bet, operator.eq)
        #     tests.append(test4_1)
        # # Test 4.2
        # self.handler.clickElement('BUTTON', 'CONFIRM', index=self.index)

        # for bet in betareas:
        #     placed_bet = bet.text.split('\n')[-1]
        #     test4_2 = self.task.assertion(str(self.chip), placed_bet, operator.eq)
        #     tests.append(test4_2)

        # print('\ntest 4.3')
        # # Test 4.3
        # for bet in range(len(betareas)):
        #     bet_amount = self.chip * (bet + 1)

        # balance = self.handler.getText('MULTI', 'BALANCE')
        # actual_balance = round(float(balance.replace(',','')), 2)
        # bet_placed = old_balance - actual_balance
        # test4_3 = self.task.assertion(float(bet_amount), bet_placed, operator.eq)
        
        # print(f'Test 3: Old Balance: {old_balance}')
        # print(f'Test 3: New Balance: {actual_balance}')

        # print(f'Expected: {bet_amount}')
        # print(f'Actual: {bet_placed}')
        # tests.append(test4_3)


        return 'FAILED' if 'FAILED' in tests else 'PASSED'
