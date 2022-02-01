from pony import orm

db = orm.Database()

class User(db.Entity):
    username = orm.PrimaryKey(str)
    password = orm.Required(str)

db.bind(provider='sqlite', filename='../users/users.db', create_db=True)
db.generate_mapping(create_tables=True)

@orm.db_session
def get_password(username):
    return User[username].password

@orm.db_session
def new(username, password_hash):
    try:
        User[username]
        raise AlreadyExistsError(f'User {username} already exists')
    except orm.core.ObjectNotFound:
        # User doesn't exist - create it
        User(username=username, password=password_hash)
        orm.commit()

class AlreadyExistsError(Exception):
    pass
