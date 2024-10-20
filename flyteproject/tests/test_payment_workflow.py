from flytekit.remote import FlyteRemote
from flytekit.configuration import Config

# Initialize Flyte remote connection
remote = FlyteRemote(
    Config.for_sandbox(),
    default_project="payment_project",
    default_domain="development"
)

def test_payment_workflow():
    # Simulate a payment request for testing
    transaction_data = {
        "user_id": "12345",
        "amount": 150.0,
        "currency": "USD"
    }

    # Execute the workflow directly for testing
    execution = remote.execute(
        remote.fetch_workflow('payment_processing', 'payment_workflow'),
        inputs={'transaction_data': transaction_data}
    )

    # Wait for the workflow to finish and fetch results
    result = remote.wait(execution)
    assert result.outputs['status'] == "success"
    print("Test Passed: Payment Workflow executed successfully!")

if __name__ == "__main__":
    test_payment_workflow()