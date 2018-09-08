'''
Function to read user data from a json file
'''
import json
from pathlib import Path


def read(username):
    staff_name = username
    my_file = Path("./" + staff_name + ".json")
    if my_file.is_file():
        with open(staff_name + ".json", "r") as f:
            existing_data = json.load(f)

            return existing_data
