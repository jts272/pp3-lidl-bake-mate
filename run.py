# Additional dependencies:

# Source guide for dependencies and var setup:
# https://www.youtube.com/watch?v=lPTKUiafTRY

# pprint used to better render list/dict data in terminal
from pprint import pprint
# gspread, google-auth and numpy installed via pip3 install command
# gspread library used for google sheets integration
import gspread
# Only the Credentials class imported from google-auth for authorization
from google.oauth2.service_account import Credentials
# numpy is used for its list concatenating method
import numpy as np


# Set scope for Google IAM authentication for the APIs the program has
# access to.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# const to hold the untracked credentials file
CREDS = Credentials.from_service_account_file("creds.json")
# const to give scope to the credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# const to authorize the gspread client with these scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# const to hold the full spreadsheet
SHEET = GSPREAD_CLIENT.open("lidl_bake_wk_52-2022")

# const to reference the sheet containing all bakery item properties
ITEM_REFERENCE_SHEET = SHEET.worksheet("item-reference")
# const to get the list of items names. gspread returns a list of list
# items so numpy is used to flatten the list for future use
ITEM_ALL_NAMES = list(np.concatenate(ITEM_REFERENCE_SHEET.get(("A2:A37"))))

# const to reference the most recent worksheet by index
LATEST_SHEET_REF = SHEET.get_worksheet(-1)
# const to reference the title of the most recent sheet
LATEST_SHEET_TITLE = LATEST_SHEET_REF.title


def get_worksheet_from_input():
    """
    This function asks the user to input the date. This input is
    returned from the function and used as an argument so the rest of
    the program knows which worksheet to address.

    Checks are performed for the presence and value of the input to
    guide the user to selecting the necessary sheet for the day.
    """
    # Begin loop that is looking for a date that is contained in the
    # base spreadsheet
    while True:
        try:
            # This input is asking the user to input the date for the
            # sheet they wish to access. This matches up with the title
            # of the worksheet from the base spreadsheet
            user_date = input(
                "Please enter the date as DD-MM-YY to select your bake plan:\n"
            )
            # var to reference the worksheet named by user's input
            worksheet = SHEET.worksheet(user_date)
            # var to access the actual title of the
            worksheet_title = worksheet.title
            # If the input is valid, but not the latest sheet to be
            # completed, inform the user and repeat the input operation
            if worksheet_title != LATEST_SHEET_TITLE:
                print(f"The plan for {worksheet_title} is already complete!")
                print(f"Please enter {LATEST_SHEET_TITLE} to continue\n")
                continue
            # Loop is broken if the user provides a date that matches
            # with the correct worksheet for the day
            break
        except gspread.exceptions.WorksheetNotFound:
            # Using gspread's built in exception, the user is informed
            # that this sheet is unavailable if it is not found in the
            # base spreadsheet
            print(f"No plan was found for '{user_date}'")
            # The user is informed of the title of the most recent sheet
            # from the base spreadsheet to guide their next input
            print(
                f"The most recent plan available is for {LATEST_SHEET_TITLE}")
            print(f"Please enter {LATEST_SHEET_TITLE} to continue\n")
            # continue statment returns to the top of the loop so the
            # user can try again with their date input
            continue

    # Confirm to the user that their input selected the correct sheet
    # and that stock level entry will be required next
    print("Bake plan is available")
    print(f"Accessing bake plan for {worksheet_title}...\n")
    print("Please enter current stock levels for the following lines:\n")
    # Outside of the loop, the function returns the input string so that
    # it may be passed into other functions as an argument
    return worksheet


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
    items = ITEM_REFERENCE_SHEET.col_values(1)
    # print(items)
    # Get the corresponding bakery program number
    programs = ITEM_REFERENCE_SHEET.col_values(3)
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
    while True:
        # Loop through each item in the given program and take input for
        # the current number of items still on sale
        for item in program_items:
            # Credit to this blog for error handling structure on input:
            # https://bobbyhadz.com/blog/python-while-loop-user-input
            # Create a while loop so that the current iteration of the
            # parent for loop will run until input is valid
            while True:
                # The try block executes and looks to catch errors from
                # the user's input if it is not an int value
                try:
                    print(f"Item group: {program_name}\n")
                    print(f"Please input stock on hand for {item}:\n")
                    # This var specifies that the user's input must be
                    # of int type, which works with the following except
                    # statement
                    input_str = int((input("Current stock:")))
                # The except block runs when the user does not enter an
                # int
                except ValueError:
                    # This message displays when the exception is caught
                    # and notifies the user of the correct type of input
                    # needed
                    print(
                        "Please enter a number of 0 or higher when recording "
                        "stock\n"
                    )
                    # continue kw used to repeat the while loop so the
                    # user can try a different value for the current
                    # item's stock level
                    continue
                # The following if else statments work when the user
                # provides an int, then checks that it was in the valid
                # range of 0 or above
                if input_str >= 0:
                    # The user's input is confirmed
                    print(f"You entered {input_str} units for {item}\n")
                    # The input is an int and is in range so is appened
                    # to the list returned by the function
                    input_list.append(input_str)
                    # The while loop can now be broken and the for loop
                    # proceeds to get input for the next item
                    break
                else:
                    # The user is confirmed their int input and shown
                    # that negative numbers are not accepted
                    print(
                        f"You entered {input_str}. Number must be 0 or greater"
                        "\n"
                    )

        # Create dict from program items and the input list to present
        # to the user
        input_prog_summary = dict(zip(program_items, input_list))
        # Show the final list of entered values for the given program
        print(f"Stock values provided for {program_name} were:\n")
        # sort_dicts arg required as pprint will display keys
        # alphabetically by default
        # See: https://stackoverflow.com/questions/4301069/
        # any-way-to-properly-pretty-print-ordereddict
        # (Multi-line hyperlink)
        pprint(input_prog_summary, sort_dicts=False)
        print()

        # Get input at the end of the loop for the user to confirm if
        # their list values are correct
        # See: https://bobbyhadz.com/blog/python-input-yes-no-loop
        user_input = input("Confirm values are correct? Please enter y or n\n")

        if user_input.lower() == 'y':
            print(f"Values submitted for {program_name}\n")
            # Exit loop when user confirms their values are correct
            break
        elif user_input.lower() == 'n':
            print(f"Re-enter values for {program_name}\n")
            # Clear the list on restart to keep correct number of values
            input_list.clear()
            continue
        else:
            # Catch-all statement similar to if the user selects 'n' so
            # that the user only submits data they are sure is correct
            print(
                f"Input not recognized - please re-enter values for "
                f"{program_name}\n")
            input_list.clear()
            continue

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


def worksheet_update_cols(worksheet, stock_list, col_name, cell_col_start):
    """
    This function updates the API worksheet.

    Arguments passed in are the worksheet to be updated and with which
    list. As the function is to be used for updating different cols, a
    param is included to pass in the name of the col being updated as a 
    string The worksheet cell to start updating the column from is also
    passed in as a string.

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
    print(
        f"Sending {col_name} values to worksheet for {LATEST_SHEET_TITLE}"
        f"...\n"
    )

    # This update method specifies the cell to start updating the col
    # from and the var containing the list of list values
    worksheet.update(cell_col_start, list_to_sheet)
    print(
        f"Values for {col_name} in worksheet for {LATEST_SHEET_TITLE} "
        f"updated!\n")


def calculate_items_to_bake(stock_required, stock_on_hand):
    """
    In this function, both the stock required and on hand for the day
    are passed in to produce the final list of stock required to be
    baked.

    The stock on hand is subtracted from the stock required list to give
    the user the figure required. Any instances of negative numbers will
    be amended to 0 as the function is returning a quantity of items for
    the baker to prepare.
    """
    # The following print statements report the values and lengths of
    # their respective lists
    # print(f"Stock required list values:\n {stock_required}\n")
    # print(f"{len(stock_required)} items")
    # print(f"Stock on hand list values:\n {stock_on_hand}\n")
    # print(f"{len(stock_on_hand)} items")

    # This var will receive the sum of the two lists, after negative
    # ints have been set to 0
    stock_to_bake = []
    # vars are iterated through the zipped lists passed in as arguments
    for required, on_hand in zip(stock_required, stock_on_hand):
        # List var to hold each value after arithmetic operation
        calculation = [(required - on_hand)]
        # print(calculation)
        # Address each item in the calculation list and adjust any ints
        # that are less than 0 to 0
        # See: https://martinheinz.dev/blog/80
        for i in calculation:
            if i < 0:
                i = 0
            # Append to placeholder list only after conditional logic
            stock_to_bake.append(i)

    # print(f"Required stock to bake: {stock_to_bake}\n")
    # print(f"{len(stock_to_bake)} items")

    return stock_to_bake


def present_bake_requirements(list_for_baker):
    """
    This function is designed to present to the user the final list of
    items to prepare in the bakery in the terminal, using the final
    calculated stock list.
    """
    # Create the zipped dict from item names and list arg
    to_bake_dict = dict(zip(ITEM_ALL_NAMES, list_for_baker))

    # This dict comprehension adds key: value pairs to the final list
    # on the condition that they are not asking for 0 items to be baked
    # See example 4 in the link below:
    # https://www.programiz.com/python-programming/
    # dictionary-comprehension
    # (Multi-line hyperlink)
    final_bake_dict = {k: v for (k, v) in to_bake_dict.items() if v != 0}
    print("Full list of items required for baking:\n")
    # Pretty-print the dict for legibility in the terminal
    pprint(final_bake_dict, sort_dicts=False)
    print()
    print("Thank you for using Lidl BakeMate! End of program.\n")


def main():
    """
    This function calls the other functions in sequence as appropriate
    for program function.
    """
    # This var holds the return of the user's date input so the
    # appropriate worksheet can be used for the program
    curr_worksheet = get_worksheet_from_input()

    # var to get the required stock from the user selected worksheet
    stock_req = get_stock_required(curr_worksheet)

    # Calls the function to break down the full list of bakery items
    # by program type
    separate_items_by_program()

    # Create vars to hold the return values of the get stock on hand
    # function, depending on which program arguments are provided
    # prog0_on_hand = get_stock_on_hand(DEFROSTS, 'Defrosts')
    prog1_on_hand = get_stock_on_hand(APPLE_TURNOVERS, 'Apple Turnovers')
    # prog2_on_hand = get_stock_on_hand(ROLLS_BAGUETTES, 'Rolls/Baguettes')
    # prog3_on_hand = get_stock_on_hand(DANISH, 'Danish')
    # prog4_on_hand = get_stock_on_hand(CHEESE_ROLLS, 'Cheese Rolls')
    # prog5_on_hand = get_stock_on_hand(PASTRIES, 'Pastries')

    # Notify user that all stock has been entered
    print("Stock on hand input complete!\n")

    # Call the function to join the sub lists together, passing in the
    # vars created from each sub list input
    stock_on_hand_final = combine_program_lists(
        # prog0_on_hand,
        prog1_on_hand,
        # prog2_on_hand,
        # prog3_on_hand,
        # prog4_on_hand,
        # prog5_on_hand
    )

    # Create dict from full list of item names and the final input list
    full_input_summary = dict(zip(ITEM_ALL_NAMES, stock_on_hand_final))
    # Present the pprinted dict of completed item entries
    print("Complete list of stock on hand entered:\n")
    pprint(full_input_summary, sort_dicts=False)
    print()
    print(f"Number of lines counted: {len(stock_on_hand_final)}\n")

    # Update the worksheet stock on hand column
    worksheet_update_cols(
        curr_worksheet, stock_on_hand_final, "stock on hand", "C2")

    # var to store the actual number of items for the baker to prepare
    stock_to_bake = calculate_items_to_bake(stock_req, stock_on_hand_final)

    # Update the worksheet stock to bake column
    worksheet_update_cols(curr_worksheet, stock_to_bake, "stock to bake", "D2")

    # Notify user that all data has been processed and present the final
    # results
    print("Data entry complete!\n")
    present_bake_requirements(stock_to_bake)


main()
