from flytekit import task, workflow

@task
def validate_transaction(transaction_data: dict) -> bool:
    # Logic for validating transaction (e.g., checking transaction details)
    return transaction_data['amount'] > 0

@task
def process_transaction(transaction_data: dict) -> str:
    # Process the transaction and return the result
    if validate_transaction(transaction_data):
        return "success"
    else:
        return "failed"

@workflow
def payment_workflow(transaction_data: dict) -> str:
    # Flyte workflow for payment processing
    return process_transaction(transaction_data)