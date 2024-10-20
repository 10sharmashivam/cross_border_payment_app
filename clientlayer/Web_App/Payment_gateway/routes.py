from flask import request, jsonify
from app import app, db
from models import Transaction

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Payment Gateway!"})

# API to process payment
@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.get_json()

    # Extract payment details from the request
    sender = data.get('sender')
    receiver = data.get('receiver')
    amount = data.get('amount')
    currency = data.get('currency')

    # Validate transaction
    if not all([sender, receiver, amount, currency]):
        return jsonify({"error": "Missing required payment details"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    # Simulate processing and create a new transaction
    new_transaction = Transaction(
        sender=sender,
        receiver=receiver,
        amount=amount,
        currency=currency,
        status="Pending"
    )

    # Add to database
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({
        "message": "Payment processed successfully",
        "transaction_id": new_transaction.id,
        "status": new_transaction.status
    }), 201

# API to get all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = []
    for txn in transactions:
        result.append({
            "id": txn.id,
            "sender": txn.sender,
            "receiver": txn.receiver,
            "amount": txn.amount,
            "currency": txn.currency,
            "status": txn.status,
            "timestamp": txn.timestamp
        })
    return jsonify(result)