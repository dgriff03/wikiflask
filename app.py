# Tony Cannistra, Brett Fischler, and Dan Griffin
# Fall 2014
# Comp50 Final Project

from flask import Flask,render_template,request
from flask import request
import json
import requests
import sys

app = Flask(__name__)



# Retrieves Zulu Wikipedia pages from static/words.json
# Renders index.html template
@app.route('/', methods=['get'])
def home():
    try:
        Words = json.load(open("static/words.json"))
        Words["from"] = sorted( Words["from"] )
        Words["to"] = sorted( Words["to"] )
    except:
        Words = {"from": [], "to": []}
    return render_template("index.html", Words = Words)

# Gets and returns all paths from from_page to to_page
@app.route("/getData")
def get_data():
    try:
        try:
            jdata = request.args
            keys = jdata.keys()
            if (not "from_page" in keys) or (not "to_page" in keys):
                raise "bad keys"
            word_to = jdata["to_page"]
            word_from =jdata["from_page"]
        except:
            # Defaults to Soweto -> Roodepoort on exception
            word_to = "Roodepoort"
            word_from = "Soweto"
        from ast import literal_eval
        url = "http://ec2-54-173-58-136.compute-1.amazonaws.com:8001/titlelinks/" + \
              "path2?from={}&to={}".format(word_from,word_to)
        # Makes request to use our path_finder algorithm
        res = requests.get(url)
        text = res.text
        text = text[15:-2]
        paths = text.split("],[")
        lists = [x.replace("[","").replace("]","").split(",") for x in paths]
        if not lists[0][0]:
            lists = []
        return json.dumps(lists)
    except:
        return json.dumps({"error":"error"})

if __name__ == '__main__':
    app.run()
