from src.modules import *
from src.main import *
import datetime

host = creds['host']

def get_token(index, balance):
    header = {
        creds['op_name']: creds['op_value'],
        creds['t_name']: creds['t_value'],
    }

    response = requests.get(f'{host}token', headers=header)
    token = response.json()['data']['token']
    header[creds['token']] = token

    key_params = {'username': data['username']}
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
        if balance < 2000 and current_balance > 2000: #249.65
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
            'username': data['username'],
            'balance': adjustment,
            'action': action,
            'transferId': formatted_x
        }
        response = requests.post(host + creds['balance'], headers=header, json=key_params)
        updated_balance = response.json()['data']['balance']
    print(f'{Fore.GREEN}Balance: {updated_balance}')

    key_params = {'username': data['username'], 'betlimit': str(index)}
    response = requests.get(host + creds['game_key'], headers=header, json=key_params)
    game_key = response.json()['data']['key']

    query_params = {'key': game_key}
    response = requests.get(host + creds['site_url'], headers=header, params=query_params)
    game_url = response.json()['data']['url']
    return game_url
