# gen imports
import datetime, requests, random, pytest, yaml, re, os, os.path, operator, base64, warnings, cv2, shutil, json, pytesseract

# selenium
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

# google
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account

# misc
from fake_useragent import UserAgent
from datetime import date
from colorama import Fore, init
from time import sleep
from io import BytesIO
from PIL import Image

init(autoreset=True)
userAgent = UserAgent(platforms="mobile")

deviceName = os.environ['USERPROFILE'].split(os.path.sep)[-1]
path = f'C:\\Users\\{deviceName}\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = path

def delete_files(directory):
    if os.path.exists(directory): shutil.rmtree(directory)
    else: pass

def create_files(directory):
    if os.path.exists(directory): pass
    else: os.makedirs(directory)
        
delete_files('screenshots/')
delete_files('decoded_images/')

def locator(*keys):
    with open("resources/locator.yaml", "r") as loc:
        get_locator = yaml.load(loc, Loader=yaml.FullLoader)
        for key in keys:
            get_locator = get_locator[key]
        
        return get_locator
    
def execJS(driver, function=None):
    with open(f'resources/script.js','r') as js:
        getScript = js.read()
        script = getScript + f'return {function}'
        run = driver.execute_script(script)
        return run

with open('scenarios.json') as json_file:
    json_data = json_file.read()
    scenarios = json.loads(json_data)

with open('creds.json') as json_file:
    json_data = json_file.read()
    creds = json.loads(json_data)

def displayToast(driver, message):
    script = f"""
    var toast = document.createElement('div');
    toast.classList.add('toast');
    toast.textContent = '{message}';
    document.body.appendChild(toast);

    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%)';
    toast.style.backgroundColor = 'rgba(255, 255, 255, 0.6)';
    toast.style.color = '#008000';
    toast.style.padding = '10px';
    toast.style.borderRadius = '5px';
    toast.style.zIndex = '9999';
    toast.style.fontWeight = 'bold';
    toast.style.fontFamily = 'Arial, sans-serif';

    setTimeout(function() {{
        toast.remove();
    }}, 3000);
    """
    driver.execute_script(script)

def duplicate_sheet(service, spreadsheet_id, sheet_id, new_title):
    # Duplicate the sheet
    new_sheet = service.spreadsheets().sheets().copyTo(
        spreadsheetId=spreadsheet_id,
        sheetId=sheet_id,
        body={'destinationSpreadsheetId': spreadsheet_id}
    ).execute()
    
    # Get the new sheet ID
    new_sheet_id = new_sheet['sheetId']
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'requests': [{
                'updateSheetProperties': {
                    'properties': {'sheetId': new_sheet_id, 'title': new_title},
                    'fields': 'title',
                }
            }]
        }
    ).execute()

    return new_title, new_sheet_id

def update_spreadsheet(value, rng):
    new_title = date.today().isoformat()
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # The ID of the spreadsheet.
    SPREADSHEET_ID = env("SPREADSHEET_ID")

    creds = None
    if os.path.exists("resources/token.json"):
        creds = Credentials.from_authorized_user_file("resources/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("resources/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("resources/token.json", "w") as token: token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        # Check if the new title already exists
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        existing_sheet_id = None
        for sheet in sheets:
            if sheet['properties']['title'] == new_title:
                existing_sheet_id = sheet['properties']['sheetId']
                break
        if existing_sheet_id:
            # Update existing sheet
            new_sheet_title = new_title
            new_sheet_id = existing_sheet_id
        else:
            # Duplicate Sheet1
            for sheet in sheets:
                if sheet['properties']['title'] == 'FORMAT':
                    new_sheet_title, new_sheet_id = duplicate_sheet(service, SPREADSHEET_ID, sheet['properties']['sheetId'], new_title)
                    print(f"The name of the duplicated sheet is: {new_sheet_title}")
                    break
        # Update value in the sheet (existing or duplicated)
        if isinstance(value, list):
            # Filter out empty sublists and empty strings
            non_empty_sublists = [sublist for sublist in value if sublist and all(isinstance(elem, str) and elem.strip() for elem in sublist)]
            
            # Join non-empty strings from non-empty sublists into a single string
            cell_value = ', '.join(''.join(sublist) for sublist in non_empty_sublists)
            
            # Update values with a list containing a single string
            values = [[cell_value]]

        else:
            # If value is not a list, update values with a list containing a single value
            values = [[value]]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{new_sheet_title}!{rng}",  
            valueInputOption="RAW",
            body=body
        ).execute()
        # print(f"{result.get('updatedCells')} cell updated on the sheet.")

    except HttpError as err: print(err)


def env(value):
    return os.environ.get(value)