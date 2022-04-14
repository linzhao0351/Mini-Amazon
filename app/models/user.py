from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

from .dal.api import dal_api as db

class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, nickname, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.address = address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, nickname, address
FROM Users
WHERE email = :email
""",
                              email=email)

        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, nickname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, nickname, address)
VALUES(:email, :password, :firstname, :lastname, :nickname, :address)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname,
                                  nickname=nickname, address=address)
            id = rows[0][0]
 
            app.db.execute("""
INSERT INTO Current_balance(user_id)
VALUES(:user_id)
""",
                                user_id=id)

            return User.get(id)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, nickname, address
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def Update(id, email, firstname, lastname, nickname, address):
        rows = app.db.execute("""
UPDATE Users
SET email=:email, firstname=:firstname , lastname=:lastname, nickname=:nickname, address=:address
WHERE id=:id
""",
                              id=id,
                              email=email, 
                              firstname=firstname, 
                              lastname=lastname, 
                              nickname=nickname,
                              address=address)
        return "Success"
    
    @staticmethod
    def get_proxy_id():
        all_id = app.db.execute('''
SELECT id
FROM Users
''')
        return max(all_id)
