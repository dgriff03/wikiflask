
from flask import Flask,render_template,request
from flask import request
import json
import numpy as np
import requests
# import pymysql

app = Flask(__name__)

@app.route('/', methods=['get'])
def home():
    return render_template("index.html")


@app.route("/getData")
def get_data():
    url = "http://ec2-54-173-58-136.compute-1.amazonaws.com:8001/titlelinks/path2?from=Soweto&to=Roodepoort"
    jsonData = json.loads(requests.get(url).text)
    try:
        strs = json['titlelinks'].replace('[','').split('],')
        lits = [s.replace('[','').split('],') for s in strs]
        return json.dumps(lits)
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
