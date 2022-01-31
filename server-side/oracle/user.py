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
