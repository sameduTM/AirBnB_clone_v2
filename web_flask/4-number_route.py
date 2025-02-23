#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    return f"Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return f"HBNB"


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    return f"C {escape(text)}".replace("_", " ")


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    return f"Python {escape(text)}".replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
