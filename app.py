from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Initialize game state
game_state = {
    "board": [""] * 9,  # 3x3 grid of empty strings
    "turn": "X",  # X always starts first
    "player1": "PLAYER1",
    "player2": "PLAYER2",
    "winner": None,
    "draw": False,
    "player1_wins": 0,
    "player2_wins": 0,
    "current_player": "PLAYER1",
}

WIN_PATTERNS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]  # Diagonals
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle player name input
        if "player1" in request.form and "player2" in request.form:
            game_state["player1"] = request.form["player1"]
            game_state["player2"] = request.form["player2"]
            game_state["current_player"] = game_state["player1"]
            return redirect("/game")
    return render_template("enter_names.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    if not game_state["player1"] or game_state["player1"] == "PLAYER1":
        return redirect("/")
        
    if request.method == "POST" and "cell" in request.form:
        # Handle game move
        index = int(request.form["cell"])
        if game_state["board"][index] == "" and game_state["winner"] is None:
            # Place the mark
            game_state["board"][index] = game_state["turn"]
            # Switch turn
            game_state["turn"] = "O" if game_state["turn"] == "X" else "X"
            game_state["current_player"] = game_state["player2"] if game_state["turn"] == "O" else game_state["player1"]
            check_winner()
            if game_state["winner"]:
                return redirect("/game")
            if "" not in game_state["board"]:
                game_state["draw"] = True
                return redirect("/game")
    return render_template("index.html", game_state=game_state)

@app.route("/reset", methods=["POST"])
def reset():
    # Reset the game to its initial state (not a new game, just a reset)
    game_state["board"] = [""] * 9
    game_state["turn"] = "X"
    game_state["winner"] = None
    game_state["draw"] = False
    return redirect("/game")

@app.route("/new_game", methods=["POST"])
def new_game():
    # Reset the entire game including scores and player names
    game_state["board"] = [""] * 9
    game_state["turn"] = "X"
    game_state["winner"] = None
    game_state["draw"] = False
    game_state["player1"] = "PLAYER1"
    game_state["player2"] = "PLAYER2"
    game_state["player1_wins"] = 0
    game_state["player2_wins"] = 0
    game_state["current_player"] = "PLAYER1"
    return redirect("/")

def check_winner():
    # Check if there is a winner
    for pattern in WIN_PATTERNS:
        if game_state["board"][pattern[0]] == game_state["board"][pattern[1]] == game_state["board"][pattern[2]] != "":
            game_state["winner"] = game_state["board"][pattern[0]]
            if game_state["winner"] == "X":
                game_state["player1_wins"] += 1
            else:
                game_state["player2_wins"] += 1
            return

if __name__ == "__main__":
    app.run(debug=True, port=5001)
