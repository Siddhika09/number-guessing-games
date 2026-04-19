# app.py
from flask import Flask, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "abc"

@app.route("/start")
def start():
    session["secret"] = random.randint(1, 100)
    return jsonify({"message": "Game started!"})

@app.route("/guess/<int:num>")
def guess(num):
    secret = session.get("secret", 50)
    if num < secret:   return jsonify({"result": "low"})
    elif num > secret: return jsonify({"result": "high"})
    else:              return jsonify({"result": "win"})

app.run(debug=True)