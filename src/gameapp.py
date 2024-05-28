from src.modules import *
from src.main import *

host = creds['host']

def get_token(index=84):
    header = {
        creds['op_name']: creds['op_value'],
        creds['t_name']: creds['t_value'],
    }

    response = requests.get(f'{host}token', headers=header)
    token = response.json()['data']['token']
    header[creds['token']] = token

    key_params = {'username': data['username'], 'betlimit': str(index)}
    response = requests.get(host + creds['game_key'], headers=header, json=key_params)
    game_key = response.json()['data']['key']

    query_params = {'key': game_key}
    response = requests.get(host + creds['site_url'], headers=header, params=query_params)
    game_url = response.json()['data']['url']
    return game_url

def printname(name):
    print(name)
