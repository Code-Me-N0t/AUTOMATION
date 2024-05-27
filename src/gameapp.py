from src.modules import *
from src.main import *
import datetime

host = env('host')

def get_token(index=84, balance=None):
    header = {
        env('op_name'): env('op_value'),
        env('t_name'): env('t_value'),
    }

    response = requests.get(f'{host}token', headers=header)
    token = response.json()['data']['token']
    header[env('token')] = token

    if balance is not None:
        key_params = {'username': data['username']}
        response = requests.get(host + env('balance'), headers=header, json=key_params)
        current_balance = response.json()['data']['balance']
        
        x = datetime.datetime.now()
        formatted_x = x.strftime("%Y-%m-%d_T%H-%M-%S")

        skip = False

        current_balance = float(current_balance)
        balance = float(balance)

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
            response = requests.post(host + env('balance'), headers=header, json=key_params)
            updated_balance = response.json()['data']['balance']
        print(f'{Fore.GREEN}Balance: {updated_balance}')

    key_params = {'username': data['username'], 'betlimit': str(index)}
    response = requests.get(host + env('game_key'), headers=header, json=key_params)
    game_key = response.json()['data']['key']

    query_params = {'key': game_key}
    response = requests.get(host + env('site_url'), headers=header, params=query_params)
    game_url = response.json()['data']['url']
    return game_url
