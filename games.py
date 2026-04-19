from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

secret_number = None
attempts = 0
guess_history = []

html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>Number Guessing Game</title>
  <style>
    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #667eea, #764ba2);
    }

    .box {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(10px);
      padding: 30px;
      border-radius: 15px;
      width: 360px;
      text-align: center;
      color: white;
      box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }

    h2 {
      margin-bottom: 10px;
    }

    input {
      padding: 12px;
      width: 75%;
      border-radius: 8px;
      border: none;
      text-align: center;
      font-size: 16px;
      margin-bottom: 10px;
    }

    button {
      padding: 12px;
      width: 100%;
      border: none;
      border-radius: 8px;
      margin-bottom: 10px;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
    }

    button:hover {
      transform: scale(1.05);
      opacity: 0.9;
    }

    #startBtn {
      background: #00c9a7;
      color: white;
    }

    #guessBtn {
      background: #ff7a18;
      color: white;
    }

    #message {
      margin-top: 10px;
      padding: 10px;
      border-radius: 8px;
      font-weight: bold;
      transition: 0.3s;
    }

    .low { background: rgba(0, 150, 255, 0.2); }
    .high { background: rgba(255, 50, 50, 0.2); }
    .win { background: rgba(0, 255, 150, 0.3); }
    .error { background: rgba(255, 200, 0, 0.3); }

    #attempts {
      margin-top: 10px;
      font-weight: bold;
    }

    #historyBox {
      margin-top: 15px;
      text-align: left;
      max-height: 120px;
      overflow-y: auto;
    }

    #historyList {
      list-style: none;
      padding: 0;
    }

    #historyList li {
      background: rgba(255,255,255,0.2);
      margin: 5px 0;
      padding: 6px;
      border-radius: 6px;
      text-align: center;
    }
  </style>
</head>

<body>

<div class="box">
  <h2>🎯 Guess the Number</h2>

  <button id="startBtn" onclick="startGame()">Start Game</button>

  <input type="number" id="guessInput" placeholder="Enter 1-100" disabled>
  <button id="guessBtn" onclick="makeGuess()" disabled>Guess</button>

  <p id="attempts">Attempts: 0</p>
  <div id="message"></div>

  <div id="historyBox">
    <b>📜 History</b>
    <ul id="historyList"></ul>
  </div>
</div>

<script>
async function startGame() {
  const res = await fetch("/start");
  const data = await res.json();

  document.getElementById("guessInput").disabled = false;
  document.getElementById("guessBtn").disabled = false;

  document.getElementById("attempts").innerText = "Attempts: 0";
  document.getElementById("historyList").innerHTML = "";

  showMessage(data.message, "low");
}

async function makeGuess() {
  const num = document.getElementById("guessInput").value;

  if (!num) {
    showMessage("Enter a number!", "error");
    return;
  }

  const res = await fetch("/guess/" + num);
  const data = await res.json();

  showMessage(data.message, data.result);

  document.getElementById("attempts").innerText =
    "Attempts: " + data.attempts;

  const list = document.getElementById("historyList");
  list.innerHTML = "";

  data.history.forEach(g => {
    const li = document.createElement("li");
    li.innerText = "👉 " + g;
    list.appendChild(li);
  });

  if (data.result === "win") {
    document.getElementById("guessInput").disabled = true;
    document.getElementById("guessBtn").disabled = true;
  }

  document.getElementById("guessInput").value = "";
}

function showMessage(text, type) {
  const msg = document.getElementById("message");
  msg.innerText = text;
  msg.className = type;
}
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(html_code)


@app.route("/start")
def start_game():
    global secret_number, attempts, guess_history
    secret_number = random.randint(1, 100)
    attempts = 0
    guess_history = []

    return jsonify({
        "message": "Game started! Guess wisely 😎",
        "attempts": attempts,
        "history": guess_history
    })


@app.route("/guess/<int:num>")
def guess(num):
    global secret_number, attempts, guess_history

    attempts += 1
    guess_history.append(num)

    if num < secret_number:
        return jsonify({
            "message": "Too low! 🔼",
            "result": "low",
            "attempts": attempts,
            "history": guess_history
        })

    elif num > secret_number:
        return jsonify({
            "message": "Too high! 🔽",
            "result": "high",
            "attempts": attempts,
            "history": guess_history
        })

    else:
        return jsonify({
            "message": f"🎉 You won in {attempts} attempts!",
            "result": "win",
            "attempts": attempts,
            "history": guess_history
        })


if __name__ == "__main__":
    app.run(debug=True)