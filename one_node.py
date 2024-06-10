import hashlib # hash �븿�닔�슜 sha256 �궗�슜�븷 �씪�씠釉뚮윭由�
import json
import time
import random
import requests
from flask import Flask, request, jsonify

class Blockchain(object):
    
    def __init__(self, account_weight, account_name):
        self.chain = []                                   # chain�뿉 �뿬�윭 block�뱾 �뱾�뼱�샂
        self.current_transaction = []                     # �엫�떆 transaction �꽔�뼱以�
        self.nodes = set()                                # Node 紐⑸줉�쓣 蹂닿��
        self.miner_wallet = {'account_name': account_name, 'weight': account_weight}  # 지갑정보 생성
        self.new_block(previous_hash='genesis_block', address = account_name)        # genesis block 생성
        self.account_name = account_name
        self.account_weight = account_weight

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(block_string).hexdigest()   # hash �씪�씠釉뚮윭由щ줈 sha256 �궗�슜
    @property
    def last_block(self):
        return self.chain[-1]                             # 泥댁씤�쓽 留덉��留� 釉붾줉 媛��졇�삤湲�!!

    @property
    def get_transaction(self):
        return  len(self.current_transaction)
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()          # �쟾 proof��� 援ы븷 proof 臾몄옄�뿴 �뿰寃�
        guess_hash = hashlib.sha256(guess).hexdigest()    # �씠 hash 媛� ����옣
        return guess_hash[:4] == "0000"                  # �븵 4�옄由ш�� 0000 �씠硫� True (�븣留욎�� nonce媛믪쓣 李얠쓬)

    def pos(self):
        winner_list = []            # 각 노드에서 pick_winner 결과 뽑힌 winner 리스트
        time.sleep(1)
        my_winner = self.pick_winner(account_name = self.account_name, account_weight = self.account_weight)   
        winner_list.append(my_winner)   # winner 리스트에 내노드 결과 넣기
        time.sleep(1)

        for target_node in blockchain.nodes:            # 다른 노드들도 pick_winner 진행 
            print(target_node)
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            res = requests.get('http://' + target_node   + "/nodes/pick_winner", headers=headers)
            winner_info = json.loads(res.content)  # 근처 노드들 선정결과 받아와서
            print(winner_info)
            winner_list.append(winner_info['winner']) 

        final_winner = max(winner_list,key = winner_list.count)  # 각 노드들의 pos 결과로 가장 많이 선정된 winner를 최종 winner 로 선정
        print("final_winner selected : ", final_winner)
        
        return final_winner

    def pick_winner(self,account_name, account_weight):  ### 누가누가 블록 만들래!! 만들사람 뽑기
        candidate_list = []  # POS 대상자를 뽑을 전체 풀!!
             
        for w in range(account_weight):  # 나의 노드들의 weight 수만큼 추가
            candidate_list.append(account_name)
       
        random.shuffle(candidate_list)       #  랜덤으로 섞고!
        for x in  candidate_list:           #  첫번째 node를 winner로 선정
            winner  = x
            print("WINNER SELECTED : ", winner)
            break
        
        return winner                       # winner 공개

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender' : sender, # �넚�떊�옄
                'recipient' : recipient, # �닔�떊�옄
                'amount' : amount, # 湲덉븸
                'timestamp':time.time()
            }
        )
        return self.last_block['index'] + 1   

    def new_block(self, previous_hash=None, address = ''):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : time.time(), # timestamp from 1970
            'transactions' : self.current_transaction,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
            'validator' : address
        }
        block["hash"] = self.hash(block)
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
            last_block = block
            current_index += 1
        return True
    
my_ip = '0.0.0.0'
my_port = '5000'
node_identifier = 'node_'+my_port
mine_owner = 'master'
mine_profit = 0.1

blockchain = Blockchain(account_name=mine_owner, account_weight= 100)

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
    required = ['sender', 'recipient', 'amount'] 

    if not all(k in values for k in required):
        print('error')
        return 'missing values', 400

    index = blockchain.new_transaction(values['sender'],values['recipient'],
values['amount'])
        
    response = {'message' : 'Transaction will be added to Block {%s}' % index}
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    transaction_len = blockchain.get_transaction
    if transaction_len == 0 :
        response = {
            'message' : 'No transaction in node. Need making transaction ',
            'transactions length' : transaction_len
        }
        return jsonify(response), 200
    
    print("MINING STARTED")   
    final_winner = blockchain.pos()  

    if final_winner == blockchain.account_name:  # 만약 본 노드가 winner로 선정되었으면 아래와 같이
 

        blockchain.new_transaction(
            sender=mine_owner, 
            recipient=node_identifier, 
            amount=mine_profit # coinbase transaction 
        )

        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(previous_hash, address= mine_owner)
        print("MINING FINISHED")

        response = {
            'message' : 'new block found',
            'index' : block['index'],
            'nonce' : block['validator'],
            'transactions' : block['transactions'],
            'previous_hash' : block['previous_hash']
        }
          
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)