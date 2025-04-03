from flask import Flask, request, jsonify
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
    response = model_endpoint.invoke(user_question)
    return jsonify({"answer": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
