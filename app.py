from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

conversation_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    messages = [
        {
            "role": "system",
            "content": "You are Sudais AI, a helpful assistant created by Hafiz Sudais Ismail, a CS student at ITU Lahore. Keep replies concise and friendly."
        }
    ] + conversation_history
    
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
    
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })
    
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)