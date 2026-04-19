from flask import Flask, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "guessing123"

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Number Guessing Game</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f0f4f8;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .box {
      background: white;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      width: 350px;
      text-align: center;
    }
    h1 { color: #2c3e50; margin-bottom: 5px; }
    p.sub { color: #888; font-size: 13px; margin-bottom: 20px; }
    input {
      width: 70%;
      padding: 10px;
      font-size: 16px;
      border: 2px solid #ddd;
      border-radius: 6px;
      text-align: center;
      outline: none;
      margin-bottom: 12px;
    }
    input:focus { border-color: #3498db; }
    .btn {
      display: block;
      width: 100%;
      padding: 10px;
      font-size: 15px;
      font-weight: bold;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-bottom: 8px;
    }
    #guessBtn { background: #3498db; color: white; }
    #guessBtn:hover { background: #2980b9; }
    #startBtn { background: #2ecc71; color: white; }
    #startBtn:hover { background: #27ae60; }
    #message {
      margin-top: 16px;
      padding: 12px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: bold;
      display: none;
    }
    .low   { background: #eaf4fb; color: #2980b9; }
    .high  { background: #fdecea; color: #e74c3c; }
    .win   { background: #e8f8f0; color: #27ae60; }
    .error { background: #fff3cd; color: #856404; }
  </style>
</head>
<body>
<div class="box">
  <h1>Number Guessing Game</h1>
  <p class="sub">Python is picking the number!</p>

  <button class="btn" id="startBtn" onclick="startGame()">Start New Game</button>

  <input type="number" id="guessInput" placeholder="Enter 1-100" min="1" max="100" disabled />
  <button class="btn" id="guessBtn" onclick="makeGuess()" disabled>Guess</button>

  <div id="message"></div>
</div>

<script>
  async function startGame() {
    const res  = await fetch("/start");
    const data = await res.json();
    showMessage(data.message, "low");
    document.getElementById("guessInput").disabled = false;
    document.getElementById("guessBtn").disabled   = false;
    document.getElementById("guessInput").value    = "";
    document.getElementById("guessInput").focus();
  }

  async function makeGuess() {
    const num = document.getElementById("guessInput").value;
    if (!num) { showMessage("Please enter a number!", "error"); return; }

    const res  = await fetch("/guess/" + num);
    const data = await res.json();
    showMessage(data.message, data.result);

    if (data.result === "win") {
      document.getElementById("guessInput").disabled = true;
      document.getElementById("guessBtn").disabled   = true;
    }
    document.getElementById("guessInput").value = "";
    document.getElementById("guessInput").focus();
  }

  function showMessage(text, type) {
    const msg = document.getElementById("message");
    msg.innerText     = text;
    msg.className     = type;
    msg.style.display = "block";
  }

  document.getElementById("guessInput").addEventListener("keydown", function(e) {
    if (e.key === "Enter") makeGuess();
  });
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/start")
def start():
    session["secret"]   = random.randint(1, 100)
    session["attempts"] = 0
    return jsonify({"message": "Game started! Guess a number between 1 and 100."})

@app.route("/guess/<int:num>")
def guess(num):
    if "secret" not in session:
        return jsonify({"result": "error", "message": "Click Start New Game first!"})

    session["attempts"] += 1
    secret   = session["secret"]
    attempts = session["attempts"]

    if num < 1 or num > 100:
        return jsonify({"result": "error", "message": "Enter a number between 1 and 100!"})
    elif num < secret:
        return jsonify({"result": "low",  "message": f"Too Low! Try higher. (Attempt {attempts})"})
    elif num > secret:
        return jsonify({"result": "high", "message": f"Too High! Try lower. (Attempt {attempts})"})
    else:
        return jsonify({"result": "win",  "message": f"Correct! The number was {secret}. You got it in {attempts} attempts!"})

if __name__ == "__main__":
    print("Open this in your browser --> http://127.0.0.1:5000")
    app.run(debug=True)