from src.modules import *
from src.main import data
game_url = env("GAME_URL")


def get_token():
    header = {
        env("OP_NAME"): env("OP_VALUE"),
        env("T_NAME"): env("T_VALUE")
    }
    
    # Get Token
    response = requests.get(f"{game_url}/token", headers=header)
    token = response.json()['data']['token']
    header[f'{env("TOKEN")}'] = token

    # Get Game Key
    username = {'username': f'{data["Username"]}'}
    response = requests.get(game_url+env("GAME_KEY"), headers=header, json=username)
    game_key = response.json()['data']['key']

    # Get URL
    query_params = {'key': game_key}
    response = requests.get(game_url+env("SITE_URL"), headers=header, params=query_params)
    return response.json()['data']['url']