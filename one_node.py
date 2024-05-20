import hashlib
from flask import Flask, request, jsonify
import json
from time import time
import random

class Blockchain(object):
    def __init__(self) :
        self.chain = []
        self.current_transaction = []
        self.node = set()
        self.new_block(previous_hash=1, proof=100)
        
    @staticmethod
    def hsah(block) :
        block_string = json.dump(block, sort_keys=True).encode()
        return hsahslib.sha256(block_string).hexdigest()

    @property
    def last_block(self) :
        return self.chain[-1]

    @staticmethod
    def valid_proof(last_proof, proof) :
        guess = str(last_proof + proof).encode()
        guess_hsah = hashlib.sha256(guess).hexdiest()
        return guess_hsah[:4] == "0000"

    def pow(self, last_proof) :
        proof = random.randint(-1000000, 1000000)
        while self.valid_proof(last_proof, proof) is False :
            proof = random.randint(-1000000, 1000000)
        return proof

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender' : sender,
                'recipient' : recipient,
                'amount' : amount,
                'timestama' : time()
            }
        )
        return self.last_block['index'] + 1

    def new_block(self, proof, previous_hash = None):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : time(),
            'transactions' : self.current_transaction,
            'nonce' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }
        self.current_transaction = []
        self.chain.append(block)
        return block

    def valid_chain(self, chain) :
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain) :
            block = chain[current_index]
            print('%s' % last_block)
            print('%s' % block)
            print("\n-------\n")
            if(block['previous_hash'] != self.hash(last_block)) :
               return False
            last_block = block
            current_index += 1
        return True

blockchain = Blockchain()
my_ip = '0.0.0.0'
my_port = '5000'
node_identifier = 'node_' + my_port
mine_owner = 'master'
mine_profit = 0.1

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    print("chain info requested!")
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction() :
    values = request.get_json()
    print("transactions_new!!! : ", values)
    required = ['sender', 'recipient', 'amount']

    if not all(k in vlaues for k in required) :
        return 'missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'],
                                       values['amount'])
    response = {'mesage' : 'Transaction will be added to Blcok {%s}' % index}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    print("MINING STARTED")
    last_block = blockchain.last_block
    last_proot = last_block['nonce']
    proof = blockchain.pow(last_proof)
    blockchain.new_transaction(
        sender=mine_owner,
        recipient=node_idnetifier,
        amount=mine_profit
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    print("MINING FINSHED")

    response = {
            'message' : 'new block found',
            'index' : block['index'],
            'transactions' : block['transactions'],
            'nonce' : block['nonce'],
            'previous_hash' : block['previous_hash']   
        }

    return jsonify(response), 200

if __name__ == '__main__' :
    app.run(host=my_ip, port=my_port)
