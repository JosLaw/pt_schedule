import gspread
import pandas as pd
import numpy as np
from more_itertools import locate
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
booking_day = []
booking_time = []  # Array to hold booking details
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

# Timeslot from worksheet
timeslot = {
    0: ("08:00"),
    1: ("09:00"),
    2: ("10:00"),
    3: ("11:00"),
    4: ("12:00"),
    5: ("13:00"),
    6: ("14:00"),
    7: ("15:00"),
    8: ("16:00"),
    9: ("17:00"),
    10: ("18:00"),
}


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
                print("Thanks for enquiring. Come back soon!")
                exit()
            elif new_booking == "Y":
                print("Checking database...")
                break
            else:
                print("Invalid input. Type (Y) or (N)")
        except ValueError as e:
            print(f"Invalid input: {e}.\n")


def chose_day():
    """
    User to select day
    """
    print(days)
    while True:
        select_day = int(input(
            "What day would you like to book? Enter value 0 - 6: \n"))
        try:
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
                booking_day.append(choice_day)
                break
        except ValueError as e:
            print(f"Invalid input: {e}.\n")


def check_worksheet():
    """
    Checks worksheet for unbooked time slots which are marked by '-'
    from user's day choice
    """
    while True:
        check_timeslot = np.array(worksheet_days[choice_day.lower()])
        searchval = '-'
        ii = np.where(check_timeslot == searchval)[0]
        free = [(i) for i in ii if i in timeslot]
        available_slots = [(k, v) for k, v in timeslot.items() if k in free]
        slot = [k[0] for k in available_slots]
        print(f"Available slots: \n {available_slots} \n")
        choice = int(input(f"Select timeslot: "))
        try:
            if choice not in slot:
                raise ValueError(
                    f"Please enter a listed number"
                )
            else:
                choice_time = timeslot[choice]
                booking_time.append(choice_time)
                print(f"You selected {choice_time}")
                break
        except ValueError as e:
            print(f"Slot unavailable: {e}.\n")


def update_bookings(date, hour):
    """
    Update spreadsheet with user booking
    """
    b_worksheet = SHEET.worksheet('bookings')
    b_day = b_worksheet.get('B1:H1')
    b_time = b_worksheet.get('A2:A12')
    print(date, hour)


def update_clients(data):
    """
    Updates worksheet with the client name data provided
    """
    create_user = SHEET.worksheet("clients")
    create_user.append_row(data)


def main():
    """
    Calls all functions required on page load
    """
    get_name()
    check_client()
    make_booking()
    chose_day()
    check_worksheet()
    # update_clients(user)
    update_bookings(booking_day, booking_time)


main()
