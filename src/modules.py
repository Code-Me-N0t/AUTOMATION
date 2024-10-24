import datetime, requests, random, pytest, yaml, re, os, os.path, operator, base64, warnings, shutil, json, sys, logging, functools, time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException, StaleElementReferenceException, MoveTargetOutOfBoundsException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from google_auth_oauthlib.flow import InstalledAppFlow
from selenium.webdriver.chrome.options import Options
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from selenium.webdriver.common.keys import Keys
from googleapiclient.errors import HttpError
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build
from google.oauth2 import service_account
from fake_useragent import UserAgent
from colorama import Fore, init
from selenium import webdriver
from datetime import date
from io import BytesIO
from time import sleep
from PIL import Image

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors")

# logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

init(autoreset=True)
userAgent = UserAgent(platforms="mobile")

deviceName = os.environ['USERPROFILE'].split(os.path.sep)[-1]
# path = f'C:\\Users\\{deviceName}\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = path

def env(value): return os.environ.get(value)

def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try: return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception in {func.__name__}: {type(e).__name__}")
            return None
    return wrapper

def load_json(filename):
        with open(filename) as json_file:
            json_data = json_file.read()
            return json.loads(json_data)

def delete_files(directory):
    if os.path.exists(directory): shutil.rmtree(directory)
    else: pass

def create_files(directory):
    if os.path.exists(directory): pass
    else: os.makedirs(directory)

def locator(*keys):
    with open("resources/locator.yaml", "r") as loc:
        get_locator = yaml.load(loc, Loader=yaml.FullLoader)
        for key in keys: get_locator = get_locator[key]
        return get_locator
    
scenarios = load_json('resources/scenarios.json')
creds = load_json('resources/creds.json')
test_status = {key: [] for key in scenarios.keys()}
delete_files('screenshots/')
delete_files('decoded_images/')

def duplicate_sheet(service, spreadsheet_id, sheet_id, new_title):
    new_sheet = service.spreadsheets().sheets().copyTo(
        spreadsheetId=spreadsheet_id,
        sheetId=sheet_id,
        body={'destinationSpreadsheetId': spreadsheet_id}
    ).execute()
    
    new_sheet_id = new_sheet['sheetId']
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': [{
            'updateSheetProperties': {
                'properties': {'sheetId': new_sheet_id, 'title': new_title},
                'fields': 'title',
            }
        }]}
    ).execute()

    return new_title, new_sheet_id

def update_spreadsheet(value, rng):
    new_title = date.today().isoformat()
    SCOPES = [creds['SCOPES']]
    SPREADSHEET_ID = env("SPREADSHEET_ID")

    creds = None
    if os.path.exists("resources/token.json"):
        creds = Credentials.from_authorized_user_file("resources/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("resources/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("resources/token.json", "w") as token: 
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        existing_sheet_id = None
        for sheet in sheets:
            if sheet['properties']['title'] == new_title:
                existing_sheet_id = sheet['properties']['sheetId']
                break

        if existing_sheet_id:
            new_sheet_title = new_title
            new_sheet_id = existing_sheet_id
        else:
            for sheet in sheets:
                if sheet['properties']['title'] == 'FORMAT':
                    new_sheet_title, new_sheet_id = duplicate_sheet(
                        service, SPREADSHEET_ID, 
                        sheet['properties']['sheetId'], 
                        new_title
                    )
                    print(f"The name of the duplicated sheet is: {new_sheet_title}")
                    break

        if isinstance(value, list):
            non_empty_sublists = [
                sublist for sublist in value if sublist and all(
                    isinstance(elem, str) and elem.strip() for elem in sublist
                )
            ]
            cell_value = ', '.join(''.join(sublist) for sublist in non_empty_sublists)
            values = [[cell_value]]
        else:
            values = [[value]]

        body = {'values': values}
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{new_sheet_title}!{rng}",
            valueInputOption="RAW",
            body=body
        ).execute()

    except HttpError as err: print(err)

class Modules:
    def __init__(self, handler):
        self.handler = handler
    
    def execJS(self, function):
        with open('resources/script.js', 'r') as js:
            getScript = js.read()
        script = getScript + f'return {function}'
        run = self.handler.driver.execute_script(script)
        return run

    def displayToast(self, type, color, message):
        function_call = f"displayToast('{type}', '{color}', '{message}');"
        self.execJS(function_call)

    def click(self, element):
        location = element.location
        size = element.size
        x = location['x'] + size['width'] // 2
        y = location['y'] + size['height'] // 2
        actions = ActionChains(self.handler.driver)
        
        try:
            actions.move_to_element_with_offset(
                element, size['width'] // 2, size['height'] // 2
            ).perform()
        except MoveTargetOutOfBoundsException:
            actions.move_to_element(
                element
            ).perform()

        element.click()
        self.execJS(f'highlightClick({x}, {y});')
        return True
    
    def sendTG(self, tests):
        url = creds['tg_host']
        BOT_TOKEN = creds['tg_token']
        CHAT_ID = creds['tg_id']

        header = "TEST RESULTS:\n"
        test_details = "\n".join([f"{test['testname']}: {test['result']}" for test in tests])
        message = f"{header}\n{test_details}"
        
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }

        response = requests.post(f'{url}bot{BOT_TOKEN}/sendMessage', data=payload)

        if response.status_code == 200:
            print('Message Sent')
        else:
            print(f'Message Not Sent: {response.status_code}, {response.text}')
