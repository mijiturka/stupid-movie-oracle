from flask import Flask, render_template
from oracle import options

app = Flask(__name__)

@app.route('/')
def main():
    movies = [
    "Cats",
    "Breakin'",
    "Tougher Than Leather",
    "Krush Groove",
    "Red Planet Mars",
    "The Mummy's Ghost",
    "Final Stab",
    "The Wiz Live!"
    ]

    return render_template('oracle.html', movies=options.dieable(movies, sides=6))
