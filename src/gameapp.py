from src.modules import *
from src.main import data

host = env("host")

def get_token():
    header = {
        env('OP_NAME'): env('OP_VALUE'),
        env('T_NAME'): env('T_VALUE'),
    }

    response = requests.get(f'{host}token', headers=header)
    token = response.json()['data']['token']
    header[env('TOKEN')] = token

    username = {'username': f'{data["Username"]}'}
    response = requests.get(host+env('GAME_KEY'), headers=header, json=username)
    game_key = response.json()['data']['key']

    query_params = {'key': game_key}
    response = requests.get(host+env('SITE_URL'), headers=header, params=query_params)
    return response.json()['data']['url']















# def get_token1():
#     header = {
#         env("OP_NAME"): env("OP_VALUE"),
#         env("T_NAME"): env("T_VALUE")
#     }
    
#     # Get Token
#     response = requests.get(f"{game_url}/token", headers=header)
#     token = response.json()['data']['token']
#     header[f'{env("TOKEN")}'] = token

#     # Get Game Key
#     username = {'username': f'{data["Username3"]}'}
#     response = requests.get(game_url+env("GAME_KEY"), headers=header, json=username)
#     game_key = response.json()['data']['key']

#     # Get URL
#     query_params = {'key': game_key}
#     response = requests.get(game_url+env("SITE_URL"), headers=header, params=query_params)
#     return response.json()['data']['url']

# def get_token2():
#     header = {
#         env("OP_NAME"): env("OP_VALUE"),
#         env("T_NAME"): env("T_VALUE")
#     }
    
#     # Get Token
#     response = requests.get(f"{game_url}/token", headers=header)
#     token = response.json()['data']['token']
#     header[f'{env("TOKEN")}'] = token

#     # Get Game Key
#     username = {'username': f'{data["Username2"]}'}
#     response = requests.get(game_url+env("GAME_KEY"), headers=header, json=username)
#     game_key = response.json()['data']['key']

#     # Get URL
#     query_params = {'key': game_key}
#     response = requests.get(game_url+env("SITE_URL"), headers=header, params=query_params)
#     return response.json()['data']['url']