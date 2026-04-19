from flask import Flask, request, jsonify, session
from flask_cors import CORS
import random

app = Flask(__name__)
app.secret_key = "guessing123"
CORS(app, supports_credentials=True, origins="*")

@app.route("/start")
def start():
    session["secret"] = random.randint(1, 100)
    session["attempts"] = 0
    return jsonify({"message": "Game started! Guess a number between 1 and 100."})

@app.route("/guess/<int:num>")
def guess(num):
    if "secret" not in session:
        return jsonify({"result": "error", "message": "Start the game first!"})

    session["attempts"] += 1
    secret = session["secret"]
    attempts = session["attempts"]

    if num < 1 or num > 100:
        return jsonify({"result": "error", "message": "Enter a number between 1 and 100!"})
    elif num < secret:
        return jsonify({"result": "low",  "message": f"📈 Too Low! Try higher. (Attempt {attempts})"})
    elif num > secret:
        return jsonify({"result": "high", "message": f"📉 Too High! Try lower. (Attempt {attempts})"})
    else:
        return jsonify({"result": "win",  "message": f"🎉 Correct! The number was {secret}. You got it in {attempts} attempts!"})

if __name__ == "__main__":
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True)