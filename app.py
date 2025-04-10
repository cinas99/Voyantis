from flask import Flask, request, jsonify
import time
from collections import defaultdict

app = Flask(__name__)

# In-memory storage for queues
queues = defaultdict(list)

# try commit

@app.route('/api/<queue_name>', methods=['POST'])
def post_message(queue_name):
    message = request.get_json()
    if not message:
        return jsonify({"error": "Message body is required"}), 400
    queues[queue_name].append(message)
    return jsonify({"status": "Message added to queue"}), 201

@app.route('/api/<queue_name>', methods=['GET'])
def get_message(queue_name):
    timeout = request.args.get('timeout', default=10, type=int)
    start_time = time.time()

    while time.time() - start_time < timeout:
        if queues[queue_name]:
            message = queues[queue_name].pop(0)
            return jsonify(message), 200
        time.sleep(0.1)  # Avoid busy waiting

    return '', 204  # No content if timeout elapses

if __name__ == '__main__':
    app.run(debug=True)