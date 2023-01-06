# Additional dependencies:

# Source guide for dependencies and var setup:
# https://www.youtube.com/watch?v=lPTKUiafTRY

# pprint used to better render list data in terminal
# from pprint import pprint
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
# wk52_tue_sheet = SHEET.worksheet("27-12-22")
# wk52_wed_sheet = SHEET.worksheet("28-12-22")
# wk52_thu_sheet = SHEET.worksheet("29-12-22")
# item_reference_sheet = SHEET.worksheet("item-reference")

# vars containing the data of the specified sheet in list format
# wk52_tue_data = wk52_tue_sheet.get_all_values()
# wk52_wed_data = wk52_wed_sheet.get_all_values()
# wk52_thu_data = wk52_thu_sheet.get_all_values()
# item_reference_data = item_reference_sheet.get_all_values()

# print to test API function
# print(wk52_tue_data)
# print(wk52_wed_data)
# print(wk52_thu_data)
# print(item_reference_data)


def capture_date_input():
    """
    This function takes user input for the current date as a string.
    The output is passed as an argument to the function to get the
    current day's worksheet
    """
    captured_date = input(
        "Please input today's date in the format DD-MM-YY:\n")
    return captured_date


capt_date = capture_date_input()
# print(capt_date)


def get_current_worksheet(date):
    """
    This function takes the captured date as an argument to select the
    appropriate worksheet
    """
    current_worksheet = SHEET.worksheet(date)
    # pprint(current_worksheet.get_all_values())
    return current_worksheet


cur_wksh = get_current_worksheet(capt_date)
# print(cur_wksh)


def get_stock_required():
    """
    Using the current worksheet var, this function returns a list of
    numbers which represent the stock required for the current day.
    """
    # Get the values of the stock on hand column from the worksheet
    on_hand_col = cur_wksh.col_values(2)
    # Use a list slice to remove the heading, leaving numbers
    # https://www.geeksforgeeks.org/python-list-slicing/
    on_hand_nums = on_hand_col[1::]
    # Use list comprehension to convert the list to ints
    # https://www.geeksforgeeks.org/
    # python-converting-all-strings-in-list-to-integers/
    # (Multi-line hyperlink)
    on_hand_ints = [int(n) for n in on_hand_nums]
    return on_hand_ints


print(get_stock_required())
