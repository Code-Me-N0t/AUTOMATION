from src.modules import *
from src.handlers.task_handler import Tasks
from src.handlers.element_handler import Handler
from src.handlers.api_handler import GameAPI
import logging

# Define constants
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
        self.handler.modules.execJS(f'noFullScreen();')
        self.table = table

        while True:
            self.task.navigateLobby(self.game)
            logging.info(f"Navigating lobby to find table {self.table}")
            gamelist = self.handler.getElements('LOBBY', 'TABLE')

            for game in gamelist:
                self.actions.move_to_element(game).perform()

                if self.table in game.text:
                    logging.info(f"Entering table {self.table}")
                    self.handler.modules.click(game)
                    self.handler.waitElement('INGAME', 'MAIN')

                    result = self.collect_results()

                    if len(result) >= 2 and self.is_streak(result):
                        if self.perform_betting_logic(result):
                            logging.info(f"Streak ended. Exiting table {self.table} and re-entering.")
                            break  # Exit the game and re-enter the table

                    logging.info(f"Exiting the table {self.table}")
                    self.handler.clickElement('INGAME', 'EXIT')
                    break  # Exit to lobby and loop back to re-enter the table

    def collect_results(self) -> list:
        """Collect game results and store them in a list."""
        result = []
        for _ in range(4):
            self.handler.waitElement('INGAME', 'RESULT WIN')
            message = self.handler.getText('INGAME', 'VALIDATION')
            result.append(message)

            logging.info(f"Collected Result: {message}")
            self.handler.waitElementInvis('INGAME', 'RESULT')

        return result

    def is_streak(self, result: list) -> bool:
        """Check if all results in the list are the same."""
        if all(x == result[0] for x in result):
            logging.info(f"Streak detected: {result}")
            return True
        else:
            logging.info("No streak detected.")
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
                logging.info(f"Bet succeeded. Continuing betting. Bet streak: {bet_streak}")
                continue
            else:
                logging.info(f"Bet failed. Ending bet streak at {bet_streak}.")
                return True  # Exit to the lobby

    def bet(self, bet_area: str, bet_amount: int) -> bool:
        """Place a bet and check the result."""
        self.handler.waitText('INGAME', 'VALIDATION', text='Please Place Your Bet!')
        self.task.editChips(4000)

        # Place bet on tie if applicable
        self.place_bet('TIE BETAREA')

        # Adjust chip amount and place bet on designated area
        self.task.editChips(bet_amount)
        self.place_bet(f'{bet_area} BETAREA')

        # Confirm bet
        self.handler.clickElement('INGAME', 'CONFIRM')

        # Check the result of the bet
        self.handler.waitElement('INGAME', 'RESULT WIN')
        message = self.handler.getText('INGAME', 'VALIDATION')
        logging.info(f"Bet Result: {message}")

        return True if bet_area in message else False

    def place_bet(self, bet_area: str) -> None:
        """Click on the bet area, retry if intercepted."""
        while True:
            try:
                self.handler.clickElement(bet_area)
                break
            except ElementClickInterceptedException:
                self.handler.waitElementInvis('INGAME', 'RESULT')