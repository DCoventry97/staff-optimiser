'''
Function to read user data from a json file
'''
import xml.etree.cElementTree as ET
from pathlib import Path


def read(username):
    staff_name = username
    my_file = Path("./" + staff_name + ".xml")
    if my_file.is_file():
        with open(staff_name + ".xml", "r") as file:
            tree = ET.parse(file)
            root = tree.getroot()

            scores = []
            times = []
            for child in root:
                rating = child.get("rating")
                scores.append(rating.get("score"))
                times.append(rating.get("time"))
            
            return times, scores
