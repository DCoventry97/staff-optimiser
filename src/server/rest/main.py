#!flask/bin/python
import xml.etree.cElementTree as ET
from flask import Flask, request, Response, jsonify, render_template, redirect
import json
import sys
from linear_regression import LinearRegression
from os import path

app = Flask(__name__)

lin_reg = LinearRegression()

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/getreport/<id>")
def view_report(id):
    result = lin_reg.get_val(id)
    if abs(result) > 0.1:
        advice = "No trend detected, they are consistent over the day."
    elif result > 0:
        advice = "more productive later in the day."
    else:
        advice = "more productive earlier in the day."
    return render_template("result.html", advice=advice, id=id)


@app.route("/getreport", methods=["GET","POST"])
def get_report():
    if request.method == "GET":
        with open("staff.txt") as staff_names:
            all_names = staff_names.readlines()
            del all_names[0]
        return render_template("select_report.html", names=all_names)
    else:
        staff = request.form["staff-select"]
        return redirect("/getreport/"+staff)


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

        file = path.isfile("./xml/"+staff_name+".xml")
        if not file:
            root = ET.Element("staffData")
            tree = ET.ElementTree(root)
            tree.write("./xml/"+staff_name+".xml")
            with open("staff.txt", "a") as staff_names:
                staff_names.write("\n"+staff_name)
                staff_names.close()

        with open("./xml/"+staff_name+".xml") as file:
            tree = ET.parse("./xml/"+staff_name+".xml")
            root = tree.getroot()
            new_rating = ET.SubElement(root, "rating")
            new_time = ET.SubElement(new_rating, "time")
            new_time.text = str(time)
            new_score = ET.SubElement(new_rating, "score")
            new_score.text = str(score)
            tree.write("./xml/"+staff_name+".xml")

        return jsonify({"a":score}), 201



if __name__ == '__main__':
    app.run(debug=True, port=7643)
