from flask import Flask, render_template, request, redirect, url_for
from getdata import get_data
from random import shuffle
from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABC"


@app.route("/", methods=["GET", "POST"])
def dictionary():
    try:
        filepath = Path("static/words.txt")
        with open(filepath) as file:
            words = [word.replace(",", "").title() for word in file.read().split() if "," in word]
            shuffle(words)

        if request.method == "POST":
            word = request.form.get("search")
            return redirect(url_for("display", word=word))

        return render_template("dictionary.html", words=words)
    except KeyError:
        return "<h1>Sorry</h1> <p> Word not found in the dictionary </p> <a href='/'> Return to home page </a>"


@app.route("/display/<word>", methods=["GET", "POST"])
def display(word):
    try:
        data = get_data(word)
        if request.method == "POST":
            word = request.form.get("search")
            return redirect(url_for("display", word=word))

        return render_template("display.html", data=data, word=word.title())
    except KeyError:
        return "<h1>Sorry</h1> <p> Word not found in the dictionary </p> <a href='/'> Return to home page </a>"


if __name__ == "__main__":
    app.run(debug=True)
