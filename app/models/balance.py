from flask import current_app as app

class Balance:
    def __init__(self, trans_id, trans_date, id, trans, balance):
        self.trans_id = trans_id
        self.trans_date = trans_date
        self.id = id
        self.trans = trans
        self.balance = balance

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT trans_id, trans_date, id, trans, balance
FROM Balance
WHERE id = :id
''',
                              id=id)
        return Balance(*(rows[0])) if rows is not None else None
