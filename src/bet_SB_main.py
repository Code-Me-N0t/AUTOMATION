from src.modules import *
from src.handlers.task_handler import Tasks
from src.handlers.element_handler import Handler
from src.handlers.api_handler import GameAPI
import logging

# Constants
BET_BASE_AMOUNT = 40000
BET_MULTIPLIER = 10000

class speedBaccarat:
    def __init__(self, driver):
        self.driver = driver
        self.handler = Handler(driver)
        self.task = Tasks(self.handler)
        self.actions = ActionChains(driver)
        self.api = GameAPI()
        self.balance = 1000000
        self.game = "BACCARAT"
        self.table = None

    @handle_exceptions
    def main(self, table: str) -> None:
        """Main method to run the baccarat game betting logic."""
        self.table = table
        
        while True:
            self.handler.modules.execJS(f'noFullScreen();')
            self.task.navigateLobby(self.game)
            self.log(f"Navigating to table: {self.table}")
            gamelist = self.handler.getElements('LOBBY', 'TABLE')

            for game in gamelist:
                self.actions.move_to_element(game).perform()

                if self.table in game.text:
                    self.log(f"Entering the table: {self.table}")
                    self.handler.modules.click(game)
                    self.handler.waitElement('INGAME', 'MAIN')

                    result = self.collect_results()

                    if self.is_streak(result):
                        if self.perform_betting_logic(result):
                            self.log(f"Streak ended")
                            # break

                    self.log(f"Exiting the table: {self.table}")
                    self.handler.clickElement('INGAME', 'EXIT')
                    break

    def collect_results(self) -> list:
        """Collect game results and store them in a list."""
        result = []
        
        for _ in range(4):
            message = ''
            while True:
                self.handler.waitElement('INGAME', 'RESULT')
                self.handler.waitText('INGAME', 'VALIDATION', text='No More Bets')
                self.handler.waitElementInvis('INGAME', 'VALIDATION')

                self.handler.waitElement('INGAME', 'VALIDATION')
                message = self.handler.getText('INGAME', 'VALIDATION')
                if message not in ('BANKER WIN!', 'PLAYER WIN!', 'TIE!'):
                    continue
                else:
                    break
            result.append(message)

            self.log(f"Collected Result: {message}")
            self.handler.waitElementInvis('INGAME', 'RESULT')

        return result

    def is_streak(self, result: list) -> bool:
        """Check if all results in the list are the same."""
        if all(x == result[0] for x in result):
            self.log(f"Streak detected: {result}")
            return True
        else:
            self.log('No streak detected')
            return False

    def perform_betting_logic(self, result: list) -> bool:
        """Perform betting logic based on game results."""
        bet_amount = BET_BASE_AMOUNT
        bet_streak = 0

        while True:
            bet_area = 'BANKER' if any('BANKER' in r for r in result) else 'PLAYER'
            did_win = self.bet(bet_area, bet_amount)

            bet_amount += BET_MULTIPLIER
            bet_streak += 1

            if did_win:
                self.log(f"Bet streak: {bet_streak}")
                continue
            else:
                self.log(f"Bet streak ended: {bet_streak}")
                return True

    def bet(self, bet_area: str, bet_amount: int) -> bool:
        """Place a bet and check the result."""
        self.handler.waitText('INGAME', 'VALIDATION', text='Please Place Your Bet!')
        
        self.task.editChips(4000)
        self.place_bet('TIE BETAREA')

        self.task.editChips(bet_amount)
        self.place_bet(f'{bet_area} BETAREA')

        self.handler.clickElement('INGAME', 'CONFIRM')

        self.handler.waitElement('INGAME', 'RESULT WIN')
        message = self.handler.getText('INGAME', 'VALIDATION')
        self.log(f"Bet Result: {message}")

        return True if bet_area in message else False

    def place_bet(self, bet_area: str) -> None:
        """Click on the bet area, retry if intercepted."""
        while True:
            try:
                self.handler.clickElement(bet_area)
                break
            except ElementClickInterceptedException:
                self.handler.waitElementInvis('INGAME', 'RESULT')

    def log(self, log: str) -> None:
        """ customizes log display """
        logging.info(f'{Fore.GREEN}{log}{Fore.LIGHTBLACK_EX}')
