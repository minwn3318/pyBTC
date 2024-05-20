import requests
import json
import pandas as pd
import hashlib
import random

headers = {'Content_Type' : 'application/json; charset=utf-8'}
res = requests.get("http://localhost:5000/chain", headers=headers)
json.loads(res.content)

headers = {'Content_Type' : 'application/json; charset=utf-8'}
data = {
    "sender" : "test_from",
    "recipient" : "test_to",
    "amount" : 3
}
requests.post("http://localhost:5000/transactions/new", headers=headers,
              data = json.dumps(data)).content

headers = {'Content_Type' : 'application/json; charset=utf-8'}
res = requests.get("http://localhost:5000/mine")
print(res)
print(res.text)

headers = {'Content_Type' : 'application/json; charset=utf-8'}
data = {
    "sender" : "test_from",
    "recipient" : "test_to2",
    "amount" : 30
}
requests.post("http://localhost:5000/transactions/new", headers=headers,
              data = json.dumps(data)).content

headers = {'Content_Type' : 'application/json; charset=utf-8'}
data = {
    "sender" : "test_from",
    "recipient" : "test_to3",
    "amount" : 300
}
requests.post("http://localhost:5000/transactions/new", headers=headers,
              data = json.dumps(data)).content

headers = {'Content_Type' : 'application/json; charset=utf-8'}
res = requests.get("http://localhost:5000/mine")
print(res)
print(res.text)

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
