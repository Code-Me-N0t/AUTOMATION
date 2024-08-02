from src.modules import *
from src.gameapp import *

"""
    This function, `update_balance`, adjusts the user's balance based on the current state and the target balance for an automation test.

    Parameters:
    - driver: The web driver instance used to interact with the web application.
    - balance: The target balance to set for the user.

    Functionality:
    1. Retrieves the user's current balance using an API call.
    2. Determines the necessary balance adjustment based on the target balance:
        - If the target balance is 1,000,000:
            - No adjustment is made if the current balance is already greater than 1,000,000.
            - Otherwise, the balance is set to 1,000,000.
        - If the target balance is less than 2,000:
            - If the current balance exceeds 2,000, it deducts the difference to match the target balance.
            - If the current balance is zero, it increases the balance to match the target balance.
            - Otherwise, no adjustment is made.
    3. Performs the balance adjustment via an API call if needed.
    4. Prints the updated balance and refreshes the web driver.

    Returns:
    - The current balance before any adjustment.
"""

def update_balance(driver, balance):
    _ = get_token()
    

    key_params = {'username': creds['username']}
    response = requests.get(host + creds['balance'], headers=header, json=key_params)
    current_balance = response.json()['data']['balance']

    x = datetime.datetime.now()
    formatted_x = x.strftime("%Y-%m-%d_T%H-%M-%S")

    skip = False

    current_balance = float(current_balance)
    balance = float(balance)
    if balance == 1000000:

        if current_balance > balance:
    
            updated_balance = current_balance
    
            skip = True
    
        else:
    
            adjustment = balance
    
            action = 'IN'
    
    elif balance < 2000:

        if balance < 2000 and current_balance > 2000:
    
            adjustment = current_balance - balance
    
            action = 'OUT'
    
        elif current_balance == 0:
    
            adjustment = balance
    
            action = 'IN'
    
        else: 
    
            updated_balance = current_balance
    
            skip = True
    
    if skip == False:

        key_params = {
            'username': creds['username'],
            'balance': adjustment,
            'action': action,
            'transferId': formatted_x
        }
        response = requests.post(host + creds['balance'], headers=header, json=key_params)
        updated_balance = response.json()['data']['balance']
    print(f'\n{Fore.LIGHTBLACK_EX}Balance: {updated_balance}')
    driver.refresh()


    return current_balance