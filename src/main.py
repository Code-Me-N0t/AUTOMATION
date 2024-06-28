from src.modules import *
from src.task_handler import Tasks
from src.element_handler import Handler
from src.assert_handler import Assert
from src.updatebalance import *


class Multi:
    def __init__(self, driver):
        """ handles the initialization of the variables and functions needed """
        self.handler =  Handler(driver)
        self.task =     Tasks(self.handler)
        self.asserts =  Assert(self.handler)
        self.chip = 201
        self.betlimit = 84
        self.balance = 1000000
        self.index = None
        self.wasClicked = None
        self.actions = ActionChains(driver)
        self.game_found = None
        self.table = None
        self.results = []
        self.testcases = [
            self.TestSwitchTable,
        ]

    @handle_exceptions
    def main(self, game_type):
        self.task.navigateLobby('MULTI')
        gamelist = locator(game_type)

        for game in range(len(gamelist)):
            update_balance(self.handler.driver, self.balance)
            in_selection = False
            self.wasClicked = None
            print(Fore.GREEN+f'Table {gamelist[game]}: ', end='')
            game_elements = self.handler.getElements('MULTI', 'MULTI TABLE')

            if game_elements:
                for i in range(len(game_elements)):  # in multi page
                    multi_tables = game_elements[i]
                    self.game_found = False

                    tablenum = locator('MULTI TABLE', 'MAIN') + str(i + 1)
                    self.index = tablenum

                    if gamelist[game] not in multi_tables.text and not in_selection:
                        self.handler.waitClickable('MULTI', 'TABLE SWITCH', index=tablenum)
                        select = self.handler.getElements('MULTI', 'MINI TABLECARD')

                        for x in range(len(select)):  # in table selection modal
                            tableselection = select[x]
                            self.actions.move_to_element(tableselection).perform()
                            in_selection = True

                            if gamelist[game] in tableselection.text:
                                self.wasClicked = click_highlighter(self.handler.driver, tableselection)
                                self.game_found = True
                                self.table = gamelist[game]
                                break
                    else:
                        self.game_found = True
                    
                    if self.game_found:
                        table_details = self.handler.getText('MULTI TABLE', 'TABLE DETAILS', index=tablenum)
                        print(Fore.GREEN + table_details)
                        break
                    elif not self.game_found and in_selection: # game not found in current index 
                        self.handler.clickElement('MULTI', 'CLOSE SIDETABLE')
                    else:
                        print('Unhandled condition')
                        
                if self.game_found:  # tests here
                    self.run_tests(self.testcases)
                else: 
                    self.task.printText('red', f'{gamelist[game]} not found')
            else: 
                self.task.printText('red', f'game_elements are empty')

            game_elements = self.handler.getElements('MULTI', 'MULTI TABLE')

        self.handler.waitClickable('NAV', 'FEATURED')
        self.handler.waitElement('LOBBY', 'MAIN')

    def run_tests(self, tests):
        """  """
        space = self.task.spacer()
        for test in tests:
            print(f'{test.__name__}:{space} ', end='')
            result = test()
            print(result)
            self.results.append(result)
        return self.results
    
    def TestSwitchTable(self):
        if self.wasClicked:
            displayToast(self.handler.driver, 'check-circle', 'green', 'TABLE SWITCH')
            table = self.handler.getText('MULTI TABLE', 'TABLE NAME', index=self.index)
            try:
                assert self.table == table
                result = 'PASSED'
            except AssertionError:
                result = 'FAILED'
        else:
            result = None
        return result
    
    def multiple_bet(self):
        print('multiple bet')
        result = 'PASSED'
        return result
    
    def allin_bet(self):
        print('allin bet')
        result = 'PASSED'
        return result
    
    def bet_limit(self):
        print('bet limit')
        result = 'PASSED'
        return result

    

def update_scenarios(games):
    if games == 'all': games = ['BACCARAT', 'DT', 'SICBO', 'SEDIE']
    print(' \n')

    for game in games:
        cell = locator("CELL", f"{game}")
        print(f'{Fore.GREEN}Updated game scenario: {game}')

        for index, (name, values) in enumerate(scenarios.items()):
            if values and name:
                if game not in ['BACCARAT', 'DT'] and name in ['Card Result', 'Flipped Cards', 'Bet Within Bet Pool']: continue
                if name == 'Bet On Super Six' and game != 'BACCARAT': continue
                update_spreadsheet(values, f"C{(cell + index)}")

def PlayMulti(driver, game, test, report=None, index=None, new_balance=1000000):
    navigateTab(driver, "MULTI")
    TH.navigateLobby
    gameTable = locator(game)
    actions = ActionChains(driver)

    try:
        for selectedGame in range(len(gameTable)):
            update_balance(driver, new_balance)
            printText('title', f"\nFinding: {gameTable[selectedGame]}")
            
            game_found = False
            elements = findElements(driver, "MULTI", "MULTI TABLE")
            for i in range(len(elements)):
                in_tableselection = False
                name = elements[i]
                tableNum = locator("MULTI TABLE", "MAIN") + str(i + 1) + ")"
                while name.text == '':
                    continue
                if gameTable[selectedGame] not in name.text and in_tableselection == False:
                    waitModClickable(driver, "MULTI", "TABLE SWITCH", table=tableNum)
                    select = findElements(driver, "MULTI", "MINI TABLECARD")
                    for x in range(len(select)):
                        actions.move_to_element(select[x]).perform()
                        if gameTable[selectedGame] in select[x].text:
                            click_highlighter(driver, select[x], True)
                            game_found = True
                            break
                        else:
                            continue
                    elements = findElements(driver, "MULTI", "MULTI TABLE")
                    name = elements[i]
                    if gameTable[selectedGame] not in name.text and game_found == False:
                        waitClickable(driver, "MULTI", "CLOSE SIDETABLE")
                    if game_found:
                        in_tableselection = True
                        break
                else:
                    game_found = True
                    break

            if game_found:  # PLACE BET
                chip = int(data['chip value'])
                balance = findElement(driver, "MULTI", "USER BALANCE")

                printText('title', f'Table {gameTable[selectedGame]} found')
                displayToast(driver, 'check-circle', 'green', f'Game Table: {gameTable[selectedGame]}')
                betArea = randomizeBetarea(game)

                BettingTimer(driver, tableNum)
                
                # TEST CASES
                if test == 'betlimit' and index is not None:
                    betLimit(driver, 
                             game, 
                             index, 
                             gameTable[selectedGame], 
                             tableNum, 
                             betArea)
                elif test == 'singlebet':
                    singleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)
                elif test == 'multiplebet':
                    multipleBet(driver, game, gameTable[selectedGame], tableNum, chip, balance, betArea)
                elif test == 'allinbet':
                    allInBet(driver, game, gameTable[selectedGame], tableNum, chip, balance)
                else: print(Fore.RED + 'Invalid test parameters')

                # end of code
            if not game_found:
                printText('failed', f'Table {gameTable[selectedGame]} not found')

            elements = findElement(driver, "MULTI", "MULTI TABLE")
        printText('body', '\n************************** report summary **************************')

    except ValueError as e: printText('failed', e)

    except Exception as e: 
        printText('failed', e)
        pass

    # report
    if report is not None: multiReportSheet(report, game, test_status)

    waitClickable(driver, "NAV", "FEATURED")
    waitElement(driver, "LOBBY", "MAIN")

def betLimit(driver, game, index, gametable, tablenum, betarea):
    findElement(driver, 'PLAYER', 'AVATAR', click=True)
    waitElement(driver, 'PLAYER', 'MAIN')
    betlimit = findElement(driver, 'PLAYER', 'BET LIMIT')
    getText = betlimit.text.split(' ')
    actual_min = int(getText[0])
    actual_max = int(getText[-1])
    expected_min = locator('BET LIMIT ID', str(index), 'MIN')
    expected_max = locator('BET LIMIT ID', str(index), 'MAX')

    # bet correction
    assertion(driver, 'Correct Bet Limit Assertion', actual_min, expected_min, operator.eq, test_status['Correct Bet Limit'], gametable, scenarios['Correct Bet Limit'])
    assertion(driver, 'Correct Bet Limit Assertion', actual_max, expected_max, operator.eq, test_status['Correct Bet Limit'], gametable, scenarios['Correct Bet Limit'])
    
    findElement(driver, 'PLAYER', 'CLOSE', click=True)

    # assert can bet with lowest and highest bet
    WithinBetLimit(driver, f'Bet within bet limit [MIN: {actual_min}]', game, gametable, tablenum, betarea, actual_min, test_status, scenarios)
    WithinBetLimit(driver, f'Bet within bet limit [MAX: {actual_max}]', game, gametable, tablenum, betarea, actual_max, test_status, scenarios)

    # place below && over betlimit
    BelowAboveBetlimit(driver, 'Below Minimum Limit', game, gametable, tablenum, betarea, actual_min, test_status, scenarios)
    BelowAboveBetlimit(driver, 'Over Maximum Limit!', game, gametable, tablenum, betarea, actual_max, test_status, scenarios)

    # place below betlimit but within betpool
    if game == 'BACCARAT' or game == 'DT': WithinBetPool(driver, gametable, tablenum, actual_min, test_status, scenarios)
    else: printText('body', f'Bet Within Bet Pool is not available in {game}')

def singleBet(driver, game, gametable, tablenum, chip, balance, betArea):
    displayToast(driver, 'check-circle', 'green', 'SINGLE BET')
    printText('title', 'TEST: SINGLE BET')
    EditChips(driver, chipValue=chip)
    oldBalance = round(float(balance.text.replace(',','')), 2)
    
    TableSwitch(driver, tablenum, gametable, test_status, scenarios)
    CancelBet(driver, game, gametable, chip, tablenum, betArea, test_status,scenarios)
    UnconfirmedBet(driver, game, gametable, tablenum, chip, betArea, test_status,scenarios)
    BetSuccessful(driver, game, gametable, tablenum, betArea, test_status,scenarios)
    BalanceDeduction(driver, gametable, oldBalance, chip, test_status,scenarios)
    betPlaced = findModElement(driver, "MULTI BETTINGAREA", game, betArea, table=tablenum)
    PlaceBet(driver, betPlaced, 'Single Bet Assertion', gametable, str(chip), test_status['Single Bet'], scenarios['Single Bet'])
    NoMoreBets(driver, gametable, tablenum, test_status,scenarios)
    ClosedBetTimer(driver, game, gametable, tablenum, betArea, test_status, scenarios)
    if game == 'BACCARAT' or game == 'DT': b, r = sample_func(driver, game, gametable, tablenum, test_status)
    Payout(driver, game, gametable, balance, oldBalance, betArea, test_status, chip, scenarios)
    EmptyBetarea(driver, gametable, chip, test_status, betPlaced, scenarios)
    if game == 'BACCARAT' or game == 'DT': BetRecord(driver, game, gametable, b, r, tablenum, test_status)
    if game == 'BACCARAT': superSix(driver, gametable, tablenum, test_status, scenarios)
        
def multipleBet(driver, game, gametable, tablenum, chip, balance, betarea):
    displayToast(driver, 'check-circle', 'green', 'MULTIPLE BET')
    print('\n')
    printText('title', 'TEST: MULTIPLE BET')
    EditChips(driver, chipValue=chip)

    oldBalance = round(float(balance.text.replace(',','')), 2)
    BettingTimer(driver, tablenum, timer=14)

    waitBetMask(driver, 'MULTI TABLE', 'BET MASK', table=tablenum)
    betarea_element = findModElements(driver, 'MULTIPLE BETTINGAREA', game, table=tablenum)
    for bet in betarea_element: click_highlighter(driver, bet, True)
    findModElement(driver, 'MULTI BUTTON', 'CONFIRM', click=True, table=tablenum)
    validate = waitModText(driver, 'MULTI', 'VALIDATION', text='Bet Successful!', table=tablenum, time=10)
    assertion(driver,'Bet Successful Assertion', validate, True, operator.eq, test_status['Bet Successful'],gametable, scenarios['Bet Successful'])

    for bets in range(len(betarea_element)): betamount = chip * (bets+1)

    BalanceDeduction(driver, gametable, oldBalance, betamount, test_status,scenarios)
    for bet in betarea_element: PlaceBet(driver, bet, 'Multiple Bet Assertion', gametable, str(chip), test_status['Multiple Bet'],scenarios['Multiple Bet'])
    NoMoreBets(driver, gametable, tablenum, test_status,scenarios)
    ClosedBetTimer(driver, game, gametable, tablenum, betarea, test_status, scenarios)
    Payout(driver, game, gametable, balance, oldBalance, betarea, test_status, betamount, scenarios)
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)

def allInBet(driver, game, gametable, tablenum, chip, balance):
    displayToast(driver, 'check-circle', 'green', 'ALL IN BET')
    printText('title', 'TEST: ALL IN BET')
    EditChips(driver, chipValue=chip)

    # scenario 1: validate 'Insufficient Bet' displayed
    # print('scenario 1')
    message = getInsufficientText(driver, game, tablenum)
    # print('scenario 1.1')
    while message == '': continue
    # print('scenario 1.2')
    validation_message = message
    
    # scenario 2: all in then cancel, validate betarea is empty
    has_chip = False
    waitModClickable(driver, 'MULTI BUTTON', 'CANCEL', table=tablenum)
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)

    bet_placed = findModElements(driver, 'MULTI TABLE', 'BET PLACED', table=tablenum)
    for bet_area in bet_placed:
        if 'hidden-chip' not in bet_area.get_attribute('class'): has_chip = True
    
    waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)

    # scenario 3: all in then do not confirm, validate next round betting area is empty
    # print('scenario 3')
    not_empty = False
    _ = getInsufficientText(driver, game, tablenum)

    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)
    waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)

    bet_placed = findModElements(driver, 'MULTI TABLE', 'BET PLACED', table=tablenum)
    for bet_area in bet_placed:
        if 'hidden-chip' not in bet_area.get_attribute('class'): not_empty = True

    # scenario 4: all in bet then click confirm, validate bet successful displayed
    # print('scenario 4')
    _ = getInsufficientText(driver, game, tablenum)
    waitModClickable(driver, 'MULTI BUTTON', 'CONFIRM', table=tablenum)

    for _ in range(100):
        validate = findModElement(driver, 'MULTI', 'VALIDATION', table=tablenum)
        validate_bet = validate.text
        if validate_bet == "Bet Successful!": break
        sleep(.5)

    # scenario 5: validate balance remaining should be zero
    # print('scenario 5')
    waitModElement(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)
    remaining_balance = round(float(balance.text.replace(',','')), 2)

    # assertion: assert all scenarios passed
    # print('assertion')
    assertion(driver, 'All In Bet', 
              [validation_message, has_chip, not_empty, validate_bet, remaining_balance], 
              ['Insufficient Balance', False, False, 'Bet Successful!', 0], 
              operator.eq, 
              test_status['All In Bet'], 
              gametable, 
              scenarios['All In Bet'])
    
    waitModElementInvis(driver, "MULTI TABLE", "TABLE RESULT", table=tablenum)
