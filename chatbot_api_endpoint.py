from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from Chain.inference_endpoint import llm_inference_endpoint

app = Flask(__name__)
CORS(app)
model_endpoint = llm_inference_endpoint()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    user_question = data["question"]

    def generate():
        # Stream tokens from the model endpoint.
        # Option A: Just yield tokens as plain text
        for token in model_endpoint.stream(user_question):
            # If needed, you can process token formatting here.
            # For a simple text stream:
            yield token
            # Option B: For an SSE-like format, do:
            # yield f"data: {token}\n\n"

    # Use a plain text MIME type or "text/event-stream" for SSE
    return Response(generate(), mimetype='text/plain')  # Or "text/event-stream" if using SSE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
