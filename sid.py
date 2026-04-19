from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

secret_number = None
attempts = 0
guess_history = []

# HTML inside Python
html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>Number Guessing Game</title>
  <style>
    body {
      font-family: Arial;
      background: #f0f4f8;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .box {
      background: white;
      padding: 30px;
      border-radius: 10px;
      width: 350px;
      text-align: center;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    input {
      padding: 10px;
      width: 70%;
      margin-bottom: 10px;
    }
    button {
      padding: 10px;
      width: 100%;
      margin-bottom: 8px;
      cursor: pointer;
    }
    #message { margin-top: 10px; font-weight: bold; }

    .low { color: blue; }
    .high { color: red; }
    .win { color: green; }
    .error { color: orange; }

    #historyBox {
      margin-top: 10px;
      text-align: left;
      background: #f8f9fa;
      padding: 10px;
      border-radius: 5px;
      max-height: 120px;
      overflow-y: auto;
    }
  </style>
</head>
<body>

<div class="box">
  <h2>Number Guessing Game</h2>

  <button onclick="startGame()">Start Game</button>

  <input type="number" id="guessInput" placeholder="1-100" disabled>
  <button onclick="makeGuess()" id="guessBtn" disabled>Guess</button>

  <p id="attempts">Attempts: 0</p>
  <div id="message"></div>

  <div id="historyBox">
    <b>History:</b>
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

  // update attempts
  document.getElementById("attempts").innerText =
    "Attempts: " + data.attempts;

  // update history
  const list = document.getElementById("historyList");
  list.innerHTML = "";

  data.history.forEach(g => {
    const li = document.createElement("li");
    li.innerText = g;
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
        "message": "Game started! Guess a number.",
        "attempts": attempts,
        "history": guess_history
    })


@app.route("/guess/<int:num>")
def guess(num):
    global secret_number, attempts, guess_history

    if secret_number is None:
        return jsonify({
            "message": "Start the game first!",
            "result": "error"
        })

    attempts += 1
    guess_history.append(num)

    if num < secret_number:
        return jsonify({
            "message": "Too low! Try higher 🔼",
            "result": "low",
            "attempts": attempts,
            "history": guess_history
        })

    elif num > secret_number:
        return jsonify({
            "message": "Too high! Try lower 🔽",
            "result": "high",
            "attempts": attempts,
            "history": guess_history
        })

    else:
        return jsonify({
            "message": f"🎉 Correct! Attempts: {attempts}",
            "result": "win",
            "attempts": attempts,
            "history": guess_history
        })


if __name__ == "__main__":
    app.run(debug=True)