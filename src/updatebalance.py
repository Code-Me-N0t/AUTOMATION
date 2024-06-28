from src.modules import *
from src.gameapp import *


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
    print(f'\n{Fore.GREEN}Balance: {updated_balance}')
    driver.refresh()

    return current_balance