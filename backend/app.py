from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict
import time

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

queues = defaultdict(list)

@app.route('/api/<queue_name>', methods=['POST'])
def post_message(queue_name):
    try:
        message = request.get_json()
        if not message:
            return jsonify({"error": "Invalid JSON body"}), 400
        queues[queue_name].append(message)
        return jsonify({"status": "Message added to queue"}), 201
    except Exception as e:
        return jsonify({"error": "Malformed request", "details": str(e)}), 400

@app.route('/api/<queue_name>', methods=['GET'])
def get_message(queue_name):
    try:
        timeout_ms = request.args.get('timeout', default=10000, type=int)
        if timeout_ms < 0:
            return jsonify({"error": "Timeout must be a positive integer"}), 400

        timeout = timeout_ms / 1000  # Convert milliseconds to seconds
        start_time = time.time()

        if queue_name not in queues:
            return jsonify({"error": f"Queue '{queue_name}' does not exist"}), 404

        while time.time() - start_time < timeout:
            if queues[queue_name]:
                message = queues[queue_name].pop(0)
                return jsonify(message), 200
            time.sleep(0.1)

        return '', 204
    except ValueError as e:
        return jsonify({"error": "Invalid query parameter", "details": str(e)}), 400

@app.route('/api/queues', methods=['GET'])

def get_all_queues():
    return jsonify({queue: len(messages) for queue, messages in queues.items()}), 200

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)
