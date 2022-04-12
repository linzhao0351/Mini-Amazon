from flask import current_app as app


class SellerOrder():

    def __init__(self, order_id, buyer_id, seller_id, product_id, price, quantity, fulfillment_status, ts, product_name):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.price = price        
        self.quantity = quantity
        self.ts = ts
        self.fulfillment_status = fulfillment_status
        self.product_name = product_name

    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT p1.*, p2.ts, p3.name
FROM Orders AS p1, Orders_summary AS p2, Products AS p3
WHERE p1.order_id = p2.order_id AND p1.product_id=p3.product_id
ORDER BY p2.ts DESC
''',
                              seller_id=seller_id)
        if len(rows) == 0:
            return None
        
        return [SellerOrder(*row) for row in rows]

    @staticmethod
    def get_order(order_id, seller_id):
        rows = app.db.execute('''
SELECT p1.*, p2.ts, p3.name
FROM Orders AS p1, Orders_summary AS p2, Products AS p3
WHERE p1.seller_id=:seller_id AND p1.order_id=:order_id AND p1.order_id = p2.order_id AND p1.product_id=p3.product_id AND p1.seller_id=:seller_id
ORDER BY p2.ts DESC
''',
                              order_id=order_id,
                              seller_id=seller_id)
        if len(rows) == 0:
            return None
        
        return [SellerOrder(*row) for row in rows]