# Additional dependencies:

# Source guide for dependencies and var setup:
# https://www.youtube.com/watch?v=lPTKUiafTRY

# pprint used to better render list data in terminal
from pprint import pprint
# DictReader is used to construct data structures from csv files
# from csv import DictReader
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
item_reference_sheet = SHEET.worksheet("item-reference")

# vars containing the data of the specified sheet in list format
# wk52_tue_data = wk52_tue_sheet.get_all_values()
# wk52_wed_data = wk52_wed_sheet.get_all_values()
# wk52_thu_data = wk52_thu_sheet.get_all_values()
item_reference_data = item_reference_sheet.get_all_values()
item_reference_dict = item_reference_sheet.get_all_records()

# print to test API function
# print(wk52_tue_data)
# print(wk52_wed_data)
# print(wk52_thu_data)
# pprint(item_reference_data)
# pprint(item_reference_dict)


def capture_date_input():
    """
    This function takes user input for the current date as a string.
    The output is passed as an argument to the function to get the
    current day's worksheet.
    """
    captured_date = input(
        "Please input today's date in the format DD-MM-YY:\n")
    return captured_date


def get_current_worksheet(date):
    """
    This function takes the captured date as an argument to select the
    appropriate worksheet.
    """
    current_worksheet = SHEET.worksheet(date)
    # pprint(current_worksheet.get_all_values())
    return current_worksheet


def get_stock_required(worksheet):
    """
    Using the current worksheet var, this function returns a list of
    numbers which represent the stock required for the current day.

    Parameter added for worksheet for scope compatibility from main
    function.
    """
    # Get the values of the stock on hand column from the worksheet
    on_hand_col = worksheet.col_values(2)
    # Use a list slice to remove the heading, leaving numbers
    # https://www.geeksforgeeks.org/python-list-slicing/
    on_hand_nums = on_hand_col[1::]
    # Use list comprehension to convert the list to ints
    # https://www.geeksforgeeks.org/
    # python-converting-all-strings-in-list-to-integers/
    # (Multi-line hyperlink)
    on_hand_ints = [int(n) for n in on_hand_nums]
    return on_hand_ints


def separate_items_by_program():
    """
    This function is designed to create separate subset lists for each
    different bakery program. This allows for user input to be broken
    down by category when entering stock on hand levels.
    """
    # Add global keyword access at the top of the function so the vars
    # can be accessed from other functions
    global DEFROSTS, APPLE_TURNOVERS, ROLLS_BAGUETTES, DANISH, CHEESE_ROLLS
    global PASTRIES
    # Get the item names from reference sheet
    items = item_reference_sheet.col_values(1)
    # print(items)
    # Get the corresponding bakery program number
    programs = item_reference_sheet.col_values(3)
    # print(programs)
    # Create a dictionary with zip method to create key: value pairs
    items_by_prog = dict(zip(items, programs))
    # pprint(items_by_prog)
    # List comprehensions of keys with program number conditional
    # https://stackoverflow.com/questions/44664247/
    # python-dictionary-how-to-get-all-keys-with-specific-values
    # (Multi-line hyperlink)
    DEFROSTS = [k for k, v in items_by_prog.items() if v == '0']
    # pprint(f"Defrost program items are: {DEFROSTS}")
    APPLE_TURNOVERS = [k for k, v in items_by_prog.items() if v == '1']
    # pprint(f"Apple turnover program items are: {APPLE_TURNOVERS}")
    ROLLS_BAGUETTES = [k for k, v in items_by_prog.items() if v == '2']
    # pprint(f"Rolls/baguettes program items are: {ROLLS_BAGUETTES}")
    DANISH = [k for k, v in items_by_prog.items() if v == '3']
    # pprint(f"Danish program items are: {DANISH}")
    CHEESE_ROLLS = [k for k, v in items_by_prog.items() if v == '4']
    # pprint(f"Cheese rolls program items are: {CHEESE_ROLLS}")
    PASTRIES = [k for k, v in items_by_prog.items() if v == '5']
    # pprint(f"Pastry program items are: {PASTRIES}")


def get_stock_on_hand(program_items, program_name):
    """
    This is the function that take user input for the stock on hand.
    Taking the program var as a parameter, it will loop through each
    item in the given program and request the current quantity for the
    user to enter.

    The program name is provided as a string argument when called to
    present the final values entered for the program clearly to the
    user.
    """
    input_list = []
    # Loop through each item in the given program and take input for the
    # current number of items still on sale
    for item in program_items:
        print(f"Please input stock on hand for {item}:")
        input_str = input("Current stock:")
        print(f"You entered {input_str} units for {item}")
        input_list.append(input_str)

    # Outside of the loop, show the final list of entered values for the
    # given program
    print(f"Stock values provided for {program_name} were: {input_list}")
    # Return the input list so that a full list for stock from all
    # programs may be constructed
    return input_list


def main():
    """
    This function calls the other functions in sequence as appropriate
    for program function.
    """
    # capt_date = (capture_date_input())
    # print(type(capt_date))

    # curr_worksheet = get_current_worksheet(capt_date)
    # print(curr_worksheet)

    # stock_req = get_stock_required(curr_worksheet)
    # print(stock_req)

    separate_items_by_program()
    # print(DEFROSTS)
    # print(APPLE_TURNOVERS)
    # print(ROLLS_BAGUETTES)
    # print(DANISH)
    # print(CHEESE_ROLLS)
    # print(PASTRIES)

    # Create vars to hold the return values of the get stock on hand
    # function, depending on which program arguments are provided
    prog0_on_hand = get_stock_on_hand(DEFROSTS, 'defrosts')
    prog1_on_hand = get_stock_on_hand(APPLE_TURNOVERS, 'apple_turnovers')

    print(prog0_on_hand)
    print(prog1_on_hand)


main()
