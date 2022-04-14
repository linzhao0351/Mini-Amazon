from flask import current_app as app


class Current_Balance:
    def __init__(self, balance):
        self.balance = balance

class Balance:
    def __init__(self, trans_id, trans_date, trans_ts, user_id, trans, trans_description, balance):
        self.trans_id = trans_id
        self.trans_date = trans_date
        self.trans_ts = trans_ts
        self.user_id = user_id
        self.trans = trans
        self.trans_description = trans_description
        self.balance = balance

    @staticmethod
    def get(user_id):
        rows = app.db.execute('''
SELECT current_balance
FROM Current_Balance
WHERE user_id = :user_id
''',
                              user_id=user_id)

        return Current_Balance(*rows[0])

    @staticmethod
    def get_lastrow():
        rows = app.db.execute('''
SELECT *
FROM Balance
''')
        return Balance(*(rows[-1])) if rows is not None else None

    @staticmethod
    def get_all(user_id):
        rows = app.db.execute('''
SELECT *
FROM Balance
WHERE user_id = :user_id
ORDER BY trans_date DESC
''',
                        user_id=user_id)
        return [Balance(*row) for row in rows]

class Update_balance:
    def __init__(self, trans_id, trans_date, user_id, trans, trans_description, balance):
        self.trans_id = trans_id
        self.trans_date = trans_date
        self.user_id = user_id
        self.trans = trans
        self.trans_description = trans_description
        self.balance = balance

    @staticmethod
    def insert(trans_date, user_id, trans, trans_description, balance):
        rows = app.db.execute('''
INSERT INTO Balance(trans_date, user_id, trans, trans_description, balance)
VALUES (:trans_date, :user_id, :trans, :trans_description, :balance)
''',
                              trans_date = trans_date, 
                              user_id = user_id, 
                              trans = trans, 
                              trans_description=trans_description,
                              balance = balance)

        rows = app.db.execute('''
UPDATE Current_balance
SET current_balance = :balance
WHERE user_id=:user_id
''',
                            user_id=user_id,
                            balance=balance)

        return "Success"


    

