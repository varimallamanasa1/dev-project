from flask import Flask, render_template, request, redirect, url_for
import random
from threading import Lock

app = Flask(__name__)

MIN_NUM = 1
MAX_NUM = 100

_state = {
    "secret_number": random.randint(MIN_NUM, MAX_NUM),
    "guess_count": 0,
}
_lock = Lock()


def reset_game():
    with _lock:
        _state["secret_number"] = random.randint(MIN_NUM, MAX_NUM)
        _state["guess_count"] = 0


@app.route("/")
def index():
    with _lock:
        guess_count = _state["guess_count"]
    message = f"Guess a number between {MIN_NUM} and {MAX_NUM}."
    return render_template("index.html", message=message, guess_count=guess_count)


@app.route("/guess", methods=["POST"])
def guess():
    form_value = request.form.get("guess")
    try:
        user_guess = int(form_value)
    except:
        message = "Invalid input. Enter a valid number."
        return render_template("index.html", message=message, guess_count=_state["guess_count"])

    with _lock:
        _state["guess_count"] += 1
        guess_count = _state["guess_count"]
        secret = _state["secret_number"]

    if user_guess == secret:
        message = f"🎉 Correct! You guessed {secret} in {guess_count} attempts."
        reset_game()
        return render_template("result.html", message=message)

    if user_guess < secret:
        message = f"Too low! Try again. (Guess #{guess_count})"
    else:
        message = f"Too high! Try again. (Guess #{guess_count})"

    return render_template("index.html", message=message, guess_count=guess_count)


@app.route("/reset")
def reset():
    reset_game()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
