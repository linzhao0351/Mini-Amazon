from flask import current_app as app


class OrderSummary():
    def __init__(self, order_id, buyer_id, ts, firstname, lastname, address, order_status):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.ts = ts
        self.order_status = order_status

class SellerOrder():

    def __init__(self, order_id, product_id, seller_id, quantity, price, fulfillment_status, product_name):
        self.order_id = order_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        self.price = price        
        self.fulfillment_status = fulfillment_status
        self.product_name = product_name


    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT p1.*, p3.name, S.ts
FROM Orders AS p1, Products AS p3, Orders_summary as S
WHERE p1.seller_id=:seller_id AND p1.product_id=p3.product_id AND p1.order_id=S.order_id
ORDER BY S.ts DESC
''',
                              seller_id=seller_id)
        if len(rows) == 0:
            return None

        return [SellerOrder(*row[0:-1]) for row in rows]
        

    @staticmethod
    def get_order_summary(order_id):
        rows = app.db.execute('''
SELECT O.order_id, O.buyer_id, O.ts, U.firstname, U.lastname, U.address, O.order_status
FROM Orders_summary AS O, Users AS U
WHERE O.order_id=:order_id AND O.buyer_id=U.id
ORDER BY O.ts DESC
''',
                    order_id=order_id)

        if len(rows) == 0:
            return None       
        
        return OrderSummary(*(rows[0]))
        

    @staticmethod
    def get_order(order_id, seller_id):
        rows = app.db.execute('''
SELECT p1.*, p3.name
FROM Orders AS p1, Products AS p3, Users As U
WHERE p1.order_id=:order_id AND 
      p1.seller_id=:seller_id AND 
      p1.product_id=p3.product_id AND 
''',
                              order_id=order_id,
                              seller_id=seller_id)
        if len(rows) == 0:
            return None
        
        return [SellerOrder(*row) for row in rows]


    @staticmethod
    def get_product(order_id, product_id):
        rows = app.db.execute('''
SELECT p1.*, p3.name
FROM Orders AS p1, Products AS p3
WHERE p1.order_id=:order_id AND p1.product_id=p3.product_id
''',
                              order_id=order_id,
                              product_id=product_id)
        
        return SellerOrder(*(rows[0]))


    @staticmethod
    def update(order_id, product_id, fulfillment):
        res = app.db.execute('''
UPDATE Orders
SET fulfillment_status=:fulfillment_status
WHERE order_id=:order_id AND product_id=:product_id
''',
                    order_id=order_id,
                    product_id=product_id,
                    fulfillment_status=fulfillment)

        rows = app.db.execute('''
SELECT fulfillment_status
FROM Orders
WHERE order_id=:order_id
''',
                    order_id=order_id)

        # check status of every product
        fstatus = [row[0] for row in rows]
        if 0 in fstatus:
            pass
        else:
            app.db.execute('''
UPDATE Orders_summary
SET order_status=1
WHERE order_id=:order_id
''',
                    order_id=order_id)

        return res   


    @staticmethod
    def norder(seller_id):
        rows = app.db.execute('''
SELECT COUNT(DISTINCT order_id) AS num_order
FROM Orders
WHERE seller_id = :seller_id 
''',
                              seller_id=seller_id)
        if rows is None:
            return None
        return rows

    @staticmethod
    def mean_nprod_rev(seller_id):
        rows = app.db.execute('''
WITH t1 AS (
    SELECT order_id, product_id, price*quantity AS revenue
    FROM Orders
    WHERE seller_id = :seller_id), t2 AS(
        SELECT t1.order_id, COUNT(DISTINCT t1.product_id) AS num_prod, SUM(t1.revenue) AS totalrevenue
        FROM t1
        GROUP BY t1.order_id
    ) 
SELECT ROUND(AVG(num_prod)::numeric,2) AS ave_nprod, ROUND(AVG(totalrevenue)::numeric,2) AS ave_revenue
FROM t2
''',
                              seller_id=seller_id)
        if rows is None:
            return None
        return rows
