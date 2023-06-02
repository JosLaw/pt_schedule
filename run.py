import gspread
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pt_ schedule')

user = []  # Array to hold username
booking = []  # Array to hold booking details
target_per_week = []  # Array to hold user's target number of training per week

# Days to book
days = {
    0: ("Mon"),
    1: ("Tues"),
    2: ("Wed"),
    3: ("Thur"),
    4: ("Fri"),
    5: ("Sat"),
    6: ("Sun"),
}

# Days from spreadsheet
booking_worksheet = SHEET.worksheet('bookings')
worksheet_days = {
    'mon': booking_worksheet.get('B2:B12'),
    'tues': booking_worksheet.get('C2:C12'),
    'wed': booking_worksheet.get('D2:D13'),
    'thur': booking_worksheet.get('E2:E12'),
    'fri': booking_worksheet.get('F2:F12'),
    'sat': booking_worksheet.get('G2:G12'),
    'sun': booking_worksheet.get('H2:H12'),
}

day_choice = ""


def get_name():
    """
    Gets user name. Will need first name and initial of surname
    to be valid.
    """
    while True:
        print("Enter first name & surname initial (NameS)")
        name = input("Name: ").capitalize()
        try:
            if len(name) <= 2:
                raise ValueError(
                    f"More than one letter required for name"
                )
            elif not name.isalpha():
                raise ValueError(
                    f"Use format NameS. Special characters not recognised"
                )
            else:
                break
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
    global client
    client = name[:-1] + name[-1].upper()
    return client


def check_client():
    """
    Checks if user is existing client or new client
    Searches spreadhseet for name to confirm user input
    """

    while True:
        client_check = input("Exsisting client? (Y) or (N): \n").capitalize()
        try:
            if client_check == "Y" or client_check == "N":
                print("Checking database...")
                user.append(client)
                worksheet = SHEET.worksheet('clients')
                client_list = worksheet.get('A2:A12')
                if user in client_list:
                    print(f"Welcome back {client} \n")
                    break
                else:
                    print(f"Creating profile for {client} \n")
                    break
            else:
                raise ValueError(
                    f"Type (Y) or (N)"
                )
        except ValueError as e:
            print(f"Invalid input: {e}.\n")


def make_booking():
    """
    Provides booking options and puts the
    information into an array
    """
    while True:
        new_booking = input("Make a new booking? (Y) or (N)\n").capitalize()
        try:
            if new_booking == "N":
                print("Thanks for enquiring. See you soon!")
                break
            elif new_booking == "Y":
                print("Checking database...")
                print(days)
                select_day = int(input(
                    "What day would you like to book? Enter value 0 - 6: \n"))
                if select_day not in days:
                    raise ValueError(
                        f"Please enter a listed number for day"
                    )
                else:
                    global choice_day
                    choice_day = days[select_day]
                    print(
                        f"You selected {choice_day}"
                    )
                    print("checking system...")
                    check_worksheet()
                    break
            else:
                print("Invalid input. Type (Y) or (N)")
        except ValueError as e:
            print(f"Invalid input: {e}.\n")


def check_worksheet():
    """
    Checks worksheet for unbooked time slots which are marked by '-'
    from user's day choice
    """
    b_test = np.array(worksheet_days[choice_day.lower()])
    searchval = '-'
    ii = np.where(b_test == searchval)[0]
    print(ii)


def update_clients(data):
    """
    Updates worksheet with the client name data provided
    """
    create_user = SHEET.worksheet("clients")
    create_user.append_row(data)


# def main():
    """
    Calls all functions required on page load
    """
    get_name()
    check_client()
    make_booking()
    # update_clients(user)


make_booking()
