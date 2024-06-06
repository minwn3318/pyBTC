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
                           "contract_code" :"token_name = 'pySTAKINGTOKEN' \ntoken_total_volume = 100000\ntoken_owner = {'token_maker' : 10000}\nstaking_status = {}",
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
""",
                           "contract_function_token_staking" :"""
def token_staking(staker,amount):
    if staker in token_owner.keys():                       ## 예치자(staker)가 실제 존재하는 사용자인지 확인
        if get_balance(staker) > amount:                   ## 예치자(staker)의 잔고가 예치 금액보다 많은지 확인
            token_owner[staker]  = token_owner[staker] - amount   ## 예치자(staker)의 잔고에서 예치 금액 제외
            staking_status [len(staking_status)] =  {'staker':staker,'amount':amount}  
            ## 예치 정보(staking_status)에 예치자(staker)의 예치내역 저장
            print("Staing Completed")
            get_balance(staker) 
            
        else:
            return "Insufficient Balance"
    else:
        return "Unavailable Staker id"
""",
                           "contract_function_staking_yield" :"""
def staking_yield(staking_status):                                 ## 예치 이자 지급함수
    for t in staking_status:
        print(staking_status[t])
            staking_status[t]['amount'] = staking_status[t]['amount'] * (1+0.1)    ## 예치 이자가 10% 지급된 금액으로 예치금 변경
    return staking_status
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
                    break
        print(Lottery())       
        invaild_transaction = True       

    elif select_command == '0' :
        print("클라이언트를 종료합니다")
        run_client = False

    else :
        print("범위 이외 값을 선택하셨습니다 다시 선택하여 주십시오")