import hashlib
import time
import json
from flask import Flask, request

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, transactions, proof):
    value = str(index) + str(previous_hash) + str(timestamp) + str(transactions) + str(proof)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def proof_of_work(previous_proof):
    new_proof = 0
    while not valid_proof(previous_proof, new_proof):
        new_proof += 1
    return new_proof

def valid_proof(previous_proof, new_proof):
    guess = f'{previous_proof}{new_proof}'.encode('utf-8')
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"  # Adjust the difficulty by changing the number of leading zeros

# Flask web server
app = Flask(__name__)

blockchain = []
transactions = []

@app.route('/mine', methods=['GET'])
def mine():
    global blockchain, transactions

    # Mine a new block
    previous_block = blockchain[-1]
    previous_proof = previous_block.proof
    proof = proof_of_work(previous_proof)

    # Create a new transaction for the mining reward
    transactions.append({'sender': '0', 'recipient': 'miner_address', 'amount': 1})

    new_block = Block(
        index=len(blockchain) + 1,
        previous_hash=previous_block.hash,
        timestamp=time.time(),
        transactions=list(transactions),
        proof=proof,
        hash=calculate_hash(len(blockchain) + 1, previous_block.hash, time.time(), transactions, proof)
    )

    # Reset the list of transactions
    transactions = []

    blockchain.append(new_block)

    response = {
        'message': 'New Block mined successfully',
        'index': new_block.index,
        'hash': new_block.hash,
        'previous_hash': new_block.previous_hash,
        'timestamp': new_block.timestamp,
        'transactions': new_block.transactions,
        'proof': new_block.proof
    }
    return json.dumps(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    global transactions
    data = request.get_json()

    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in data for field in required_fields):
        return 'Missing fields', 400

    transactions.append({
        'sender': data['sender'],
        'recipient': data['recipient'],
        'amount': data['amount']
    })

    return 'Transaction added to the block', 201

@app.route('/chain', methods=['GET'])
def get_chain():
    global blockchain
    response = {
        'chain': [block.__dict__ for block in blockchain],
        'length': len(blockchain)
    }
    return json.dumps(response), 200

if __name__ == '__main__':
    # Create the genesis block
    genesis_block = Block(1, '1', time.time(), [], 0, calculate_hash(1, '1', time.time(), [], 0))
    blockchain.append(genesis_block)

    # Run the Flask web server
    app.run(port=5000)
