from flask import Flask, render_template, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = "sudais-ai-secret-key-2026"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if "history" not in session:
        session["history"] = []

    session["history"].append({
        "role": "user",
        "content": user_message
    })

    messages = [
        {
            "role": "system",
            "content": "You are Sudais AI, a helpful assistant created by Hafiz Sudais Ismail, a CS student at ITU Lahore. Keep replies concise and friendly."
        }
    ] + session["history"]

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages
        }
    )

    reply = response.json()["choices"][0]["message"]["content"]

    session["history"].append({
        "role": "assistant",
        "content": reply
    })

    session.modified = True
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)