# Lidl BakeMate Python Terminal Application

![Lidl Bakery Items]

Live link - [Heroku](https://pp3-lidl-bake-mate.herokuapp.com/)

Accompanying spreadsheet - [Google Sheets](https://docs.google.com/spreadsheets/d/1F5qGL73_mbY4tX07SAwo8x-ooswImLdlVWjapZWEyjg/edit#gid=1612631949)

---

## Overview

- Usage Scenario

---

## Planning

### UX

### User Stories

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