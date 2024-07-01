from flask import Flask
from datetime import datetime
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import time
import hashlib # hash 함수용 sha256 사용할 라이브러리

import requests
import json
import os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES, PKCS1_OAEP

headers = {'Content-Type' : 'application/json; charset=utf-8'}

def generate_salt():
    return get_random_bytes(32)

def xor_bytes(data1, data2):
    return bytes(a ^ b for a, b in zip(data1, data2))

def generate_key(password, salt):
    password_bytes = password.encode('utf-8')
    password_bytes = pad(password_bytes, 32)[:32]  # 패스워드를 32바이트로 패딩
    key = xor_bytes(password_bytes, salt)
    return key

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv, ciphertext

def decrypt(iv, ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

exe_wallet = True
nick_exe = True
pass_exe = True
while(exe_wallet) :
    select = input("진행할 내용을 입력하세요 '1번 회원가입', '2번 로그인', '3번 블록체인 가져오기', '4번 트랜잭션 생성': ")
    if select == '1':
        while(nick_exe) :
            nick_name = input("닉네임을 먼저 입력해주세요 : ")
            get_chain = requests.get("http://localhost:5000/chain", headers=headers)
            transactions = get_chain["chain"] 
            for smart_Contract in transactions :
                smart_Contract = smart_Contract["smart_contract"]
                print(smart_Contract)
                if smart_Contract["type"] == "join" :
                    if smart_Contract["user_name"] == nick_name :
                        print("nickName equal")
                        print("닉네임 중복, 다시 입력해주세요")
                        nick_name = None
                        break

            if nick_name != None :
                nick_exe = False
        try:
            os.makedirs(nick_name)
            print(f"'{nick_name}' 폴더가 성공적으로 생성되었습니다.")
        except FileExistsError:
            print(f"'{nick_name}' 폴더는 이미 존재합니다.")
        except Exception as e:
            print(f"폴더를 생성하는 중 오류가 발생했습니다: {e}")
                    
        while(pass_exe) :
            pass_word = input("비밀번호를 입력해주세요 :")
            check_pass_word = input("확인용 비밀번호를 입력해주세요 : ")

            salt = generate_salt()

            pass_word_XOR = generate_key(pass_word, salt)
            print(f"Generated Key: {pass_word_XOR.hex()}")
            check_pass_word_XOR = generate_key(check_pass_word, salt)
            print(f"Generated Key: {check_pass_word_XOR.hex()}")

            if pass_word_XOR != check_pass_word_XOR :
                print("비밀번호가 맞지 않습니다 다시 작성해주세요")

            else :
                pass_exe = False

        print("correct")
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key() 

        iv, encrypt_privat_key = encrypt(private_key, pass_word_XOR)

        # 딕셔너리 생성
        data =  {
                "name" :  nick_name,
                "encrypt_key" : encrypt_privat_key,
                "iv" : iv,
                "salt" : salt
        }

        # 딕셔너리를 JSON 문자열로 변환
        json_data = json.dumps(data, indent=4)

        #JSON 파일 경로 설정
        json_file_path = os.path.join(nick_name, f"{nick_name}.json")

        # JSON 파일 작성 및 저장
        try:
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"JSON 데이터가 '{json_file_path}' 파일에 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f"JSON 파일을 저장하는 중 오류가 발생했습니다: {e}")            
    
        join_data =  {
                'sender' : nick_name, # 송신자
                'recipient' : "master1", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "type" : "join",
                    "user_name" : nick_name,
                    "public_key" : public_key,
                }
            }

        private_key_obj = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key_obj)
        
        join_dataJson = json.dumps(join_data, sort_keys=True)
        contract_Hash = hashlib.sha256(join_dataJson.encode()).hexdigest()
        signed = cipher_rsa.encrypt(contract_Hash)

        join_data["smart_contract"]["contract_Hash"] = contract_Hash
        join_data["smart_contract"]["signed"] = signed

        requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = join_dataJson)

        nick_exe = True
        pass_exe = True

    if select == '2' :
        while(nick_exe) :
            nick_name = input("닉네임을 먼저 입력해주세요 : ")
            current_directory = os.getcwd()

            # "nace" 폴더 경로 생성
            nace_folder_path = os.path.join(current_directory, 'nace')

            # "nace" 폴더가 존재하는지 확인
            if os.path.isdir(nace_folder_path):
                print(f"'{nace_folder_path}' 폴더를 찾았습니다.")
    
                # "nace.json" 파일 경로 생성
                nace_json_path = os.path.join(nace_folder_path, 'nace.json')
    
            # "nace.json" 파일이 존재하는지 확인
                if os.path.isfile(nace_json_path):
                    print(f"'{nace_json_path}' 파일을 찾았습니다.")
        
            # JSON 파일 읽기
                    try:
                        with open(nace_json_path, 'r', encoding='utf-8') as json_file:
                            data = json.load(json_file)
                        print("JSON 파일을 성공적으로 읽어왔습니다.")
                        print(data)  # 파이썬 딕셔너리 출력
                        nick_exe = False
                    except Exception as e:
                        print(f"JSON 파일을 읽는 중 오류가 발생했습니다: {e}")
                else:
                    print(f"'{nace_json_path}' 파일이 존재하지 않습니다.")
            else:
                print(f"'{nace_folder_path}' 폴더가 존재하지 않습니다.")

        while(pass_exe) :
            pass_word = input("비밀번호를 입력해주세요 :")
            encrypt_privat_key = data["encrypt_privat_key"]
            salt = data["salt"]
            iv = data["iv"]

            key = generate_key(pass_word, salt)
            
            privat_key = decrypt(iv, encrypt_privat_key, key)

            get_chain = requests.get("http://localhost:5000/chain", headers=headers)
            transactions = get_chain["chain"] 

            for smart_Contract in transactions :
                smart_Contract = smart_Contract["smart_contract"]
                print(smart_Contract)
                if smart_Contract["type"] == "join" :
                    if smart_Contract["user_name"] == nick_name :
                        message = b'This is a message for encryption'

                        public_key = smart_Contract["public_key"]

                        private_key_obj = RSA.import_key(private_key)
                        cipher_rsa = PKCS1_OAEP.new(private_key_obj)
                        ciphertext = cipher_rsa.encrypt(message)
                        
                        public_key_obj = RSA.import_key(public_key)
                        cipher_rsa = PKCS1_OAEP.new(public_key_obj)
                        decrypted_message = cipher_rsa.decrypt(ciphertext)

                        if decrypted_message == message :
                            print("succes login")
                            pass_exe = False

        login_data =  {
                'sender' : nick_name, # 송신자
                'recipient' : "master1", # 수신자
                'amount' : 0, # 금액
                'timestamp':time.time(),
                'smart_contract' : {
                    "type" : "login",
                    "user_name" : nick_name,
                }
            }

        login_dataJson = json.dumps(login_data, sort_keys=True)
        contract_Hash = hashlib.sha256(login_dataJson.encode()).hexdigest()
        join_data["smart_contract"]["contract_Hash"] = contract_Hash
        join_data["smart_contract"]["singed"] = cipher_rsa.encrypt(contract_Hash)
        requests.post("http://127.0.0.1:5001/transactions/new", headers=headers, data = login_dataJson)

        nick_exe = True
        pass_exe = True
        
    if select == '3' :
        print("블록체인을 가져오고 있습니다 잠시만 기다려 주십시오")
        res = requests.get("http://localhost:5000/chain", headers=headers)
        print(json.loads(res.content))

    elif select == '4' :
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
                "smart_contract": {}
        }

        print('거래내역을 생성중입니다 잠시만 기다려 주십시오')
        res = requests.post("http://localhost:5000/transactions/new", headers=headers, data=json.dumps(data)).content
        print(json.loads(res))
        invaild_transaction = True
