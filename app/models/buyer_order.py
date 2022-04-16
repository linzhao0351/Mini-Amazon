from flask import current_app as app

class OrderSummary():
    def __init__(self, order_id, buyer_id, ts, total_amount, order_status):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.ts = ts
        self.total_amount = total_amount
        self.order_status = order_status

class Orders():

    def __init__(self, order_id, product_id, seller_id, quantity, price, fulfillment_status, product_name):
        self.order_id = order_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        self.price = price        
        self.fulfillment_status = fulfillment_status
        self.product_name = product_name


    @staticmethod
    def get_order_summary(buyer_id):
        rows = app.db.execute('''
SELECT *
FROM Orders_summary
WHERE buyer_id = :buyer_id
ORDER BY ts DESC
''',
                    buyer_id=buyer_id)

        if len(rows) == 0:
            return None       
        
        return [OrderSummary(*row) for row in rows]


    @staticmethod
    def get_order_detail(order_id):
        rows = app.db.execute('''
SELECT p1.*, p3.name
FROM Orders AS p1, Products AS p3
WHERE p1.order_id=:order_id AND p1.product_id=p3.product_id
''',
                              order_id=order_id)
        if len(rows) == 0:
            return None
        
        return [Orders(*row) for row in rows]





class Search:
	def __init__(self):
		pass

	@staticmethod
	def search_order(search, buyer_id):
		order_list = search.split(" ")

		regex = '''{d}'''.format(d='|'.join(order_list))
	
		rows = app.db.execute("""
SELECT order_id, buyer_id, product_name, ts, total_amount, fulfillment_status
FROM Orders
WHERE buyer_id=:buyer_id AND product_name ~* :regex
ORDER BY ts DESC
""",
					regex=regex,
                    buyer_id = buyer_id)
		
		if len(rows) == 0:
			return None

		return [Orders(*row) for row in rows]