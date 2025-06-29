from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

def load_knowledge_base(subject):
    filepath = os.path.join("data", f"{subject}.txt")
    knowledge_base = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    knowledge_base[key.lower()] = value.strip()
    return knowledge_base

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    subject = data.get("subject", "").lower()
    message = data.get("message", "").lower()

    knowledge_base = load_knowledge_base(subject)
    answer = "I don't know the answer to that yet. Please ask something else."

    for keyword in knowledge_base:
        if keyword in message:
            answer = knowledge_base[keyword]
            break

    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(debug=True)
