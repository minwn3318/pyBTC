from flask import Flask
from flask import render_template
import requests
import json
import os
import pandas as pd

app = Flask(__name__, template_folder=os.getcwd())

@app.route('/')
def index() :
    headers = {'Content_type' : 'application/json; charset=utf-8'}
    res = requests.get("http://localhost:5000/chain", headers=headers)

    status_json = json.loads(res.text)
    df_scan = pd.DataFrame(status_json['chain'])

    return render_template('/one_node_scan.html', df_scan = df_scan, block_len = len(df,scan))

app.run(port=8000)
