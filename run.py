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
            if len(name) <= 1:
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



