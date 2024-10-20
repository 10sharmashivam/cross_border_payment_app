from flytekit import task, workflow

@task
def detect_fraud(transaction_data: dict) -> bool:
    # Placeholder for fraud detection logic (e.g., using AI/ML)
    # For now, just a simple rule to detect fraud
    return transaction_data['amount'] > 10000  # Flag as fraud if amount > 10k

@workflow
def fraud_detection_workflow(transaction_data: dict) -> bool:
    return detect_fraud(transaction_data)