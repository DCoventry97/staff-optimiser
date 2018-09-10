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
    #calculates advice and sends it to the user
    result = lin_reg.get_val(id)
    if abs(result) > 0.1:
        advice = "No trend detected, they are consistent over the day."
    elif result > 0:
        advice = "more productive later in the day."
    else:
        advice = "more productive earlier in the day."
    return render_template("result.html", advice=advice, id=id)

#page for manager to view all staff in system and request advice for each of them. 
@app.route("/getreport", methods=["GET","POST"])
def get_report():
    if request.method == "GET":
        #make list of names of staff in system
        all_names = []
        tree = ET.parse("./staff.xml")
        root = tree.getroot()
        for child in root:
            all_names.append(child.text)
            #send page with names of all staff in system
        return render_template("select_report.html", names=all_names)
    else:
        #redirect user to requested report page
        staff = request.form["staff-select"]
        return redirect("/getreport/"+staff)

#post method to send staff score to. 
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

        #check if staff member has an xml file, makes one if not
        file = path.isfile("./xml/"+staff_name+".xml")
        if not file:
            root = ET.Element("staffData")
            tree = ET.ElementTree(root)
            tree.write("./xml/"+staff_name+".xml")
            
            #makes a file to store all staff names in if it does not exist
            if not path.isfile("./staff.xml"):
                root = ET.Element("staffNames")
                tree = ET.ElementTree(root)
                tree.write("staff.xml")

            #stores staff members name in staff.xml
            tree = ET.parse("./staff.xml")
            root = tree.getroot()
            new_user = ET.SubElement(root, "staff")
            new_user.text = staff_name
            tree.write("staff.xml")

        #adds new score and time for staff member
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
