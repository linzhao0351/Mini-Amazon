from flask import current_app as app


class Fulfillment:
    def __init__(self, id, uid, seller_id, pid, price, quantity, time_purchased, fulfillment):
        self.id = id
        self.uid = uid
        self.seller_id = seller_id
        self.pid = pid
        self.price = price        
        self.quantity = quantity
        self.time_purchased=time_purchased
        self.fulfillment = fulfillment

# display order information
    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT p1.*
FROM Purchases p1, Products p2
WHERE p2.uid = :seller_id AND p1.pid = p2.id
ORDER BY p1.time_purchased DESC
''',
                              seller_id=seller_id)
        if rows is None:
            return None
        return rows

    @staticmethod
    def get_order(id, seller_id):
        rows = app.db.execute('''
SELECT p1.id, p1.pid, p2.name, p1.quantity
FROM Purchases p1, Products p2
WHERE p1.id = :id AND p1.pid = p2.id AND p2.uid=:seller_id
ORDER BY p1.pid ASC
''',
                              id=id,
                              seller_id=seller_id)
        if rows is None:
            return None
        return rows

# update fulfillment status
    @staticmethod
    def update(id, fulfillment):
        res = app.db.execute('''
UPDATE Purchases
SET fulfillment=:fulfillment
WHERE id=:id
''',
					id=id,
                  fulfillment=fulfillment)
        return res   

#fulfillment summary
    @staticmethod
    def count_fulfill(seller_id):
        rows = app.db.execute('''
SELECT p1.fulfillment, COUNT(p1.fulfillment) AS num_fulfill
FROM Purchases p1, Products p2
WHERE p2.uid = :seller_id AND p1.pid = p2.id
GROUP BY p1.fulfillment
''',
                              seller_id=seller_id)
        if rows is None:
            return None
        return rows

    @staticmethod
    def meanrev(seller_id):
        rows = app.db.execute('''
WITH t1 AS (
    SELECT p1.id, p1.price*p1.quantity AS revenue
    FROM Purchases p1, Products p2
    WHERE p2.uid = :seller_id AND p1.pid = p2.id), t2 AS(
        SELECT t1.id, SUM(t1.revenue) AS totalrevenue
        FROM t1
        GROUP BY t1.id
    ) 
SELECT  ROUND(AVG(totalrevenue)::numeric,2) AS averevenue
FROM t2
''',
                              seller_id=seller_id)
        if rows is None:
            return None
        return rows


######################
# add fake order detail data 
    @staticmethod
    def fake_order(uid, pid, price, quantity, fulfillment='false'):
        try:
            rows = app.db.execute("""
INSERT INTO Purchases(uid, pid, price, quantity, time_purchased, fulfillment)
VALUES(:uid, :pid, :price, :quantity, CURRENT_TIMESTAMP, :fulfillment)
RETURNING id 
""",
                                  uid = uid,
                                  pid = pid,
                                  price=price,
                                  quantity = quantity,
                                  fulfillment = fulfillment)
            if rows is None:
                return None
            return [Fulfillment(*row) for row in rows]
        except Exception as e:
            print(str(e))
            return None           