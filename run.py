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
wk52_thu_sheet = SHEET.worksheet("29-12-22")
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
        # Credit to this blog for error handling structure on input:
        # https://bobbyhadz.com/blog/python-while-loop-user-input
        # Create a while loop so that the current iteration of the
        # parent for loop will run until input is valid
        while True:
            # The try block executes and looks to catch errors from the
            # user's input if it is not an int value
            try:
                print(f"Please input stock on hand for {item}:\n")
                # This var specifies that the user's input must be of
                # int type, which works with the following except
                # statement
                input_str = int((input("Current stock:")))
            # The except block runs when the user does not enter an int
            except ValueError:
                # This message displays when the exception is caught and
                # notifies the user of the correct type of input needed
                print(
                    "Please enter a number of 0 or higher when recording stock"
                    "\n"
                )
                # continue kw used to repeat the while loop so the user
                # can try a different value for the current item's stock
                # level
                continue
            # The following if else statments work when the user
            # provides an int, then checks that it was in the valid
            # range of 0 or above
            if input_str >= 0:
                # The user's input is confirmed
                print(f"You entered {input_str} units for {item}\n")
                # The input is an int and is in range so is appened to
                # the list returned by the function
                input_list.append(input_str)
                # The while loop can now be broken and the for loop
                # proceeds to get input for the next item
                break
            else:
                # The user is confirmed their int input and shown that
                # negative numbers are not accepted
                print(
                    f"You entered {input_str}. Number must be 0 or greater\n"
                )

    # Outside of the loop, show the final list of entered values for the
    # given program
    print(f"Stock values provided for {program_name} were: {input_list}\n")
    # Return the input list so that a full list for stock from all
    # programs may be constructed
    return input_list


def combine_program_lists(*programs):
    """
    This function takes an arbitrary number of lists and joins them
    together. This will create the final stock on hand list that will be
    sent to the worksheet and will also be used for calculating the
    stock required to bake.
    """
    # Placeholder list that will be appended with each sub list
    final_list = []
    # Loop to address each program passed in at function call
    for program in programs:
        # Use extend method to place each sub list into on final list
        # See: https://www.w3schools.com/python/python_lists_join.asp
        final_list.extend(program)

    # print(final_list)
    return final_list


def worksheet_update_stock(worksheet, stock_list):
    """
    This function updates the API worksheet.

    Arguments passed in are the worksheet to be updated and with which
    list.

    The var for the worksheet is captured in the first function in which
    the user enters the date.

    The gspread update method requires the data to be inserted to be a
    list of lists. Any list passed to the function must be broken down
    such that each item in the list is a list item.
    """
    # List comprehension to convert the list passed into the function
    # into a list of lists
    # See: https://stackoverflow.com/questions/38604805/
    # convert-list-into-list-of-lists
    # (Multi-line hyperlink)
    list_to_sheet = [[i] for i in stock_list]
    print(f"Sending stock on hand values to worksheet dated {worksheet}")
    # This update method specifies the cell to start updating the col
    # from and the var containing the list of list values
    worksheet.update("C2", list_to_sheet)
    print(f"Stock on hand values for worksheet dated {worksheet} updated!")


def main():
    """
    This function calls the other functions in sequence as appropriate
    for program function.
    """
    capt_date = (capture_date_input())
    # print(type(capt_date))

    curr_worksheet = get_current_worksheet(capt_date)
    # print(curr_worksheet)

    stock_req = get_stock_required(curr_worksheet)
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
    prog2_on_hand = get_stock_on_hand(ROLLS_BAGUETTES, 'rolls/baguettes')
    prog3_on_hand = get_stock_on_hand(DANISH, 'danish')
    prog4_on_hand = get_stock_on_hand(CHEESE_ROLLS, 'cheese rolls')
    prog5_on_hand = get_stock_on_hand(PASTRIES, 'pastries')

    print("Input for all items by program:\n")
    print(f"defrosts: {prog0_on_hand} ({len(prog0_on_hand)} items)")
    print(f"apple turnovers: {prog1_on_hand} ({len(prog1_on_hand)} items)")
    print(f"rolls/baguettes: {prog2_on_hand} ({len(prog2_on_hand)} items)")
    print(f"danish: {prog3_on_hand} ({len(prog3_on_hand)} items)")
    print(f"cheese rolls: {prog4_on_hand} ({len(prog4_on_hand)} items)")
    print(f"pastries: {prog5_on_hand} ({len(prog5_on_hand)} items)\n")

    print("Stock on hand input complete!\n")

    # Call the function to join the sub lists together, passing in the
    # vars created from each sub list input
    stock_on_hand_final = combine_program_lists(
        prog0_on_hand,
        prog1_on_hand,
        prog2_on_hand,
        prog3_on_hand,
        prog4_on_hand,
        prog5_on_hand
    )

    print(f"Complete list of stock on hand:\n {stock_on_hand_final}")
    print(f"Number of items counted: {len(stock_on_hand_final)}")

    worksheet_update_stock(curr_worksheet, stock_on_hand_final)


# TEST_LIST = [1, 2, 3]

# TEST_LIST_OF_LISTS = [[i] for i in TEST_LIST]
# print(TEST_LIST_OF_LISTS)

# # worksheet_update_stock(wk52_thu_sheet, TEST_LIST)

main()

# wk52_thu_sheet.update('C2', TEST_LIST_OF_LISTS)
