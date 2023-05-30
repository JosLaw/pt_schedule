import gspread
import pandas as pd
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
    user = []

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
                else:
                    print(f"Creating profile for {client} \n")
                    break
            else:
                raise ValueError(
                    f"Type (Y) or (N)"
                )
        except ValueError as e:
            print(f"Invalid input: {e}.\n")


get_name()
check_client()
