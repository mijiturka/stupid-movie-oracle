from argon2 import PasswordHasher
from flask import Flask, abort, redirect, render_template, request, session, url_for
from flask_login import current_user, LoginManager, login_required, login_user, UserMixin
from pathlib import Path
import secrets

from oracle import options, user

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
    def __init__(self, username):
        self.username = username
        app.logger.debug(f'Created new instance of User: {self}')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return self.username

    def check_password(self, password):
        try:
            return PasswordHasher().verify(user.get_password(self.username), password)
        except Exception as e:
            app.logger.debug(e)
            return False

@app.route('/login-after-registration', methods=['GET', 'POST'])
def login_after_registration():
    return login(redirected_from_registration=True)

@app.route('/login', methods=['GET', 'POST'])
def login(redirected_from_registration=False):
    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    # Handle login once form has been submitted
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not user.exists(username):
            return render_template('login.html', wrong_login_details=True)

        if user.locked(username):
            app.logger.info(f'{username} keeps trying')
            return abort(403)

        if User(username).check_password(password):
            login_user(User(username))
            user.reset_unsuccessful_login_attempts(username)
            app.logger.info(f'Successfully logged-in {username}')
            return redirect(url_for('main'))
        else:
            app.logger.info(f'Failed login attempt for {username}')
            user.handle_unsuccessful_login_attempt(username)
            return render_template('login.html', wrong_login_details=True)

    # Display login page
    return render_template('login.html',
     redirected_from_registration=redirected_from_registration
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Already logged in - thus registered
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    # Handle registration once form has been submitted
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user.new(username, PasswordHasher().hash(password))
            app.logger.info(f'Successfully registered {username}')
        except user.AlreadyExistsError as e:
            app.logger.info(f'Re-registration attempted for {username}')
            return render_template('register.html', username_already_exists=True)

        return redirect('/login-after-registration', code=303)

    # Display login page
    return render_template('register.html')

@login_manager.user_loader
def load_user(userid):
    return User(userid)
