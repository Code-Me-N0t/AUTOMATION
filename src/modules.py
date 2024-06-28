# gen imports
import datetime, requests, random, pytest, yaml, re, os, os.path, operator, base64, warnings, cv2, shutil, json, pytesseract, sys

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
import logging, functools

logging.basicConfig(level=logging.CRITICAL +1)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


init(autoreset=True)
userAgent = UserAgent(platforms="mobile")

deviceName = os.environ['USERPROFILE'].split(os.path.sep)[-1]
path = f'C:\\Users\\{deviceName}\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = path

def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try: return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception in {func.__name__}: {type(e).__name__}")
            return None
    return wrapper


def click_highlighter(driver, element):
    location = element.location
    size = element.size
    x = location['x'] + size['width'] // 2
    y = location['y'] + size['height'] // 2
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, 
                                        size['width'] // 2, 
                                        size['height'] // 2).perform()
    element.click()
    highlight_click(driver, x, y)

    return True

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
        for key in keys: get_locator = get_locator[key]
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

test_status = {key: [] for key in scenarios.keys()}

with open('creds.json') as json_file:
    json_data = json_file.read()
    creds = json.loads(json_data)

def displayToast(driver, type, color, message):
    script = f"""
    var link = document.createElement('link');
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
    link.rel = 'stylesheet';
    link.type = 'text/css';
    document.head.appendChild(link);

    if ('{color}' == 'green'){{ color = '#478547'; }} else{{ color = 'red'; }}
    
    var toast = document.createElement('div');
    toast.classList.add('toast');

    var textcap = document.createTextNode('{message}');

    var icon = document.createElement('i');
    icon.classList.add('fa', 'fa-{type}');
    icon.setAttribute('aria-hidden', 'true');
    icon.style.fontSize = '20px';
    icon.style.position = 'absolute';
    icon.style.left = '0';
    icon.style.marginLeft = '10px';
    icon.style.marginRight = '10px';
    icon.style.color = color;

    toast.appendChild(icon);
    toast.appendChild(textcap);

    document.body.appendChild(toast);

    toast.style.position = 'fixed';
    toast.style.top = '0px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%) translateY(-100%)';
    toast.style.backgroundColor = 'rgba(250, 250, 250)';
    toast.style.color = color;
    toast.style.padding = '10px 40px';
    toast.style.borderRadius = '3px';
    toast.style.borderLeft = `10px solid ${{color}}`;
    toast.style.zIndex = '9999';
    toast.style.fontWeight = 'bold';
    toast.style.fontFamily = 'Arial, sans-serif';
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.5s, transform 0.5s';
    toast.style.boxShadow = '0 4px 8px rgba(0, 0, 0, .5)';
    toast.style.textAlign = 'center';
    toast.style.alignItems = 'center';
    toast.style.display = 'flex';
    toast.style.minWidth = '250px'

    setTimeout(function() {{
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(-50%) translateY(20px)';
    }}, 10);

    setTimeout(function() {{
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(-100%)';
        toast.addEventListener('transitionend', function() {{
            toast.remove();
        }});
    }}, 2000);
    """
    driver.execute_script(script)

def highlight_click(driver, x, y):
    script = f"""
        var clickIndicator = document.createElement('div');
        clickIndicator.style.position = 'absolute';
        clickIndicator.style.top = '{y}px';
        clickIndicator.style.left = '{x}px';
        clickIndicator.style.width = '20px';
        clickIndicator.style.height = '20px';
        clickIndicator.style.backgroundColor = '#39FF14';
        clickIndicator.style.borderRadius = '50%';
        clickIndicator.style.zIndex = '9999';
        clickIndicator.style.opacity = '0.8';
        clickIndicator.style.pointerEvents = 'none';
        clickIndicator.style.transition = 'opacity 0.5s ease-out';
        document.body.appendChild(clickIndicator);
        setTimeout(function() {{
            clickIndicator.style.opacity = '0';
            setTimeout(function() {{
                document.body.removeChild(clickIndicator);
            }}, 500);
        }}, 500);
    """
    driver.execute_script(script)

def duplicate_sheet(service, spreadsheet_id, sheet_id, new_title):
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

def env(value): return os.environ.get(value)