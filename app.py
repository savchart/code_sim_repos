from flask import Flask, request, jsonify
import json
from index_repos import check_similarity, extract_token_names

app = Flask(__name__)

@app.route('/check_similarity', methods=['POST'])
def check_similarity_api():
    input_code = request.form.get('code')
    if not input_code:
        return jsonify({"error": "Code is required"}), 400

    with open("inverted_index.json", "r") as f:
        inverted_index = json.load(f)

    with open("temp_code.py", "w") as f:
        f.write(input_code)

    similar_file = check_similarity("temp_code.py", inverted_index)

    if similar_file:
        return jsonify({"result": "similar", "file": similar_file})
    else:
        return jsonify({"result": "OK"})

if __name__ == '__main__':
    app.run(debug=True)
