from flask import current_app as app

class Orders:
    def __init__(self, order_id, buyer_id, product_name, time_stamp, total_amount, fulfillment_status):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.product_name = product_name
        self.time_stamp = time_stamp
        self.total_amount = total_amount
        self.fulfillment_status = fulfillment_status

    @staticmethod
    def get(buyer_id):
        rows = app.db.execute('''
SELECT order_id, buyer_id, product_name, time_stamp, total_amount, fulfillment_status
FROM Orders
WHERE buyer_id = :buyer_id
ORDER BY time_stamp DESC
''',
                              buyer_id=buyer_id)

        return [Orders(*row) for row in rows]

class Search:
	def __init__(self):
		pass

	@staticmethod
	def search_order(search, buyer_id):
		order_list = search.split(" ")

		regex = '''{d}'''.format(d='|'.join(order_list))
	
		rows = app.db.execute("""
SELECT order_id, buyer_id, product_name, time_stamp, total_amount, fulfillment_status
FROM Orders
WHERE buyer_id=:buyer_id AND product_name ~* :regex
ORDER BY time_stamp DESC
""",
					regex=regex,
                    buyer_id = buyer_id)
		
		print(rows)
		if len(rows) == 0:
			return None

		return [Orders(*row) for row in rows]