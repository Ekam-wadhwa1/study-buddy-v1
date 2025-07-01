from flask import Flask, request, render_template, jsonify
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = Flask(__name__)

# Load knowledge bases from files
def load_knowledge(file_path):
    knowledge = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ":" in line:
                key, val = line.strip().split(":", 1)
                knowledge[key.lower()] = val.strip()
    return knowledge

knowledge_bases = {
    "physics": load_knowledge(os.path.join("data", "physics.txt")),
    "chemistry": load_knowledge(os.path.join("data", "chemistry.txt")),
    "biology": load_knowledge(os.path.join("data", "biology.txt")),
}

# Load T5 model and tokenizer for paraphrasing
tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")
model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws")

# Function to paraphrase using T5
def paraphrase(text):
    text = "paraphrase: " + text + " </s>"
    encoding = tokenizer.encode_plus(text, padding="max_length", return_tensors="pt", max_length=256, truncation=True)
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_masks,
        max_length=256,
        do_sample=True,
        top_k=120,
        top_p=0.95,
        early_stopping=True,
        num_return_sequences=1
    )
    paraphrased = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return paraphrased

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("message", "").lower()
    subject = data.get("subject", "physics").lower()

    answer = "I don't know the answer to that yet. Please ask something else."
    knowledge_base = knowledge_bases.get(subject, {})

    for keyword in knowledge_base:
        if keyword in question:
            base_answer = knowledge_base[keyword]
            answer = paraphrase(base_answer)
            break

    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(debug=True)
