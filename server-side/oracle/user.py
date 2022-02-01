from pony import orm

db = orm.Database()

class User(db.Entity):
    username = orm.PrimaryKey(str)
    password = orm.Required(str)

    unsuccessful_login_attempts = orm.Required(int, default=0)
    locked = orm.Required(bool, default=False)

db.bind(provider='sqlite', filename='../users/users.db', create_db=True)
db.generate_mapping(create_tables=True)

@orm.db_session
def get_password(username):
    return User[username].password

@orm.db_session
def new(username, password_hash):
    if exists(username):
        raise AlreadyExistsError(f'User {username} already exists')
    # Create new user
    User(username=username, password=password_hash)
    orm.commit()

class AlreadyExistsError(Exception):
    pass

@orm.db_session
def exists(username):
    try:
        User[username]
        return True
    except orm.core.ObjectNotFound:
        return False

@orm.db_session
def locked(username):
    return User[username].locked

@orm.db_session
def handle_unsuccessful_login_attempt(username):
    if User[username].unsuccessful_login_attempts >= 6:
        # Lock the user's account
        User[username].locked = True
        return

    # Record this attempt
    User[username].unsuccessful_login_attempts += 1

@orm.db_session
def reset_unsuccessful_login_attempts(username):
    User[username].unsuccessful_login_attempts = 0
