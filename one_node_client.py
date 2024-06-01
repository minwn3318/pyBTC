import requests
import json
import pandas as pd
import hashlib # hash 함수용 sha256 사용할 라이브러리
import random

run_client = True
invaild_transaction = True
while run_client : 

    headers = {'Content-Type' : 'application/json; charset=utf-8'}

    select_command = input("실행할 명령어를 선택해 주십시오 (1 = chain), (2 = transaction), (3 = mine), (0 = end client): ")
    if select_command == '1' :
        print("블록체인을 가져오고 있습니다 잠시만 기다려 주십시오")
        res = requests.get("http://localhost:5000/chain", headers=headers)
        try :
            print(res.json())
        except :
            print("응답메시지에 오류가 생겼습니다")

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
        }
        print('거래내역을 생성중입니다 잠시만 기다려 주십시오')
        res = requests.post("http://localhost:5000/transactions/new", headers=headers, data=json.dumps(data)).content
        try :
            print(res.json())
        except :
            print("응답메시지에 오류가 생겼습니다")
        invaild_transaction = True

    elif select_command =='3' :
        print("블록생성 중입니다 잠시만 기다려주십시오")
        res = requests.get("http://localhost:5000/mine")
        try :
            print(res.json())
        except :
            print("응답메시지에 오류가 생겼습니다")

    elif select_command == '0' :
        print("클라이언트를 종료합니다")
        run_client = False

    else :
        print("범위 이외 값을 선택하셨습니다 다시 선택하여 주십시오")