import requests
import json
import pandas as pd
import hashlib # hash 함수용 sha256 사용할 라이브러리
import random

run_client = True
invaild_transaction = True
while run_client : 

    headers = {'Content-Type' : 'application/json; charset=utf-8'}

    select_command = input("실행할 명령어를 선택해 주십시오 (1 = chain), (2 = transaction), (3 = mine), (4 = exe contract), (0 = end client): ")
    if select_command == '1' :
        print("블록체인을 가져오고 있습니다 잠시만 기다려 주십시오")
        res = requests.get("http://localhost:5000/chain", headers=headers)
        print(json.loads(res.content))

    elif select_command == '2' :
        print("select 2")

        while invaild_transaction :
            try :
                input_value = input("송신자아이디, 수신자아이디, 보내는 양('숫자') 순서로 공백(띄어쓰기)으로 구분하여 입력해주세요 : ").split()
                input_value[2] = int(input_value[2])
                invaild_transaction = False
            except :
                 print("입력한 내용이 3개보다 작거나 입력 양식이 맞지 않습니다 다시 입력해주세요")
                 print("입력내용 : ", input_value)

        data = {
                "sender": input_value[0],
                "recipient": input_value[1],
                "amount": input_value[2],
        "smart_contract": {
                           "contract_code" :"token_name = 'pyTOKEN' \ntoken_total_volume = 100000\ntoken_owner = {'token_maker' : 10000, 'user' : 300, 'user2' : 200 }",
                           "contract_function_getBalance" :"""
def get_balance(user_id):
    print('{} Balance is : '.format(user_id), token_owner[user_id])
    return token_owner[user_id]
""",
                           "contract_function_sendToken" :"""
def send_token(sender,recipent,amount):
    if sender in token_owner.keys():
        if get_balance(sender) > amount:
            token_owner[sender]  = token_owner[sender] - amount
            if recipent in token_owner.keys():
                token_owner[recipent]  = token_owner[recipent] + amount
            else :
                token_owner[recipent]  =  amount
            print("Transaction Completed")
            get_balance(sender) 
            get_balance(recipent) 

        else:
            return "Insufficient Balance"
    else:
        return "Unavailable Sender id"
"""
                           }
                }
                
        print('거래내역을 생성중입니다 잠시만 기다려 주십시오')
        res = requests.post("http://localhost:5000/transactions/new", headers=headers, data=json.dumps(data)).content
        print(json.loads(res))
        invaild_transaction = True

    elif select_command =='3' :
        print("블록생성 중입니다 잠시만 기다려주십시오")
        res = requests.get("http://localhost:5000/mine")
        print(json.loads(res.content))

    elif select_command == '4' :
        while invaild_transaction :
            try :
                input_value = input("컨트랙트 주소를 입력해주세요 : ")
                invaild_transaction = False
            except :
                 print("입력한 내용이 3개보다 작거나 입력 양식이 맞지 않습니다 다시 입력해주세요")
                 print("입력내용 : ", input_value)
        
        res = requests.get("http://localhost:5000/chain", headers=headers)
        res_json = json.loads(res.content)

        for _block in res_json['chain']:
            for _tx in _block['transactions']:
                if _tx['smart_contract']['contract_address'] == input_value:
                    exec( _tx['smart_contract']['contract_code'])
                    print(token_name)
                    print(token_total_volume)
                    exec(_tx['smart_contract']['contract_function_getBalance'])
                    get_balance('token_maker')
                    get_balance('user')
                    exec(_tx['smart_contract']['contract_function_sendToken'])
                    send_token('token_maker','user',50)
                    send_token('token_maker','user2',3000)
                    get_balance('user2')

                    break       
        invaild_transaction = True       

    elif select_command == '0' :
        print("클라이언트를 종료합니다")
        run_client = False

    else :
        print("범위 이외 값을 선택하셨습니다 다시 선택하여 주십시오")