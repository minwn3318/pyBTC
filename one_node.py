import hashlib # hash 함수용 sha256 사용할 라이브러리
import json
import time
import datetime
import random
import requests
from flask import Flask, request, jsonify

class Blockchain(object):
    
    def __init__(self):
        self.chain = []                                   # chain에 여러 block들 들어옴
        self.current_transaction = []                     # 임시 transaction 넣어줌
        self.nodes = set()                                # Node 목록을 보관
        self.new_block(previous_hash=1, proof=100)        # genesis block 생성

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(block_string).hexdigest()   # hash 라이브러리로 sha256 사용
    @property
    def last_block(self):
        return self.chain[-1]                             # 체인의 마지막 블록 가져오기!!

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()          # 전 proof와 구할 proof 문자열 연결
        guess_hash = hashlib.sha256(guess).hexdigest()    # 이 hash 값 저장
        return guess_hash[:4] == "0000"                  # 앞 4자리가 0000 이면 True (알맞은 nonce값을 찾음)

    def pow(self, last_proof):
        proof = random.randint(-1000000,1000000)
        while self.valid_proof(last_proof, proof) is False: # valid proof 함수 활용(아래 나옴), 맞을 때까지 반복적으로 검증
            proof = random.randint(-1000000,1000000)
        return proof

    def new_transaction(self, sender, recipient, amount, smart_contract):
        self.current_transaction.append(
            {
                'sender' : sender, # 송신자
                'recipient' : recipient, # 수신자
                'amount' : amount, # 금액
                'timestamp':time.time(),
                'smart_contract' : smart_contract
            }
        )
        return self.last_block['index'] + 1   

    def new_block(self, proof, previous_hash=None):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : time.time(), # timestamp from 1970
            'transactions' : self.current_transaction,
            'nonce' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }
        block['hash'] = self.hash(block)
        self.current_transaction = []
        self.chain.append(block)     
        return block

    def valid_chain(self, chain):
        last_block = chain[0] 
        current_index = 1

        while current_index < len(chain): 
            block = chain[current_index]
            print('%s' % last_block)
            print('%s' % block)
            print("\n--------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False
            block_copy = block.copy()
            block_copy.pop('hash')
            if block['hash'] != self.hash(block_copy) :
                return False
            last_block = block
            current_index += 1
        return True
    
blockchain = Blockchain()
my_ip = '0.0.0.0'
my_port = '5000'
node_identifier = 'node_'+my_port
mine_owner = 'master'
mine_profit = 0.1

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested!!")
    response = {
        'chain' : blockchain.chain, 
        'length' : len(blockchain.chain), 
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json() 
    print("transactions_new!!! : ", values)
    required = ['sender', 'recipient', 'amount', 'smart_contract'] 

    if not all(k in values for k in required):
        return 'missing values', 400

    contract_address = hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()
    values['smart_contract']['contract_address'] = contract_address

    index = blockchain.new_transaction(values['sender'],values['recipient'],
values['amount'], values['smart_contract'])
        
    response = {'message' : 'Transaction will be added to Block {%s}' % index}
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    print("MINING STARTED")    
    last_block = blockchain.last_block
    last_proof = last_block['nonce']
    proof = blockchain.pow(last_proof)  

    blockchain.new_transaction(
        sender=mine_owner, 
        recipient=node_identifier, 
        amount=mine_profit, # coinbase transaction 
        smart_contract= {'contract_address' : 0}
    )
 
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    print("MINING FINISHED")

    response = {
        'message' : 'new block found',
        'index' : block['index'],
        'transactions' : block['transactions'],
        'nonce' : block['nonce'],
        'previous_hash' : block['previous_hash'],
        'hash' : block['hash']
    }
          
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)