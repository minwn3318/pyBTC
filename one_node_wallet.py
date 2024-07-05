from flask import Flask
from datetime import datetime
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

import requests
import json
import os
import pandas as pd

app = Flask(__name__, template_folder=os.getcwd())

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        
        contract_address = request.form.to_dict(flat=False)['smart_contract_addr'][0] 
        print(contract_address)
        # 블록 정보 호출
        headers = {'Content-Type' : 'application/json; charset=utf-8'}
        res = requests.get("http://localhost:5000/chain", headers=headers)
        res_json = json.loads(res.content)
        nft_TF = False
        ## 스마트 컨트랙트를 호출 및 실행
        for _block in res_json['chain']:
            for _tx in _block['transactions']:
                if _tx['smart_contract']['contract_address'] == contract_address:
                    exec( _tx['smart_contract']['contract_code']) 
                    nft_TF = True
                    break
        if nft_TF:
#             print(myNFT)
            return render_template("NFT_Wallet.html",  
                                   nft_name = _tx['smart_contract']['contract_code'].split("'")[3], 
                                   nft_img_url = _tx['smart_contract']['contract_code'].split("'")[7],
                                   nft_addresss = contract_address
                                   )
        else:
            return "잘못된 지갑주소입니다."

        
    return render_template('NFT_Wallet_login.html')
app.run(port=8082)