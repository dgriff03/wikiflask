
from flask import Flask,render_template,request
from flask import request
import json
import requests
import sys

app = Flask(__name__)

@app.route('/', methods=['get'])
def home():
    return render_template("index.html")


@app.route("/getData")
def get_data():
    try:
        from ast import literal_eval
        url = "http://ec2-54-173-58-136.compute-1.amazonaws.com:8001/titlelinks/path2?from=Soweto&to=Roodepoort"
        res = requests.get(url)
        text = res.text
        text = text[15:-2]
        paths = text.split("],[")
        lists = [x.replace("[","").replace("]","").split(",") for x in paths]
        return json.dumps(lists)
    except:
        return json.dumps({"error":"error"})

if __name__ == '__main__':
    app.run()
