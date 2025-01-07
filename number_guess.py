from flask import Flask, render_template, request
import random, math

app = Flask(__name__)

# Variables to hold the game state
game_state = {
    "generated_num": None,
    "minimum_guess": None,
    "user_attempts": 0,
    "num_range": None,
}

@app.route("/", methods=["GET", "POST"])
def number_guess():
    if request.method == "POST":
        if "start_game" in request.form:
            num_range = int(request.form["num_range"])
            game_state["generated_num"] = random.randint(1, num_range)
            range_size = num_range - 1 + 1
            game_state["minimum_guess"] = math.ceil(math.log2(range_size))
            game_state["user_attempts"] = 0
            game_state["num_range"] = num_range
            return render_template(
                "index.html",
                num_range=num_range,
                status="Game Started! Enter your guess below:",
                show_guess=True
            )
        elif "guess" in request.form:
            guessed_number = int(request.form["guessed_number"])
            game_state["user_attempts"] += 1

            if guessed_number == game_state["generated_num"]:
                return render_template(
                    "index.html",
                    status="Congratulations! You guessed it right.",
                    show_guess=False
                )
            elif guessed_number < game_state["generated_num"] and game_state["user_attempts"] < game_state["minimum_guess"]:
                return render_template(
                    "index.html",
                    num_range=game_state["num_range"],
                    status="Too Low! Try Again.",
                    show_guess=True
                )
            elif guessed_number > game_state["generated_num"] and game_state["user_attempts"] < game_state["minimum_guess"]:
                return render_template(
                    "index.html",
                    num_range=game_state["num_range"],
                    status="Too High! Try Again.",
                    show_guess=True
                )
            elif game_state["user_attempts"] >= game_state["minimum_guess"]:
                return render_template(
                    "index.html",
                    status=f"Game Over! The number was {game_state['generated_num']}.",
                    show_guess=False
                )
    return render_template("index.html", status="Enter a number greater than 1 to start the game:", show_guess=False)

if __name__ == "__main__":
    app.run(debug=True)
