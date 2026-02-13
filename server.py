from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading
import requests
import os

app = Flask(__name__)
CORS(app)

messages_db = {}
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

def auto_ping():
    """Дилда"""
    while True:
        time.sleep(600)
        if RENDER_URL:
            try:
                requests.get(RENDER_URL)
            except Exception:
                pass

if RENDER_URL:
    threading.Thread(target=auto_ping, daemon=True).start()

@app.route('/')
def index():
    """Проверка"""
    return "N-Rok Online", 200

@app.route('/send', methods=['POST'])
def send_message():
    """Хуй"""
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    
    target = data.get('to')
    sender = data.get('sender')
    content = data.get('content')
    sender_name = data.get('sender_name', 'User')

    if not target or not content:
        return jsonify({"error": "Missing fields"}), 400

    if target not in messages_db:
        messages_db[target] = []

    new_msg = {
        "sender": sender,
        "sender_name": sender_name,
        "content": content,
        "time": time.strftime("%H:%M")
    }
    
    messages_db[target].append(new_msg)
    
    if len(messages_db[target]) > 100:
        messages_db[target].pop(0)

    return jsonify({"status": "sent"}), 200

@app.route('/get/<token>', methods=['GET'])
def get_messages(token):
    """Выдача"""
    msgs = messages_db.pop(token, [])
    return jsonify({"messages": msgs}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
