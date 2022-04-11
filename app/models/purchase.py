from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, seller_id, pid, price, quantity, time_purchased):
        self.id = id
        self.uid = uid
        self.seller_id = seller_id
        self.pid = pid
        self.price = price
        self.quantity = quantity
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

### changes from here
    #@staticmethod
    def get_trendy_prod(seller_id):
        rows = app.db.execute('''
SELECT A.pid, A.sales, B.name, B.quantity
FROM        
(SELECT pid, SUM(quantity) AS sales
FROM Purchases
WHERE time_purchased > CURRENT_DATE - INTERVAL '3 months'
GROUP BY pid) AS A, Products AS B
WHERE B.uid = :seller_id AND B.id = A.pid
ORDER BY A.sales DESC
LIMIT 5
''',
                                seller_id=seller_id)
        print(rows)
        return rows