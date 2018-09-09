#!flask/bin/python
from flask import Flask, request, Response, jsonify
import json
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route("/staffscore", methods=["GET", "POST"])
def staff_score():
    staff_name = None
    score = None
    time = None
    #checks if post request
    if request.method == "POST":
        #gets data from post request in json form
        data = request.get_json()
        staff_name = data.get("name")
        time = data.get("time")
        score = data.get("score")

        my_file = Path("./"+staff_name+".json")
        if my_file.is_file():
            with open(staff_name+".json", "r") as f:
                existing_data = json.load(f)
                print(existing_data)

            with open(staff_name + ".json", "w") as file:
                existing_data.update(data)
                print(existing_data)
                json.dump(existing_data, file)
        else:
            with open(staff_name+'.json', 'w') as outfile:
                json.dump(data, outfile)

    return jsonify(name=staff_name, s=score, t=time)



if __name__ == '__main__':
    app.run(debug=True, port=7643)
