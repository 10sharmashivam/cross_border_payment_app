from flytekit import task, workflow

@task
def validate_transaction(transaction_data: dict) -> bool:
    # Logic for validating transaction
    return True if transaction_data['amount'] > 0 else False

@task
def process_payment(transaction_data: dict) -> str:
    # Placeholder logic for processing payments
    if validate_transaction(transaction_data):
        return "success"
    else:
        return "failed"

@workflow
def payment_workflow(transaction_data: dict) -> str:
    # Payment processing Flyte workflow
    return process_payment(transaction_data)