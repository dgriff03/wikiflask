
from flask import Flask,render_template,request
from flask import request
import json
import numpy as np
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


@app.route("/data")
@app.route("/data/<int:ndata>")
def data(ndata=100):
    """
    On request, this returns a list of ``ndata`` randomly made data points.
    :param ndata: (optional)
        The number of data points to return.
    :returns data:
        A JSON string of ``ndata`` data points.
    """
    x = 10 * np.random.rand(ndata) - 5
    y = 0.5 * x + 0.5 * np.random.randn(ndata)
    A = 10. ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
        "color": c[i]}
        for i in range(ndata)])

if __name__ == '__main__':
    app.run()
