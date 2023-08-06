import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash=0)
        self.nodes = set()

    def create_block(self, previous_hash):
        proof, hash_val = self.proof_of_work(previous_hash)

        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transaction': self.transactions,
                 'hash': hash_val}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_hash):
        new_proof = 1
        block = str(previous_hash) + str(len(self.chain) + 1) + str(datetime.datetime.now()) + str(new_proof) + str(self.transactions)
        encoded_block = json.dumps(block, sort_keys=True).encode()
        hash_val = hashlib.sha256(encoded_block).hexdigest()
        while hash_val[:2] != "00":
            new_proof += 1
            block = str(previous_hash) + str(len(self.chain) + 1) + str(datetime.datetime.now()) + str(new_proof) + str(
                self.transactions)
            encoded_block = json.dumps(block, sort_keys=True).encode()
            hash_val = hashlib.sha256(encoded_block).hexdigest()
        return new_proof, hash_val

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        # print("\nchain: ",chain)
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            print("\n\nblock: ", block)
            if block['previous_hash'] != previous_block['hash']:
                return False
            b_hash = block['hash']
            if b_hash[:2] != "00":
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1


app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    # print(previous_block)
    previous_hash = previous_block['hash']
    # print(previous_hash)
    block = blockchain.create_block(previous_hash)
    response = {'message': 'block is mined',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'hash': block['hash'],
                'transaction': block['transaction']}
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {}
    if is_valid:
        response = {'message': 'Your chain is valid'}
    else:
        repsone = {'message': 'Your chain is not valid'}
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements are missing', 400
    index = blockchain.add_transaction(json['sender'],
                                       json['receiver'],
                                       json['amount'])
    response = {'Message': f'The Transaction is added to block {index}'}
    return jsonify(response), 201

app.run(host='0.0.0.0', port=5000)
