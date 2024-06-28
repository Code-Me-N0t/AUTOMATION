from src.modules import *

host = creds['host']
header = {
    creds['op_name']: creds['op_value'],
    creds['t_name']: creds['t_value'],
}

def get_token():
    response = requests.get(f'{host}token', headers=header)
    token = response.json()['data']['token']
    header[creds['token']] = token

    return token

def get_gameurl(index=84):
    _ = get_token()
    key_params = {'username': creds['username'], 'betlimit': str(index)}
    response = requests.get(host + creds['game_key'], headers=header, json=key_params)
    game_key = response.json()['data']['key']

    query_params = {'key': game_key}
    response = requests.get(host + creds['site_url'], headers=header, params=query_params)
    game_url = response.json()['data']['url']
    
    return game_url