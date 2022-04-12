from flask import current_app as app

class Cart:
	def __init__(self, user_id, seller_id, product_id, product_name, quantity, price, ts):
		self.user_id = user_id
		self.seller_id = seller_id
		self.product_id = product_id
		self.product_name = product_name
		self.quantity = quantity
		self.price = price
		self.ts = ts
		
	@staticmethod
	def get(user_id):
		rows = app.db.execute('''
SELECT c.user_id, p.product_id, c.product_id, p.name, c.quantity, p.price, c.ts
FROM User_cart AS c, Products AS p
WHERE c.user_id = :user_id AND c.product_id = p.product_id 
''',
							user_id=user_id)

		if rows is None:
			return None

		return [Cart(*row) for row in rows]


	@staticmethod
	def insert(user_id, product_id, quantity):
		check = app.db.execute('''
SELECT quantity
FROM User_cart
WHERE user_id = :user_id AND product_id = :product_id
''',
							user_id=user_id,
							product_id=product_id)

		if len(check) > 0:
			qty = check[0][0]
			new_qty = qty + quantity

			res = Cart.update(user_id, product_id, new_qty)
			return res

		res = app.db.execute('''
INSERT INTO User_cart(user_id, product_id, quantity)
VALUES (:user_id, :product_id, :quantity)
''',
						user_id=user_id,
						product_id=product_id,
						quantity=quantity)
		
		return Cart.get(user_id)


	@staticmethod
	def clear(user_id):
		res = app.db.execute('''
DELETE 
FROM User_cart
WHERE user_id=:user_id
''',
					user_id=user_id)
		return res


	@staticmethod
	def delete(user_id, product_id):
		res = app.db.execute('''
DELETE 
FROM User_cart
WHERE user_id=:user_id AND product_id=:product_id
''',
					user_id=user_id,
					product_id=product_id)
		return res


	@staticmethod
	def update(user_id, product_id, quantity):
		res = app.db.execute('''
UPDATE User_cart
SET quantity=:quantity
WHERE user_id=:user_id AND product_id=:product_id
''',
					user_id=user_id,
					product_id=product_id,
					quantity=quantity)

		return res


	@staticmethod
	def submit_aggregate(total_amount):
		res = app.db.execute('''
INSERT INTO Orders_summary(total_amount)
VALUES (:total_amount)
RETURNING order_id
''',
					total_amount=total_amount)

		order_id = res[0][0]
		return order_id
		

	@staticmethod
	def submit_detail(buyer_id, order_id, cart):
		for item in cart:
			app.db.execute('''
INSERT INTO Orders(order_id, buyer_id, seller_id, product_id, quantity, price)
VALUES (:order_id, :buyer_id, :seller_id, :product_id, :quantity, :price)
''',
					order_id=order_id,
					buyer_id=buyer_id,
					seller_id=item.seller_id,
					product_id=item.product_id,
					quantity=item.quantity,
					price=item.price)

		return "Success"


	@staticmethod
	def retract_order(order_id):
		app.db.execute('''
DELETE 
FROM Orders_summary
WHERE order_id=:order_id
''',
					order_id=order_id)

		app.db.execute('''
DELETE 
FROM Orders
WHERE order_id=:order_id
''',
					order_id=order_id)

		return 0




		





