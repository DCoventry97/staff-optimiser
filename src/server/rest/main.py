#!flask/bin/python
import xml.etree.cElementTree as ET
from flask import Flask, request, Response, jsonify, render_template
import json
from os import path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/staffscore", methods=["POST"])
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

        file = path.isfile("..//algorithms/"+staff_name+".xml")
        if not file:
            root = ET.Element("staffData")
            tree = ET.ElementTree(root)
            tree.write("..//algorithms/"+staff_name+".xml")

        with open("..//algorithms/"+staff_name+".xml") as file:
            tree = ET.parse("..//algorithms/"+staff_name+".xml")
            root = tree.getroot()
            new_rating = ET.SubElement(root, "rating")
            new_time = ET.SubElement(new_rating, "time")
            new_time.text = str(time)
            new_score = ET.SubElement(new_rating, "score")
            new_score.text = str(score)
            tree.write("..//algorithms/"+staff_name+".xml")

        return jsonify({"a":score}), 201



if __name__ == '__main__':
    app.run(debug=True, port=7643)
