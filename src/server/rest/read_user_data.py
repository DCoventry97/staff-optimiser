'''
Function to read user data from a json file
'''
import xml.etree.cElementTree as ET
from os import path


def read(username):
    staff_name = username
    if path.isfile("./xml/"+staff_name + ".xml"):
        with open("./xml/"+staff_name + ".xml", "r") as file:
            tree = ET.parse(file)
            root = tree.getroot()

            scores = []
            times = []
            for child in root:
                scores.append(child.find("score").text)
                times.append(child.find("time").text)
            return times, scores