from src.modules import *
from src.main import data

host = 'http://161.117.248.87:9003/api/v2/mars/'

def get_token():
    header = {
        env('OP_NAME'): env('OP_VALUE'),
        'X-key': 'test123',
    }

    response = requests.get(f'{host}token', headers=header)
    token = response.json()['data']['token']
    header[env('TOKEN')] = token

    key_params = {'username': f'{data["username"]}','betlimit': data["bet limit"]}
    response = requests.get(host+'game-providers/30/games/ogplus/key', headers=header, json=key_params)
    game_key = response.json()['data']['key']

    query_params = {'key': game_key}
    response = requests.get(host+'game-providers/30/play', headers=header, params=query_params)
    return response.json()['data']['url']