from flask import Blueprint, jsonify, request
from models import db, Transaction

payment_routes = Blueprint('payments', __name__)

@payment_routes.route('/status/<transaction_id>', methods=['GET'])
def check_status(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        return jsonify({'status': transaction.status})
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@payment_routes.route('/history/<user_id>', methods=['GET'])
def payment_history(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    if transactions:
        return jsonify([t.as_dict() for t in transactions])
    else:
        return jsonify({'error': 'No transactions found for user'}), 404