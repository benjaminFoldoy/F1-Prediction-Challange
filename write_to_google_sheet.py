import re
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
from driver_standings import driver_standings, driver_standings_points
from constructor_standings import constructor_standings, constructor_standings_points
from knusprosent import update_values_sheet

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1OEUmbzJEi1aXiXAKrNsEsd2DrlDEt9RJamWSYHE3qL8'
SAMPLE_RANGE_NAME = '2023!A1:Z100'
TOKEN_PATH = "token_sheets_v4.pickle"

def main():
    global values_input, service, sheet
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Client_Secrets.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])
    
    
main()

#df=pd.DataFrame(values_input[1:], columns=values_input[0])

def has_numbers(inputstring):
    return any(char.isdigit() for char in inputstring)
    


def get_cell_crd(string, sheet = None):
    
    if sheet is None:
        sheet = values_input
    
    column_alpha = string
    row_num = ""
    while True:
        if has_numbers(column_alpha):
            row_num = column_alpha[-1] + row_num
            column_alpha = column_alpha[:-1]
        else:
            break
    return [int(ord(column_alpha)-65), int(row_num) - 1]

def get_cell_value(crd, sheet = None):
    
    if sheet is None:
        sheet = values_input
    
    try:
        return sheet[crd[1]][crd[0]]
    except:
        print(f"cell {crd} does not have a value")

def insert_into_cell(crd, value, sheet2d = None):
    if sheet2d is None:
        sheet2d = values_input
    
    crd = get_cell_crd(crd)
    
    while True: #if row does not exist, add rows until it does
        if len(sheet2d) <= crd[1]:
            sheet2d.append([])
        else:
            break
    
    while True: #if column of that row does not exist, add columns until it does
        if len(sheet2d[crd[1]]) <= crd[0]:
            sheet2d[crd[1]].append("")
        else:
            break
    sheet2d[crd[1]][crd[0]] = value

def update_sheet(sheet2d = None):
    if sheet2d is None:
        sheet2d = values_input
    
    sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
            range="2023!A1:Z100",
            valueInputOption='USER_ENTERED',
            body={'values': sheet2d}
        ).execute()

def update_driver_standings():
    ds = driver_standings()
    for i, driver in enumerate(ds):
        crd = "M"+str(5 + i)
        insert_into_cell(crd, driver)

def update_constructor_standings():
    cs = constructor_standings()
    for i, constructor in enumerate(cs):
        crd = "R"+str(5+i)
        insert_into_cell(crd, constructor)

def update_scoreboard():
    b = int(get_cell_value(get_cell_crd("P27"))) + int(get_cell_value(get_cell_crd("P28"))) + int(get_cell_value(get_cell_crd("P29")))
    k = int(get_cell_value(get_cell_crd("Q27"))) + int(get_cell_value(get_cell_crd("Q28"))) + int(get_cell_value(get_cell_crd("Q29")))
    insert_into_cell("P30", b, values_input)
    insert_into_cell("Q30", k, values_input)

def update_everything():
    update_driver_standings()
    update_constructor_standings()
    driver_standings_points(values_input)
    constructor_standings_points(values_input)
    update_values_sheet(values_input)
    update_scoreboard()
    update_sheet()


if __name__ == "__main__":
    update_everything()