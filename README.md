# Lidl BakeMate Python Terminal Application

![Lidl Bakery Items]

Live link - [Heroku](https://pp3-lidl-bake-mate.herokuapp.com/)

Accompanying spreadsheet - [Google Sheets](https://docs.google.com/spreadsheets/d/1F5qGL73_mbY4tX07SAwo8x-ooswImLdlVWjapZWEyjg/edit#gid=1612631949)

---

## Overview

Lidl BakeMate is a data-driven Python progam with Google Sheets integration that
 aims to boost productivity in Lidl GB stores. The program requests input from
 the user which is used to perform calculations which increase efficiency in a
 daily task. Data is presented in an accessible format to the user in the
 terminal, as well as in the integrated worksheet. 

### Usage Scenario

Lidl prides itself on its in-store bakery offering. Goods are baked three times
 per day (twice on a Sunday), according to the bake plan for the day - which is
 unique to the store. Both morning bakes are produced as laid out on the plan.
 However, the third and final bake of the day works differently. Bakery
 co-ordinators jot down their current stock levels for each line at 14:00. From
 there, they will subtract their stock on hand from the final stock required
 column on their paper worksheet. After they have manually written down this
 sum, they will then proceed to bake the goods needed in the calculated
 quantities.

As efficiency is a cornerstone to Lidl's success, this program aims to increase
 productivity in this task. By guiding the user through the process and
 performing all arithmetic for them, this program produces the desired result
 with the minimum of effort and error.

Furthermore, this program would bolster Lidl's overall push for paperless
 working. The logic for this program is designed to work on the handheld
 terminal (ACD) which each store uses for data-driven processes.

### ACD

![ACD]

This handheld device is fundamental to store operation through a range of data-
driven processes. Input consists of:

- Numerical keypad
- Enter key (red)
- Clear key ('C')
- Up/down keys (to scroll through lists)
- Function keys (top row)
- Context prompts on touch screen (Yes, No, Back, etc.)

The hardware is taken into account in the program. Program input is simple,
 requiring input only from numbers or single letters. For example, instances
 in the program where the user inputs 'Y' then the Enter key on the keyboard
 simulate simply pressing the Enter key on the ACD.

### Google Sheets Integration

[Please refer to the program's accompanying spreadsheed](https://docs.google.com/spreadsheets/d/1F5qGL73_mbY4tX07SAwo8x-ooswImLdlVWjapZWEyjg/edit#gid=1612631949)

Bake plans are sent to each store by the internal Back Office system. The Google
 Sheet functions to replicate this database. In the deployed program, the sheet
 uses real-world figures from an actual Lidl store operating in the Newton-
Aycliffe region. Figures are from a three-day span in week 52, 2022. In 
real-world deployment, there would be ongoing communication between the database
 and program. However, this scenario has simulated as three day period of time
 as a proof-of-concept.

The sheet serves as a reference point for the program to use, much like how
 current in-store staff refer to their paper bakery plans. The sheet contains
 an item reference sheet and the bakery plan for the given day as its own
 worksheet.

![Item reference]

![28-12-22 plan]

It is important to note that the naming conventions in the worksheets are
 followed, as the API relies on worksheet data to function. This is reflected in
 elements such as worksheet title, cell formatting and insertion of the newest
 sheet last in the overall spreadsheet.

The item reference sheet contains data on each individual bakery line for the
 program to address. Data such as the item name and bakery program is integral
 to the program flow.

Each day's bake plan has its own worksheet for the program to reference. This
 allows it to provide the correct plan to perform calculations against the
 user's input.

The spreadsheet holds the data for past day's entries, as shown for dates 27 and
 28-12-22. In the program scenario, the user is inputting data to calculate
 the lines they need to bake on 29-12-22. After the user confirms their inputs
 are correct, the API updates this worksheet. On the next day of trade, the
 user would be working with data for 30-12-22 in a real-world deployment and the
 29-12-22 figures would be complete and serve as a past record.

---

## Planning

Inception of the program involved jotting down on paper the steps of the main
 function.

1. Take input from the user for bake lines on-hand
2. Subtract these values from the stock required list
3. Output these results:
   - To API sheet
   - In terminal format

It also became clear that the date must be captured, so the program can address
 the correct figures for the particualar day of business. This is common in
 date-sensitive ACD applications:

![ACD date entry]

When all the parts were in place, I jotted down a paper flow chart consisting of
 the functions I would need to code. As each function was operational, I checked
 it off the list and moved to the next one.

As testing developed, it became clear that several additional functions would
 need to be implemented to fully realize the project goals. These will be
 explored in the features section in detail.

### UX

First and foremost, this program is designed for daily use in a fast-paced,
 customer-centric industry. The application must perform its required function
 efficiently and without friction for the user.

Program flow is clear. The user is guided through the process in polite yet
 assertive manner. All actions are confirmed and no action is taken without
 the user being sure of their choice. All instances of program function are
 clearly delineated and the user should never be confused about what is
 happening at any given moment.

### User Stories

Two parties are referenced in the following user stories:

- The 'Client' - Lidl GB
- The 'User' - The Lidl bakery co-ordinator member of staff

Client goals:

- Increase operational efficiency in daily afternoon bake task
- Aid KPI's by generating correct figures - e.g. only baking what is required
- To make the task accessible to all staff, regardless of mathematical ability
- To further aid the push to paperless working

User goals:

- To perform the daily afternoon bake task more efficiently
- To have confidence that their bake plan is correct
- To have a frictionless experience in performing their task

In the testing section, we will examine how these outcomes have been achieved.

---

## Design Process

- Main Function

  - ![Main flow chart]

- API Integration

## Features

### Display Program Introduction

### Date Input

![ACD date input]

![ACD date out of range]

### Stock Input

- Confirmation

### Final Stock Confirmation

- Restart Program

### Update Worksheets

- Stock on hand

- Stock to bake

### Display Final Stock to Bake

---

## Full Function Flow Charts

![Intro flow]

![Date flow]

![Input flow]

![Confirm flow]

![Update flow]

![Results flow]

---

## Testing

- Show procedures

- Each function

- Text formatting

---

## Validation

- VS Code linter

- CI PEP8 linter

## Bugs

- Append to list if invalid data:
  - Append inside if block

- Final list appending items separately instead of making one big list:
  - Use `.extend()` not `.append()`

- var only holding first sum when calculating stock to bake:
  - `calculation = [(required - on_hand)]` enclose var in list brackets

- Returned stock list only returning one number, not a list:
  - append to new list inside `for` loop

- Unable to use `<` operand between string and int:
  - Don't use list comprehension for different data types. Use `if` condition
    before append

- List keeps appending values when function is restarted:
  - use `list.clear()` method in `if` statement

- f string too long to access `{var}`:
  - use f strings on multiple lines in parentheses

- Unable to zip item list:
  - use numpy `.concatenate()` method to flatten the list

- Not displaying full results in final list of items to bake:
  - Check correct A1 notation argument for cells to reference in worksheet

- pprint shows artifacts from f strings:
  - Known issue - don't use f strings with pprint. Use separate, surrounding
    print statements

- Dictionaries displayed alphabetically when pprinted:
  - Use `sort_dicts=False` argument when pprinting a dict where insertion order
    is required to be retained

- Typing `...` at the end of an f string causes it to not display:
  - VS Code complained of an 'instance string'. Made new line for asterisk

- Infinite `while` loop in intro function:
  - Missing `()` on `user_input.lower()` so input could never be matched

---

## Project Outcome Summary

- Justify Criteria

- How project needs were met
- Input handling
- Data-driven programming constructs
- Exception handling
- Real-world data model for business needs

- Efficient code
- Flow, granular functions
- No validation errors
- Why libraries were used

![Evidence of meeting project goals]

### Design
- Positive emotional response
- Only input what is required
- All errors reported
- Consistent flow of functions
- Confirmation and feedback

### Development & Implementation
- Clean code
- Defensive design
- Comments
- PEP8 compliance
- Robust code:
  - No logic errors, error handling, API handling, input validation

### Real-World Application

### Security

- CREDS.json

### Data

- Well-structured
- Dependencies frozen
- No terminal errors
- Version control
- Credit inline
- Self-explanatory readme

---

## Version Control

## Deployment

- GitHub

- Heroku

  - Dependencies

## Technologies Used

- Libraries

## Additional Credits & Resources

- Credit in addition to those inline in `run.py`

## Future Design Ideas

- Real world implementation ideas

## Closing Words

- Achievements

- Lessons learned