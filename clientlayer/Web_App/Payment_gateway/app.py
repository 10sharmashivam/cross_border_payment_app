from flask import Flask, request, jsonify, render_template
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from blockchain_layer.blockchain import Blockchain

app = Flask(__name__)

# Initialize Flyte remote connection
remote = FlyteRemote(
    Config.for_sandbox(),
    default_project="payment_project",
    default_domain="development"
)

# Initialize Blockchain
blockchain = Blockchain()

@app.route('/')
def home():
    return "Welcome to Cross Border Payment App system"
# render_template('index.html')

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    try:
        # Call Flyte workflow for payment processing
        execution = remote.execute(
            remote.fetch_workflow('payment_processing', 'payment_workflow'),
            inputs={'transaction_data': data}
        )
        result = remote.wait(execution)
        return jsonify({"status": "success", "result": result.outputs['status']})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0", recipient="node_address", amount=1)
    block = blockchain.new_block(proof)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)