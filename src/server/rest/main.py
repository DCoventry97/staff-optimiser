#!flask/bin/python
import xml.etree.cElementTree as ET
from flask import Flask, request, Response, jsonify
import json
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route("/staffscore", methods=["GET", "POST"])
def staff_score():
    staff_name = ""
    score = None
    time = None
    #checks if post request
    if request.method == "POST":
        #gets data from post request in json form
        data = request.get_json()
        subdata = data.get("report")
        staff_name = subdata.get("name")
        time = subdata.get("time")
        score = subdata.get("score")

        file = Path("./"+staff_name+".xml")
        if not file.is_file():
            root = ET.Element("staffData")
            tree = ET.ElementTree(root)
            tree.write(staff_name+".xml")

        with open(staff_name+".xml") as file:
            tree = ET.parse(staff_name+".xml")
            root = tree.getroot()
            new_rating = ET.SubElement(root, "rating")
            new_time = ET.SubElement(new_rating, "time")
            new_time.text = time
            new_score = ET.SubElement(root, "score")
            new_score.text = score
            tree.write(staff_name+".xml")

    return jsonify(name=staff_name, s=score, t=time)



if __name__ == '__main__':
    app.run(debug=True, port=7643)
