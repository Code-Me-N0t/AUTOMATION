from src.modules import *

class GameAPI:
    def __init__(self):
        self.host = creds['host']
        self.header = {
            creds['op_name']: creds['op_value'],
            creds['t_name']: creds['t_value'],
        }
        self.token = None

    def update_header(self, key, value):
        self.header[key] = value

    def get_token(self):
        response = requests.get(
            f'{self.host}token', 
            headers=self.header
        )
        self.token = response.json()['data']['token']
        self.update_header(creds['token'], self.token)
        return self.token

    def fetch_game_key(self, index=84):
        key_params = {
            'username': creds['username'], 
            'betlimit': str(index)
        }
        response = requests.get(
            self.host + creds['game_key'], 
            headers=self.header, 
            json=key_params
        )
        game_key = response.json()['data']['key']
        return game_key

    def get_game_url(self, index=84):
        self.get_token()
        game_key = self.fetch_game_key(index)
        query_params = {'key': game_key}
        response = requests.get(
            self.host + creds['site_url'], 
            headers=self.header, 
            params=query_params
        )
        game_url = response.json()['data']['url']
        return game_url

    def get_current_balance(self):
        key_params = {'username': creds['username']}
        response = requests.get(
            self.host + creds['balance'], 
            headers=self.header, 
            json=key_params
        )
        current_balance = response.json()['data']['balance']
        return float(current_balance)

    def calculate_adjustment(self, current_balance, balance):
        skip = False
        action = ''
        adjustment = 0

        if balance == 1000000:
            if current_balance > balance:
                adjustment = current_balance
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
                adjustment = current_balance
                skip = True

        return adjustment, action, skip

    def update_balance(self, balance):
        self.get_token()
        current_balance = self.get_current_balance()

        adjustment, action, skip = self.calculate_adjustment(current_balance, balance)

        if not skip:
            x = datetime.datetime.now()
            formatted_x = x.strftime("%Y-%m-%d_T%H-%M-%S")
            key_params = {
                'username': creds['username'],
                'balance': adjustment,
                'action': action,
                'transferId': formatted_x
            }
            response = requests.post(
                self.host + creds['balance'], 
                headers=self.header, 
                json=key_params
            )
            updated_balance = response.json()['data']['balance']
        else:
            updated_balance = current_balance

        print(f'\n{Fore.LIGHTBLACK_EX}Balance: {updated_balance}')
        return updated_balance
