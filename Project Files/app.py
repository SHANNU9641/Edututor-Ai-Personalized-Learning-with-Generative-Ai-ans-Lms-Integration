from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

TOGETHER_API_KEY = "8a5404da53371b1d283c57d291a9e1231ac506480dcd83eb77a7e39028e95e64"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}"
    }
    json_data = {
        "model": TOGETHER_MODEL,
        "prompt": f"You are an educational chatbot. Answer clearly:\n\n{user_input}\n\nAnswer:",
        "max_tokens": 200,
        "temperature": 0.7
    }
    res = requests.post("https://api.together.ai/v1/completions", headers=headers, json=json_data)

    if res.status_code == 200:
        reply = res.json().get("choices", [{}])[0].get("text", "Sorry, no response.")
    else:
        reply = f"Error: {res.status_code}"

    return jsonify({"response": reply.strip()})

if __name__ == "__main__":
    app.run(debug=True)


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"response": "⚠️ No file uploaded."})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"response": "⚠️ Empty filename."})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Simulate summary for now
    return jsonify({"response": f"📄 Received '{filename}' and processing..."})
