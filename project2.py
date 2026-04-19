from flask import Flask, jsonify, render_template_string, redirect, url_for
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
            font-family: Arial;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #1d2671, #c33764);
            color: white;
            text-align: center;
        }
        .container {
            max-width: 600px;
        }
        h1 {
            font-size: 50px;
            letter-spacing: 3px;
        }
        p {
            font-size: 18px;
            margin-top: 20px;
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
<div class="container">
    <h1>🎯 NUMBER GUESSING GAME</h1>
    
    <h3>📜 How to Play:</h3>
    <p>
        1. Click on Start Game<br>
        2. Guess a number between 1 and 100<br>
        3. You will get hints (Too High / Too Low)<br>
        4. Try to win in minimum attempts 😎
    </p>

    <button onclick="window.location.href='/game'">Start Game</button>
</div>
</body>
</html>
"""

# ------------------ PAGE 2 (GAME) ------------------
game_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Play Game</title>
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

    input, button {
      padding: 12px;
      width: 100%;
      margin-bottom: 10px;
      border-radius: 8px;
      border: none;
    }

    button {
      cursor: pointer;
      font-weight: bold;
    }

    #message { margin-top: 10px; }
  </style>
</head>

<body>

<div class="box">
  <h2>🎮 Play Game</h2>

  <button onclick="startGame()">Start</button>

  <input type="number" id="guessInput" placeholder="Enter number" disabled>
  <button onclick="makeGuess()" id="guessBtn" disabled>Guess</button>

  <p id="attempts">Attempts: 0</p>
  <p id="message"></p>
</div>

<script>
async function startGame() {
  await fetch("/start");

  document.getElementById("guessInput").disabled = false;
  document.getElementById("guessBtn").disabled = false;

  document.getElementById("attempts").innerText = "Attempts: 0";
}

async function makeGuess() {
  const num = document.getElementById("guessInput").value;

  const res = await fetch("/guess/" + num);
  const data = await res.json();

  document.getElementById("message").innerText = data.message;
  document.getElementById("attempts").innerText = "Attempts: " + data.attempts;

  if (data.result === "win") {
    setTimeout(() => {
        window.location.href = "/thankyou";
    }, 1500);
  }

  document.getElementById("guessInput").value = "";
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
            font-family: Arial;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            text-align: center;
        }
        h1 {
            font-size: 50px;
        }
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
    <p>You did awesome 😎</p>
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
    return jsonify({"message": "Game Started!"})

@app.route("/guess/<int:num>")
def guess(num):
    global secret_number, attempts
    attempts += 1

    if num < secret_number:
        return jsonify({"message": "Too Low!", "result": "low", "attempts": attempts})
    elif num > secret_number:
        return jsonify({"message": "Too High!", "result": "high", "attempts": attempts})
    else:
        return jsonify({"message": "You Won!", "result": "win", "attempts": attempts})

if __name__ == "__main__":
    app.run(debug=True)