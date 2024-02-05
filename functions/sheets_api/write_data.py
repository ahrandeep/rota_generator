from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from functions.sheets_api.sheets_api import creds, SPREADSHEET_ID
from classes.grid import Grid


COLOR_STYLES = {
    "black" : {
        "rgbColor": {
            "red": 0,
            "green": 0,
            "blue": 0,
            "alpha": 1
        }
    }
}

BORDER_STYLES = {
    "none" : {
        "style": "NONE",
        "colorStyle": COLOR_STYLES["black"]
    },
    "solid" : {
        "style": "SOLID",
        "colorStyle": COLOR_STYLES["black"]
    }
}

def write_data(grid: Grid) -> bool:

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
            newSheet = sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                         body=req).execute()
            sheetId = newSheet["replies"][0]["duplicateSheet"]["properties"]["sheetId"]
            print(f"New Sheet generated - '{sheetName}'")
        else:
            print(f"Sheet already exists - {sheetName}")
    except HttpError as err:
        print(err)
        return False
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
                              range=f"{sheetName}!A2:{chr(97 + len(grid.columns))}32",
                              valueInputOption="USER_ENTERED",
                              body=body).execute()
        print(f"Values updated for sheet - '{sheetName}'")

        # Format cells with borders
        # and remove data validation for months with less than 31 days
        if rowsToFormat:
            
            update = {
                "requests": [{
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 33,
                            "startColumnIndex": 0,
                            "endColumnIndex": 8
                        },
                        "top": BORDER_STYLES["none"],
                        "bottom": BORDER_STYLES["none"],
                        "left": BORDER_STYLES["none"],
                        "right": BORDER_STYLES["none"],
                        "innerHorizontal": BORDER_STYLES["none"],
                        "innerVertical": BORDER_STYLES["none"]
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": valueLen + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 8
                        },
                        "top": BORDER_STYLES["solid"],
                        "bottom": BORDER_STYLES["solid"],
                        "left": BORDER_STYLES["solid"],
                        "right": BORDER_STYLES["solid"],
                        "innerHorizontal": BORDER_STYLES["solid"],
                        "innerVertical": BORDER_STYLES["solid"]
                    },
                },
                {
                    "setDataValidation": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": valueLen + 1,
                            "endRowIndex": 32,
                            "startColumnIndex": 1,
                            "endColumnIndex": len(grid.columns) + 1
                        }
                    }
                }]
            }
            
            sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, 
                              body=update).execute()
            print(f"Format updated for sheet - '{sheetName}'")

        return True
    
    except HttpError as err:
        print(err)
        return False