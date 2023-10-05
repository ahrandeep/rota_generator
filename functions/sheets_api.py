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
        sheet = service.spreadsheets()
        sheetId = None

        sheetProps = sheet.get(spreadsheetId=SPREADSHEET_ID,
                        fields = ("sheets.properties.title,"
                                    "sheets.properties.sheetId")
                    ).execute()

        # checks sheet titles to see if sheet already exists
        sheetId = next((ele["properties"]["sheetId"] 
                            for ele
                            in sheetProps["sheets"]
                            if (ele["properties"]["title"] == sheetName)),
                            None)

        if sheetId is None:
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
            # Duplicates base rota sheet with name as new sheetName
            newSheet = sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=req).execute()
            sheetId = newSheet["replies"][0]["duplicateSheet"]["properties"]["sheetId"]
            print(f"New Sheet generated - '{sheetName}'")
        else:
            print(f"Sheet already exists - {sheetName}")
    except HttpError as err:
        print(err)
        return None
    try:
        # generate values for sheet input. Each row is a new list inside values
        # values = [
        #   [cell_data,...],
        #   ...
        # ]
        values = []
        rowsToFormat = False

        row_count = 0
        for count, date in enumerate(grid.dates):
            values.append([date.strftime("%m/%d/%Y")])
            if date.weekday() <= 4:
                for event in grid.events[row_count]:
                    code = event.assigned.code if event.assigned is not None else "None"
                    values[count].append(f'{code}')
                row_count += 1
        
        # Fill in values up to 31 days (removes any dates which aren't needed)
        valueLen = len(values)
        if valueLen < 31:
            rowsToFormat = True
            for i in range(valueLen, 31):
                values.append([""])
    
        body = {
            "values": values
        }
        
        sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                              range=f"{sheetName}!A2:G32",
                              valueInputOption="USER_ENTERED",
                              body=body).execute()
        print(f"Values updated for sheet - '{sheetName}'")

        # Format cells with borders
        # and remove data validation for months with less than 31 days
        if rowsToFormat:
            colorStyle = {
                "rgbColor": {
                    "red": 0,
                    "green": 0,
                    "blue": 0,
                    "alpha": 1
                }
            }
            noBorderStyle = {
                "style": "NONE",
                "colorStyle": colorStyle
            }
            solidBorderStyle = {
                "style": "SOLID",
                "colorStyle": colorStyle
            }
            update = {
                "requests": [{
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 33,
                            "startColumnIndex": 0,
                            "endColumnIndex": 9
                        },
                        "top": noBorderStyle,
                        "bottom": noBorderStyle,
                        "left": noBorderStyle,
                        "right": noBorderStyle,
                        "innerHorizontal": noBorderStyle,
                        "innerVertical": noBorderStyle
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": valueLen + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 9
                        },
                        "top": solidBorderStyle,
                        "bottom": solidBorderStyle,
                        "left": solidBorderStyle,
                        "right": solidBorderStyle,
                        "innerHorizontal": solidBorderStyle,
                        "innerVertical": solidBorderStyle
                    },
                },
                {
                    "setDataValidation": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": valueLen + 1,
                            "endRowIndex": 32,
                            "startColumnIndex": 1,
                            "endColumnIndex": 9
                        }
                    }
                }]
            }
            
            sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=update).execute()
            print(f"Format updated for sheet - '{sheetName}'")

    except HttpError as err:
        print(err)
        return None