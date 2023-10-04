from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from classes.grid import Grid

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
DATA_RANGES = ['Generator!A1:K25', 'Generator Rules!B2:L10']
with open('spreadsheet_id.txt', 'r') as id:
    SPREADSHEET_ID = id.read()

def validate() -> Credentials:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_data() -> list[object]:
    """Gets data from spreadsheet using google sheets api

    Uses SPREADSHEET_ID and DATA_RANGES literals to batch get the requested ranges

    Returns:
        A list of objects where 
            name property is range name and 
            values property is a list of values in range
    """
    creds = validate()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,
                                    ranges=DATA_RANGES).execute()
        values = result.get('valueRanges', [])
        
        return values
    except HttpError as err:
        print(err)
        return None
    
def write_data(grid: Grid) -> bool:

    creds = validate()

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheetName = grid.dates[0].strftime("Rota - %b %y")
        dup = {
            "sourceSheetId": 0,
            "insertSheetIndex": 1,
            "newSheetName": sheetName
        }
        req = {
            "requests": [{
                "duplicateSheet": dup,
            }]
        }
        sheet = service.spreadsheets()
        sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=req).execute()


    except HttpError as err:
        print(err)

    try:
        values = []

        row_count = 0
        for count, date in enumerate(grid.dates):
            values.append([date.strftime("%m/%d/%Y")])
            if date.weekday() <= 4:
                for event in grid.events[row_count]:
                    code = event.assigned.code if event.assigned is not None else "None"
                    values[count].append(f'{code}')
                row_count += 1

        body = {
            "values": values
        }

        sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                              range=f"{sheetName}!A2:G32",
                              valueInputOption="USER_ENTERED",
                              body=body).execute()
    
    except HttpError as err:
        print(err)
        return None