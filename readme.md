This pytest automation script is designed to test various functionalities of a gaming web application. Below is a brief overview of the script files and their functionalities:

test.py

• This file contains test functions prefixed with "test_" that are executed by pytest.
• Test cases are organized using the playMulti(driver, game, test, report=True) function, which performs actions like playing multiple games, placing bets, and validating results.
• Each test case is associated with a specific game and test type (e.g., "BET LIMIT" or "PLACE BET").
• The script imports functions from src.modules and src.main modules to execute test scenarios.
• Error handling is implemented using try-except blocks to catch exceptions and print error messages.
• Finally, the script ensures that the WebDriver is properly closed after test execution.

Terminal Commands:
"pytest"    : Runs the script in normal conditions
"-v"        : Increases the verbosity of the output
"-s"        : Show inputs 
"-m"        : Markers (for excluding tests) e.g: pytest -s -m "not (update_scenario or multiple_bet or betlimit or allin)"

main.py

• This file contains functions that define various test scenarios.
• The playMulti(driver, game, test, report=True) function orchestrates the execution of test cases by navigating to different game tables, placing bets, and validating outcomes.
• Test data and test case details are stored in dictionaries for easy access and reporting.
• Helper functions from src.modules are used to interact with the web application, locate elements, input values, and validate results.
• Specific test scenarios like "SUPER SIX" and "BET LIMIT" are implemented with dedicated functions to handle unique behaviors.
• Reporting of test results is implemented within the playMulti function using a reporting mechanism (reportSheet) to log test outcomes and failures.

Note: This readme provides a high-level overview of the pytest automation script. For detailed implementation and usage instructions, refer to the comments within the script files (test.py and main.py) and the corresponding modules (src/modules.py and src/helpers.py).