import requests
import json
import pandas as pd
import hashlib # hash 함수용 sha256 사용할 라이브러리
import random

run_client = True
invaild_transaction = True
while run_client : 

    headers = {'Content-Type' : 'application/json; charset=utf-8'}

    select_command = input("실행할 명령어를 선택해 주십시오 (1 = registe node) (2 = chain), (3 = transaction), (4 = mine), (0 = end client) : ")
    print(select_command)
    print("\n----------\n")
    if select_command == '1' :
        while invaild_transaction :
            try :
                input_node = input("연결받는 블록체인의 노드 url주소와 연결될 노드 url주소를 공백으로 구분하여 입력하십시오(http://제외) : ").split()
                recived_node = "http://" + input_node[0] + "/nodes/register"
                registered_node = "http://" + input_node[1]
                print("노드주소 : ", recived_node, registered_node)
                print("\n----------\n")
                data = {
                    'nodes' : registered_node
                }
                invaild_transaction = False
            except :
                 print("입력 양식이 맞지 않습니다 다시 입력해주세요  1")
                 print("입력내용 : ", input_value)
                 print("\n----------\n")

        print("노드를 연결하고 있습니다 잠시만 기다려 주십시오 : ", recived_node, "<---", registered_node)
        res = requests.post(recived_node, headers=headers, data = json.dumps(data)).content
        try :
            print(json.loads(res))
            print("\n----------\n")
        except :
            print("잘못된 주소이거나 응답메시지에 오류가 생겼습니다 : 2")
            print("\n----------\n")
        invaild_transaction = True

    if select_command == '2' :
        while invaild_transaction :
            try :
                input_value = input("가져올 블록체인의 노드 url주소(http://제외)를 입력하십시오 :")
                chain_node = "http://" + input_value + "/chain"
                print("노드주소 : ", chain_node)
                print("\n----------\n")
                invaild_transaction = False
            except :
                 print("입력한 내용의 입력 양식이 맞지 않습니다 다시 입력해주세요 : 2")
                 print("입력내용 : ", input_value, chain_node)
                 print("\n----------\n")

        print("블록체인을 가져오고 있습니다 잠시만 기다려 주십시오")
        res = requests.get(chain_node, headers=headers)
        try :
            print(res.json())
            print("\n----------\n")
        except :
            print("잘못된 주소이거나 응답메시지에 오류가 생겼습니다 : 2")
            print("\n----------\n")
        invaild_transaction = True


    elif select_command == '3' :
        while invaild_transaction :
            try :
                input_value = input("송신자아이디, 수신자아이디, 보내는 양('숫자') 순서로 공백(띄어쓰기)으로 구분하여 입력해주세요 : ").split()
                print("\n----------\n")
                input_value[2] = int(input_value[2])
                input_node = input("트랜잭션을 생성할 블록체인의 노드 url주소(http://제외)를 입력하십시오 :")
                chain_node = "http://" + input_node + "/chain"
                print("노드주소 : ", chain_node)
                print("\n----------\n")
                invaild_transaction = False
            except :
                 print("입력 양식이 맞지 않습니다 다시 입력해주세요 : 3-1")
                 print("입력내용 : ", input_value)
                 print("\n----------\n")
        
        data = {
                "sender": input_value[0],
                "recipient": input_value[1],
                "amount": input_value[2],
        }
        print('거래내역을 생성중입니다 잠시만 기다려 주십시오')
        res = requests.post("http://localhost:5000/transactions/new", headers=headers, data=json.dumps(data)).content
        try :
            print(json.loads(res))
            print("\n----------\n")
        except :
            print("잘못된 주소이거나 응답메시지에 오류가 생겼습니다 : 3")
            print("\n----------\n")
        invaild_transaction = True

    elif select_command =='4' :
        while invaild_transaction :
            try :
                input_node = input("블록을 생성할 블록체인의 노드 url주소(http://제외)를 입력하십시오 :")
                chain_node = "http://" + input_node + "/chain"
                print("노드주소 : ", chain_node)
                print("\n----------\n")
                invaild_transaction = False
            except :
                 print("입력한 내용의 입력 양식이 맞지 않습니다 다시 입력해주세요 : 4")
                 print("입력내용 : ", input_value, chain_node)
                 print("\n----------\n")

        print("블록생성 중입니다 잠시만 기다려주십시오")
        res = requests.get("http://localhost:5000/mine")
        try :
            print(res.json())
            print("\n----------\n")
        except :
            print("잘못된 주소이거나 응답메시지에 오류가 생겼습니다 : 4")
            print("\n----------\n")
        invaild_transaction = True

    elif select_command == '0' :
        print("클라이언트를 종료합니다")
        run_client = False

    else :
        print("범위 이외 값을 선택하셨습니다 다시 선택하여 주십시오")
        print("\n----------\n")
