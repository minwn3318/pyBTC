import hashlib # hash 占쎈맙占쎈땾占쎌뒠 sha256 占쎄텢占쎌뒠占쎈막 占쎌뵬占쎌뵠�뇡�슢�쑎�뵳占�
import json
import time
import random
import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse

class Blockchain(object):
    
    def __init__(self, account_weight, account_name):
        self.chain = []                                   # chain占쎈퓠 占쎈연占쎌쑎 block占쎈굶 占쎈굶占쎈선占쎌긾
        self.current_transaction = []                     # 占쎌뿫占쎈뻻 transaction 占쎄퐫占쎈선餓ο옙
        self.nodes = set()                                # Node 筌뤴뫖以됵옙�뱽 癰귣떯占쏙옙
        self.miner_wallet = {'account_name': account_name, 'weight': account_weight}  # 吏�媛묒젙蹂� �깮�꽦
        self.new_block(previous_hash='genesis_block', address = account_name)        # genesis block �깮�꽦
        self.account_name = account_name
        self.account_weight = account_weight

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(block_string).hexdigest()   # hash 占쎌뵬占쎌뵠�뇡�슢�쑎�뵳�됱쨮 sha256 占쎄텢占쎌뒠
    
    @property
    def last_block(self):
        return self.chain[-1]                             # 筌ｋ똻�뵥占쎌벥 筌띾뜆占쏙옙筌랃옙 �뇡遺얠쨯 揶쏉옙占쎌죬占쎌궎疫뀐옙!!

    @property
    def get_nodeList(self) :
        node_list = []
        for node in self.nodes :
            node_list.append(node)
        return node_list
    
    @property
    def get_transaction(self):
        return  len(self.current_transaction)
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()          # 占쎌읈 proof占쏙옙占� �뤃�뗫막 proof �눧紐꾩쁽占쎈였 占쎈염野껓옙
        guess_hash = hashlib.sha256(guess).hexdigest()    # 占쎌뵠 hash 揶쏉옙 占쏙옙占쏙옙�삢
        return guess_hash[:4] == "0000"                  # 占쎈링 4占쎌쁽�뵳�덌옙占� 0000 占쎌뵠筌롳옙 True (占쎈르筌띿쉸占쏙옙 nonce揶쏅�れ뱽 筌≪뼚�벉)

    def pos(self):
        winner_list = []            # 媛� �끂�뱶�뿉�꽌 pick_winner 寃곌낵 戮묓엺 winner 由ъ뒪�듃
        time.sleep(1)
        my_winner = self.pick_winner(account_name = self.account_name, account_weight = self.account_weight)   
        winner_list.append(my_winner)   # winner 由ъ뒪�듃�뿉 �궡�끂�뱶 寃곌낵 �꽔湲�
        time.sleep(1)

        for target_node in blockchain.nodes:            # �떎瑜� �끂�뱶�뱾�룄 pick_winner 吏꾪뻾 
            print("self pos : ",target_node)
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            res = requests.get('http://' + target_node   + "/nodes/pick_winner", headers=headers)
            winner_info = json.loads(res.content)  # 洹쇱쿂 �끂�뱶�뱾 �꽑�젙寃곌낵 諛쏆븘����꽌
            print(winner_info)
            winner_list.append(winner_info['winner']) 

        final_winner = max(winner_list,key = winner_list.count)  # 媛� �끂�뱶�뱾�쓽 pos 寃곌낵濡� 媛��옣 留롮씠 �꽑�젙�맂 winner瑜� 理쒖쥌 winner 濡� �꽑�젙
        print("final_winner selected : ", final_winner)
        
        return final_winner


    def pick_winner(self,account_name, account_weight):  ### �늻媛��늻媛� 釉붾줉 留뚮뱾�옒!! 留뚮뱾�궗�엺 戮묎린
        candidate_list = []  # POS ����긽�옄瑜� 戮묒쓣 �쟾泥� ���!!
             
        for w in range(account_weight):  # �굹�쓽 �끂�뱶�뱾�쓽 weight �닔留뚰겮 異붽��
            print('self 5000 :', w)
            candidate_list.append(account_name)
       
        random.shuffle(candidate_list)       #  �옖�뜡�쑝濡� �꽎怨�!
        for x in  candidate_list:           #  泥ル쾲吏� node瑜� winner濡� �꽑�젙
            winner  = x
            print("WINNER SELECTED 5000: ", winner)
            break
        
        return winner                       # winner 怨듦컻

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender' : sender, # 占쎈꽊占쎈뻿占쎌쁽
                'recipient' : recipient, # 占쎈땾占쎈뻿占쎌쁽
                'amount' : amount, # 疫뀀뜆釉�
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

    def is_chain_valid(self, chain):           
        last_block = chain['chain'][0]
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
    
    def register_node(self, address): # url 二쇱냼瑜� �꽔寃� �맖
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc) # set �옄猷뚰삎�깭 �븞�뿉 紐⑸줉�쓣 ����옣
        
        
    def resolve_conflict(self):    # �떎瑜몃끂�뱶�뱾�씠�옉 鍮꾧탳�븯硫� 吏�湲덉쓽 �궡 �끂�뱶 �긽�깭媛� �젙�긽�씤吏� 寃�利�
        
        for registering_node in blockchain.nodes:            # 洹쇱쿂 �끂�뱶�뱾�쓽 weight �닔留뚰겮 異붽��
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            print(registering_node,  '    /http://' + registering_node   + "/chain")
            res = requests.get('http://' + registering_node   + "/chain", headers=headers)
            target_node_info = json.loads(res.content)
            
            
            if target_node_info['length'] > len(self.chain):  # �떎瑜몃끂�뱶�쓽 釉붾줉�씠 �궡 �끂�뱶�쓽 釉붾줉蹂대떎 湲멸꼍�슦
                if self.is_chain_valid(target_node_info):     # 洹몃━怨� 洹� �끂�뱶媛� valid �븷 寃쎌슦 
                    self.blockchain = target_node_info        # �궡 �끂�뱶瑜� 洹� �끂�뱶濡� �뜮�뼱�뵆�슦湲�
                    return
        return     
        
my_ip = '127.0.0.1'
my_port = '5000'
node_identifier = 'node_'+my_port
mine_owner = 'master001'
mine_profit = 0.1

blockchain = Blockchain(account_name=mine_owner, account_weight= 2)

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested!!")
    response = {
        'chain' : blockchain.chain, 
        'length' : len(blockchain.chain), 
    }
    return jsonify(response), 200

@app.route('/transaction', methods = ['GET'])
def full_transaction():
    print("transaction info requested!!")
    response = {
        'transaction' : blockchain.current_transaction,
        'length' : blockchain.get_transaction
    }
    return jsonify(response), 200

@app.route('/nodeList', methods = ['GET'])
def full_nodeList():
    print(" info requested!!")
    respones = {
        'node_list' : blockchain.get_nodeList,
        'length' : len(blockchain.get_nodeList)
    }
    return jsonify(respones), 200

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

    if "type" not in values:  ## �떊洹쒕줈 異붽���맂 寃쎌슦 type �씠�씪�뒗 �젙蹂닿�� �룷�븿�릺�뼱 �뾾�떎. �빐�떦 �궡�슜��� �쟾�뙆 �븘�슂
        for node in blockchain.nodes:  # nodes�뿉 ����옣�맂 紐⑤뱺 �끂�뱶�뿉 �젙蹂대�� �쟾�떖�븳�떎.
            headers = {'Content-Type' : 'application/json; charset=utf-8'}
            data = {
                "sender": values['sender'],
                "recipient": values['recipient'],
                "amount": values['amount'],
                "type" : "sharing"   # �쟾�뙆�씠湲곗뿉 sharing�씠�씪�뒗 type �씠 瑗� �븘�슂�븯�떎.
            }
            requests.post("http://" + node  + "/transactions/new", headers=headers, data=json.dumps(data))
            print("share transaction to >>   ","http://" + node )
            
    return jsonify(response), 201

@app.route('/block/new', methods=['POST'])
def new_block():
    block = request.get_json() 
    print("NEW BLOCK  ADDED!!! : ", block)
    
    blockchain.current_transaction = []
    blockchain.chain.append(block) 
    response = {'message' : 'Transaction will be added to Block {%s}' % block['index']}
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

    if final_winner == blockchain.account_name:  # 留뚯빟 蹂� �끂�뱶媛� winner濡� �꽑�젙�릺�뿀�쑝硫� �븘�옒��� 媛숈씠
        print("MY NODE IS SELECTED AS MINER NODE")
        blockchain.new_transaction(           #  �꽑�젙�맂 �끂�뱶�뿉寃� 蹂댁긽�쓣 二쇨퀬
            sender="mining_profit", 
            recipient=final_winner, 
            amount=mine_profit, # coinbase transaction  
        )

        previous_hash = blockchain.hash(blockchain.chain[-1])
        block = blockchain.new_block(previous_hash = previous_hash, address = final_winner)  #  �떊洹� 釉붾줉 �깮�꽦
        print(final_winner," IS SELECTED AS MINER NODE")
    #####
    #�떎瑜몃끂�뱶�뱾�뿉 �쟾�뙆�빐�빞�빐!!!
    #####
    ################### �끂�뱶 �뿰寃곗쓣 �쐞�빐 異붽���릺�뒗 遺�遺�
        for node in blockchain.nodes: # nodes�뿉 �뿰寃곕맂 紐⑤뱺 �끂�뱶�뿉 �옉�뾽利앸챸(PoW)媛� �셿猷뚮릺�뿀�쓬�쓣 �쟾�뙆�븳�떎.
            headers = {'Content-Type' : 'application/json; charset=utf-8'}

            alarm_newBlock = requests.post("http://" + node  + "/block/new", headers=headers, data = json.dumps(blockchain.chain[-1] ) ) 
            print(alarm_newBlock.content)

        response = {
            'message' : 'new block found',
            'index' : block['index'],
            'transactions' : block['transactions'],
            'validator' : block['validator'],
            'previous_hash' : block['previous_hash'],
            'hash' : block['hash']
        }
    
    else : # isWinner = False : 蹂� �끂�뱶媛� winner媛� �븘�떂
        print("MY NODE IS NOT SELECTED AS MINER NODE")
 
    response = {'message' : 'Mining Complete'}
    return jsonify(response), 200

################### �끂�뱶 �뿰寃곗쓣 �쐞�빐 異붽���릺�뒗 �븿�닔 : �떎瑜� Node �벑濡�!
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json() # json �삎�깭濡� 蹂대궡硫� �끂�뱶媛� ����옣�씠 �맖
    print("register nodes !!! : ", values)
    registering_node =  values.get('nodes')
    if registering_node == None: # �슂泥��맂 node 媛믪씠 �뾾�떎硫�! 
        return "Error: Please supply a valid list of nodes", 400
     
    ## �슂泥�諛쏆�� �끂�뱶�뱶�씠 �씠誘� �벑濡앸맂 �끂�뱶��� 以묐났�씤吏� 寃��궗
    ## 以묐났�씤�씤 寃쎌슦
    if registering_node.split("//")[1] in blockchain.nodes:
        print("Node already registered")  # �씠誘� �벑濡앸맂 �끂�뱶�엯�땲�떎.
        response = {
            'message' : 'Already Registered Node',
            'total_nodes' : list(blockchain.nodes),
        }

    ## 以묐났  �븞�릺�뿀�떎硫�
    else:  
        # �궡 �끂�뱶由ъ뒪�듃�뿉 異붽��
        blockchain.register_node(registering_node) 
        
        ## �씠 �썑 �빐�떦 �끂�뱶�뿉 �궡�젙蹂대��  �벑濡앺븯湲�
        headers = {'Content-Type' : 'application/json; charset=utf-8'}
        data = {
            "nodes": 'http://' + my_ip + ":" + my_port
        }
        print("MY NODE INFO " , 'http://' + my_ip + ":" + my_port)
        requests.post( registering_node + "/nodes/register", headers=headers, data=json.dumps(data))
        
        # �씠�썑 二쇰�� �끂�뱶�뱾�뿉�룄 �깉濡쒖슫 �끂�뱶媛� �벑�옣�븿�쓣 �쟾�뙆
        for add_node in blockchain.nodes:
            if add_node != registering_node.split("//")[1]:
                print('add_node : ', add_node)
                ## �끂�뱶 �벑濡앺븯湲�
                headers = {'Content-Type' : 'application/json; charset=utf-8'}
                data = {
                    "nodes": registering_node
                }
                requests.post('http://' + add_node   + "/nodes/register", headers=headers, data=json.dumps(data))

        response = {
            'message' : 'New nodes have been added',
            'total_nodes' : list(blockchain.nodes),
        }
    return jsonify(response), 201

@app.route('/nodes/node_weight', methods=['GET'])
def node_weight():
    print("node_weight requested!!")

    response = {
        'account_name' : blockchain.account_name,
        'account_weight' : blockchain.account_weight
    }
    return jsonify(response), 200    

    
@app.route('/nodes/pick_winner', methods=['GET'])
def pick_winner():
    print("pick_winner requested!!")
    
    candidate_list = []  # POS ����긽�옄瑜� 戮묒쓣 �쟾泥� ���!!
    for w in range(blockchain.account_weight):  # �굹�쓽 �끂�뱶�뱾�쓽 weight �닔留뚰겮 異붽��
        print('route 5000 : ', w)
        candidate_list.append(blockchain.account_name)

    for target_node in blockchain.nodes:            # 洹쇱쿂 �끂�뱶�뱾�쓽 weight �닔留뚰겮 異붽��
        print("route pos:",target_node)
        
        headers = {'Content-Type' : 'application/json; charset=utf-8'}
        res = requests.get('http://' + target_node   + "/nodes/node_weight", headers=headers)
        target_node_info = json.loads(res.content)
                
        for repeated in range(target_node_info['account_weight']):
            print('repeate : ', repeated)
            print('name : ', target_node_info['account_name'])
            candidate_list.append(target_node_info['account_name'])

    random.shuffle(candidate_list)       #  �옖�뜡�쑝濡� �꽎怨�!
    for x in  candidate_list:           #  泥ル쾲吏� node瑜� winner濡� �꽑�젙
        winner  = x
        print("WINNER SELECTED 5000-: ", winner)
        break

    
    response = {
        'winner' : winner, 
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)