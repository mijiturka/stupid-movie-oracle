from argon2 import PasswordHasher
from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import current_user, LoginManager, login_required, login_user, UserMixin
import logging
from pathlib import Path
import secrets

from oracle import options

app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = secrets.token_urlsafe(64)

@app.route('/')
@login_required
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

class User(UserMixin):
    id = 1
    username = 'capellyana'

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        try:
            return PasswordHasher().verify(Path('users/capellyana.key').read_text().strip(), password)
        except Exception as e:
            return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    # Handle login once form has been submitted
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'capellyana' and User().check_password(password):
            login_user(User())
            return redirect(url_for('main'))
        else:
            return render_template('login.html', wrong_login_details=True)

    # Display login page
    return render_template('login.html')

@login_manager.user_loader
def load_user(userid):
    return User()
