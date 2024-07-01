import requests
import json
import pandas as pd
import msvcrt
import time
import hashlib # hash 함수용 sha256 사용할 라이브러리
import datetime

headers = {'Content-Type' : 'application/json; charset=utf-8'}

def start() :
    start_data =  {
                    'sender' : "user_03", # 송신자
                    'recipient' : "smartContract_calculator", # 수신자
                    'amount' : 0, # 금액
                    'timestamp':time.time(),
                    'smart_contract' : {
                        "message" : "login caculator",
                        "user" : "user03",
                    }
                }
    start_dataJson = json.dumps(start_data, sort_keys=True)
    contract_Hash = hashlib.sha256(start_dataJson.encode()).hexdigest()

    start_data["smart_contract"]["contract_Hash"] = contract_Hash
    requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = start_dataJson)

def get_single_character_input():
    print(":", end='', flush=True)
    char = msvcrt.getch().decode('utf-8')
    print(char)  # 입력한 글자를 출력하고 줄을 바꿈
    return char

def end_client() :
        print("계산기를 종료합니다")
        end_data =  {
                'sender' : "user_03", # 송신자
                'recipient' : "smartContract_calculator", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "message" : "end caculator",
                    "user" : "user03",
                }
            }
        
        end_dataJson = json.dumps(end_data, sort_keys=True)
        contract_Hash = hashlib.sha256(end_dataJson.encode()).hexdigest()
        end_data["smart_contract"]["contract_Hash"] = contract_Hash
        requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = end_dataJson)

def reset_client():
        print("계산기를 초기화합니다")
        reset_data =  {
                'sender' : "user_03", # 송신자
                'recipient' : "smartContract_calculator", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "message" : "reset caculator",
                    "user" : "user03",
                }
            }
        reset_dataJson = json.dumps(reset_data, sort_keys=True)
        contract_Hash = hashlib.sha256(reset_dataJson.encode()).hexdigest()
        reset_data["smart_contract"]["contract_Hash"] = contract_Hash
        requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = reset_dataJson)
        requests.get("http://127.0.0.1:8003/reset", headers=headers)

def put(obj) :
    if obj not in ["+", "-", "*", "/", "="]:
        obj = int(obj)
    data = {
        "input" : obj
    }
    put_data =  {
            'sender' : "user_03", # 송신자
            'recipient' : "smartContract_calculator", # 수신자
            'amount' : 0, # 금액
            'timestamp':time.time(),
            'smart_contract' : {
                "message" : "put something caculator",
                "user" : "user03",
            }
    }
        
    put_dataJson = json.dumps(put_data, sort_keys=True)
    contract_Hash = hashlib.sha256(put_dataJson.encode()).hexdigest()
    put_data["smart_contract"]["contract_Hash"] = contract_Hash
    requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = put_dataJson)
    res = requests.post("http://127.0.0.1:8003/putting", headers=headers, data = json.dumps(data)).content
    print(res)

exe = True
start()

print("계산기 클라이언트입니다. 숫자와 사칙연산을 할 수 있습니다. 종료하고 싶으면 (ENTER)를 입력해주세요. 초기화는 (SPACE)입니다 : ")
while(exe) :
    putting = get_single_character_input()
    if putting == "\r" :
        end_client()
        exe = False
    elif putting == " ":
        reset_client()
    else :
        put(putting)