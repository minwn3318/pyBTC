from flask import Flask
from datetime import dtetime
from flask import render_template
from flask import request
from flask import redirect

import requests
import json
import os
import Pandas as pd

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        print("login 지갑주소 : ", input_value)
        headers = {'Content_Type' : 'application/json; charset=utf-8'}
        res = requests.get("http://localhost:5000/chain", headers=headers)

        status_json = json.loads(res.text)
        status_json['chain']
        tx_amount_l = []
        tx_sender_l = []
        tx_reciv_l = []
        tx_time_l = []

        for chain_index in range(len(status_json['chain'])) :
            chain_tx = stauts_json['chain'][chain_index]['transactions']

            for each_tx in range(len(cahin_tx)) :
                tx_amount_l.append(chain_tx[eacht_tx]['amount'])
                tx_sender_l.append(chain_tx[eacht_tx]['sender'])
                tx_reciv_l.append(chain_tx[eacht_tx]['reciv'])
                tx_time_l.append(chain_tx[eacht_tx]['time'])

        df_tx = pd.DataFrame()
        df_tx['timestamp'] = tx_time_l
        df_tx['sender'] = tx_sender_l
        df_tx['recipient'] = tx_reciv_l
        df_tx['amount'] = tx_amount_l
        df_tx

        df_sender = pd.DataFrame(df_tx.groupby('sender')['amount'].sum()).reset_index()
        df_sender.columns = ['user', 'sender_amount']
        df_received = pd.DataFrame(df_tx.groupby('recipient')['amount'].sum()).reset_index())
        df_received.columns = ['user', 'received_amount']
        df_received

        df_status = pd.merge(df_receivd, df_sended, on ='user', how = outer).fillna(0)
        df_status['balanc'] = df_status['received_amount'] - df_status['sended_amount']
        df_status

        if df_status['user']==input_value['wallet_id'][0].sum() == 1 :
            print("로그인 성공")
            return render_template("wallet.html", wallet_id = input_value['wallet_id'][0], wallet_value = df_status[df_status['user'] ==df_status['user'].iloc[0]['balance'].iloc[0]])
        else :
            return "잘못된 지갑주소입니다."
        
    return render_template('login.html')
        
@app.route('/wallet', methods = ['GET', 'POST'])
def wallet():
    if request.method == 'POST' :
        send_value = int(request.form.to_dict(flat=False)['send_value'][0])
        send_target = request.form.to_dict(flat = False)['send_target'][0]
        send_from = request.form.to_dict(flat=False)['send_from'][0]
        print("Login Wallet ID : ", send_from)

        if send_value > 0:
            print("Send Amout : ", send_value)
            headers = {'Content-Type' : 'application/json; charset = utf-8'}
            data = {
                "sender" : send_from,
                "recipient" : send_target,
                "amount" : send_value,
            }
            requests.post("http://localhost:5000/transactions/new", headers=headers, data=json.dumps(data))
            return "전송완료!!"

        else :
            return "0 pyBTC 이상 보내주세요!"

    return render_template('wallet.html')
