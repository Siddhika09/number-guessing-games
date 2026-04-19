from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

secret_number = None
attempts = 0

# ------------------ PAGE 1 (HOME) ------------------
home_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Number Guessing Game</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI';
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #1d2671, #c33764);
      color: white;
      text-align: center;
    }
    h1 {
      font-size: 55px;
      letter-spacing: 3px;
    }
    p {
      font-size: 18px;
      margin-top: 20px;
      line-height: 1.6;
    }
    button {
      margin-top: 30px;
      padding: 15px 25px;
      font-size: 18px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      background: #00c9a7;
      color: white;
    }
  </style>
</head>

<body>
<div>
  <h1>🎯 NUMBER GUESSING GAME</h1>

  <h3>📜 How to Play:</h3>
  <p>
    1. Click Start Game<br>
    2. Guess number between 1-100<br>
    3. Get hints (Too High / Too Low)<br>
    4. Win in minimum attempts 😎
  </p>

  <button onclick="window.location.href='/game'">Start Game</button>
</div>
</body>
</html>
"""

# ------------------ PAGE 2 (YOUR ORIGINAL GAME - FULLY PRESERVED) ------------------
game_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Number Guessing Game</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI';
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #667eea, #764ba2);
    }

    .box {
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(10px);
      padding: 30px;
      border-radius: 15px;
      width: 400px;
      text-align: center;
      color: white;
    }

    input {
      padding: 12px;
      width: 75%;
      border-radius: 8px;
      border: none;
      text-align: center;
      margin-bottom: 10px;
    }

    button {
      padding: 12px;
      width: 100%;
      border: none;
      border-radius: 8px;
      margin-bottom: 10px;
      cursor: pointer;
      font-weight: bold;
      transition: 0.3s;
    }

    button:hover {
      transform: scale(1.05);
    }

    #startBtn { background: #00c9a7; color: white; }
    #guessBtn { background: #ff7a18; color: white; }

    #message {
      margin-top: 10px;
      padding: 10px;
      border-radius: 8px;
      font-weight: bold;
    }

    .low { background: rgba(0,150,255,0.2); }
    .high { background: rgba(255,50,50,0.2); }
    .win { background: rgba(0,255,150,0.3); }
    .error { background: rgba(255,200,0,0.3); }

    #attempts {
      margin-top: 10px;
      font-weight: bold;
    }

    #historyBox {
      margin-top: 15px;
      text-align: left;
      height: 240px;
      overflow-y: auto;
      background: rgba(255,255,255,0.1);
      padding: 12px;
      border-radius: 8px;
    }

    #historyList {
      list-style: none;
      padding: 0;
    }

    #historyList li {
      margin: 6px 0;
      padding: 8px;
      border-radius: 6px;
      background: rgba(255,255,255,0.2);
      font-size: 15px;
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
    <b>👉 Your Guesses</b>
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

  const li = document.createElement("li");
  li.innerText = "Your guess: " + num;
  list.appendChild(li);

  if (data.result === "win") {
    document.getElementById("guessInput").disabled = true;
    document.getElementById("guessBtn").disabled = true;

    // 🔥 redirect AFTER win (new feature)
    setTimeout(() => {
        window.location.href = "/thankyou";
    }, 1500);
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

# ------------------ PAGE 3 (THANK YOU) ------------------
thankyou_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Thank You</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI';
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #11998e, #38ef7d);
      color: white;
      text-align: center;
    }

    h1 { font-size: 50px; }

    button {
      margin-top: 20px;
      padding: 12px 20px;
      border: none;
      border-radius: 8px;
      background: #ff7a18;
      color: white;
      cursor: pointer;
    }
  </style>
</head>

<body>
<div>
  <h1>🎉 THANK YOU FOR PLAYING!</h1>
  <p>Hope you enjoyed 😎</p>
  <button onclick="window.location.href='/'">Play Again</button>
</div>
</body>
</html>
"""

# ------------------ ROUTES ------------------
@app.route("/")
def home():
    return render_template_string(home_page)

@app.route("/game")
def game():
    return render_template_string(game_page)

@app.route("/thankyou")
def thankyou():
    return render_template_string(thankyou_page)

@app.route("/start")
def start_game():
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    return jsonify({"message": "Game started! Guess wisely 😎"})

@app.route("/guess/<int:num>")
def guess(num):
    global secret_number, attempts
    attempts += 1

    if num < secret_number:
        return jsonify({"message": "Too low! Try higher 🔼", "result": "low", "attempts": attempts})
    elif num > secret_number:
        return jsonify({"message": "Too high! Try lower 🔽", "result": "high", "attempts": attempts})
    else:
        return jsonify({"message": f"🎉 You won in {attempts} attempts!", "result": "win", "attempts": attempts})

if __name__ == "__main__":
    app.run(debug=True)