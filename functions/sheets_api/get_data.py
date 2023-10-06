from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from functions.sheets_api.sheets_api import validate, SPREADSHEET_ID

DATA_RANGES = ['Generator!A1:K25', 'Generator Rules!B2:L10']

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