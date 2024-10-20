from flask import Flask, request, jsonify
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config

app = Flask(__name__)

# Initialize Flyte remote
remote = FlyteRemote(
    Config.for_sandbox(),
    default_project="payment_project",
    default_domain="development"
)

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

if __name__ == '__main__':
    app.run(debug=True)