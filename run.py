# Additional dependencies:

# Source guide for dependencies and var setup:
# https://www.youtube.com/watch?v=lPTKUiafTRY

# gspread and google-auth installed via pip3 install command
# gspread library used for google sheets integration
import gspread
# Only Credentials class imported from google-auth for authorization
from google.oauth2.service_account import Credentials

# Set scope for Google IAM authentication for the APIs the program has
# access to.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# const to hold the untracked credentials file
CREDS = Credentials.from_service_account_file("creds.json")
# const to give scopes to the credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# const to authorize the gspread client with these scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# const to hold the full spreadsheet
SHEET = GSPREAD_CLIENT.open("lidl_bake_wk_52")

# vars to reference the individual worksheets of the full spreadsheet
wk52_tue_sheet = SHEET.worksheet("tue-27-12-22")
wk52_wed_sheet = SHEET.worksheet("wed-28-12-22")
wk52_thu_sheet = SHEET.worksheet("thu-29-12-22")
item_reference_sheet = SHEET.worksheet("item-reference")

# vars containing the data of the specified sheet in list format
wk52_tue_data = wk52_tue_sheet.get_all_values()
wk52_wed_data = wk52_wed_sheet.get_all_values()
wk52_thu_data = wk52_thu_sheet.get_all_values()
item_reference_data = item_reference_sheet.get_all_values()

# print to test API function
print(wk52_tue_data)
print(wk52_wed_data)
print(wk52_thu_data)
print(item_reference_data)
