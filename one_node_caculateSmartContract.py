import requests
import json
import pandas as pd
import hashlib # hash �븿�닔�슜 sha256 �궗�슜�븷 �씪�씠釉뚮윭由�
from flask import Flask, request, jsonify
import time
import hashlib # hash 함수용 sha256 사용할 라이브러리
import datetime

headers = {'Content-Type' : 'application/json; charset=utf-8'}

calculate_string = []
operation = 0
input_string = ""


def Input_Button(input_Thing) :
    global operation
    global calculate_string
    global input_string

    calculate_string.append(input_Thing)

    if input_Thing == "+" or input_Thing == "-" or input_Thing == "*" or input_Thing == "/" or input_Thing == "=" :
        operation = operation + 1

    if (operation == 2) :
        num1_str = ""
        num2_str = ""
        operator = None
        last_operator = None

        for item in calculate_string[:-1]:
            if isinstance(item, int):
                if operator is None:
                    num1_str += str(item)
                    print("num1 ", num1_str)
                else:
                    num2_str += str(item)
                    print("num2 ", num2_str)
            else:
                operator = item

        num1 = int(num1_str)
        num2 = int(num2_str)
        last_operator = calculate_string[-1]

        calculate_input = {
            "type" : "calculate_input",
            "num1" : num1,
            "operator" : operator,
            "num2" : num2,
            "last_operator" : last_operator
        }

        return calculate_input
    
    for item in calculate_string :
        input_string += str(item)

    intermeditate_string = input_string
    intermeditate_input = {
        "type" : "intermeditate_input",
        "input_thing" : intermeditate_string
    }
    input_string = ""
    return intermeditate_input

def calculator(num1, operator, num2, last_operator) :
    global operation
    global calculate_string
    global input_string

    num1 = int(num1)
    num2 = int(num2)
    if last_operator == "=" :
        operation = 0

        if operator == "+" :
            output = num1 + num2
        elif operator == "-" :
            output = num1 - num2
        elif operator == "*" :
            output = num1 * num2
        elif operator == "/" :
            output = num1 / num2
        final_output = {
            "output" : output
        }
        calculate_string = []
        calculate_string.append(output)
        return final_output

    elif  last_operator == "+" or last_operator == "-" or last_operator == "*" or last_operator == "/" :
        operation = 1
        calculate_string = []

        if operator == "+" :
            last_output = num1 + num2
        elif operator == "-" :
            last_output = num1 - num2
        elif operator == "*" :
            last_output = num1 * num2
        elif operator == "/" :
            last_output = num1 / num2

        calculate_string.append(last_output)
        calculate_string.append(last_operator)

        for item in calculate_string :
            input_string += str(item)

        output_string = input_string
        input_string = ""

        intermediate_output = {
            "output" : output_string 
        }
        return intermediate_output

def Reset() :
    global calculate_string
    calculate_string = []

my_ip = '0.0.0.0'
my_port = '8003'

app = Flask(__name__)

@app.route('/putting', methods = ['POST'])
def Inputting() :
    input_thing = request.get_json()["input"]
    response = Input_Button(input_thing)
    if response["type"] == "calculate_input" :
        data = {
            "num1" : response['num1'],
            "operator" : response['operator'],
            "num2" : response['num2'],
            "last_operator" : response['last_operator']
        }
        response = requests.post("http://127.0.0.1:8003/calculation", headers=headers, data = json.dumps(data))
        response = response.json()  # requests 라이브러리의 json() 메서드 사용

    result_data =  {
                'sender' : "smartContract_calculator", # 송신자
                'recipient' : "master1", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "result" : response,
                }
            }
    
    result_dataJson = json.dumps(result_data, sort_keys=True)
    contract_Hash = hashlib.sha256(result_dataJson.encode()).hexdigest()
    result_data["smart_contract"]["contract_Hash"] = contract_Hash
    requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = result_dataJson)

    return jsonify(response), 201

@app.route('/calculation', methods = ['POST'])
def calculating() :
    calculating_input = request.get_json()
    response = calculator(calculating_input['num1'],calculating_input['operator'],
               calculating_input['num2'],calculating_input['last_operator'])
    
    calcualte_result_data =  {
                'sender' : "smartContract_calculator", # 송신자
                'recipient' : "master1", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "operator1 type" : calculating_input['operator'],
                    "operator2 type" : calculating_input['last_operator'],
                    "result" : response,
                }
            }

    calcualte_result_dataJson = json.dumps(calcualte_result_data, sort_keys=True)
    contract_Hash = hashlib.sha256(calcualte_result_dataJson.encode()).hexdigest()
    calcualte_result_data["smart_contract"]["contract_Hash"] = contract_Hash
    requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = calcualte_result_dataJson)
    
    print("end calculate")
    return jsonify(response), 201

@app.route('/reset', methods = ['GET'])
def resetting() :
    Reset()
    response = {
        "reset" : "compelet",
        "inputing_string" : calculate_string
    }

    reset_data =  {
                'sender' : "smartContract_calculator", # 송신자
                'recipient' : "master1", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "reset" : "reset succes"
                }
            }
    
    reset_dataJson = json.dumps(reset_data, sort_keys=True)
    contract_Hash = hashlib.sha256(reset_dataJson.encode()).hexdigest()
    reset_data["smart_contract"]["contract_Hash"] = contract_Hash
    requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = reset_dataJson)

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)