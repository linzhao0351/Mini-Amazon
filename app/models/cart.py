from flask import current_app as app
from datetime import date


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
SELECT c.user_id, p.seller_id, c.product_id, p.name, c.quantity, p.price, c.ts
FROM User_cart AS c, Products AS p
WHERE c.user_id = :user_id AND c.product_id = p.product_id 
''',
							user_id=user_id)

		if rows is None:
			return None

		return [Cart(*row) for row in rows]

	@staticmethod
	def get_quantity(user_id, product_id):
		rows = app.db.execute('''
SELECT quantity
FROM User_cart
WHERE user_id=:user_id AND product_id=:product_id
''',
							user_id=user_id,
							product_id=product_id)

		if len(rows) == 0:
			return 0

		return rows[0][0]


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
	def submit_aggregate(buyer_id, total_amount):
		res = app.db.execute('''
INSERT INTO Orders_summary(buyer_id, total_amount)
VALUES (:buyer_id, :total_amount)
RETURNING order_id
''',
					buyer_id=buyer_id,
					total_amount=total_amount)

		order_id = res[0][0]
		return order_id
		

	@staticmethod
	def check_avail(cart):
		for item in cart:
			rows = app.db.execute('''
SELECT units_avail
FROM Products
WHERE product_id = :product_id
''',
					product_id=item.product_id)

			avail_units=rows[0][0]
			if avail_units < item.quantity:
				msg = "%s has only %s units available" % (item.product_name, avail_units)
				return msg

		return "Valid"

	@staticmethod
	def check_balance(user_id, total_amount):
		rows = app.db.execute('''
SELECT current_balance
FROM Current_Balance
WHERE user_id=:user_id
''',
					user_id=user_id)

		balance=rows[0][0]
		if balance < total_amount:
			return "Insufficient fund"

		return "Valid"


	@staticmethod
	def submit_detail(order_id, cart):
		for item in cart:
			app.db.execute('''
INSERT INTO Orders(order_id, product_id, seller_id, quantity, price)
VALUES (:order_id, :product_id, :seller_id, :quantity, :price)
''',
					order_id=order_id,
					product_id=item.product_id,
					seller_id=item.seller_id,
					quantity=item.quantity,
					price=item.price)

		return "Success"

	@staticmethod
	def update_inventory(cart):
		for item in cart:
			app.db.execute('''
UPDATE Products
SET units_avail=units_avail - :quantity
WHERE product_id=:product_id
''',
					quantity=item.quantity,
					product_id=item.product_id)

		return "Success"

	@staticmethod
	def update_balance(user_id, total_amount):
		rows = app.db.execute('''
UPDATE Current_Balance
SET current_balance=current_balance - :total_amount
WHERE user_id=:user_id
RETURNING current_balance
''',
					total_amount=total_amount,
					user_id=user_id)

		current_balance = rows[0][0]
		
		app.db.execute('''
INSERT INTO Balance(trans_date, user_id, trans, trans_description, balance)
VALUES (:trans_date, :user_id, :trans, :trans_description, :balance)
''',
					trans_date = date.today(),
					user_id = user_id, 
					trans = total_amount, 
					trans_description='Purchase',
					balance = current_balance)

		return "Success"

	@staticmethod
	def update_seller_balance(cart):
		for item in cart:
			rows = app.db.execute('''
UPDATE Current_Balance
SET current_balance=current_balance + :total_amount
WHERE user_id=:user_id
RETURNING current_balance
''',
					total_amount=item.quantity * item.price,
					user_id=item.seller_id)

			current_balance = rows[0][0]

			app.db.execute('''
INSERT INTO Balance(trans_date, user_id, trans, trans_description, balance)
VALUES (:trans_date, :user_id, :trans, :trans_description, :balance)
''',
					trans_date = date.today(),
					user_id = item.seller_id, 
					trans = item.quantity * item.price, 
					trans_description='Sell of product %s' % item.product_id,
					balance = current_balance)

		return "Success"


	@staticmethod
	def retract_order(order_id):
		app.db.execute('''
DELETE 
FROM Orders
WHERE order_id=:order_id
''',
					order_id=order_id)

		return 0

		app.db.execute('''
DELETE 
FROM Orders_summary
WHERE order_id=:order_id
''',
					order_id=order_id)



	@staticmethod
	def cancel_item(user_id, order_id, product_id):
		# delete from Orders
		rows = app.db.execute('''
SELECT price, quantity, seller_id
FROM Orders
WHERE order_id=:order_id AND product_id=:product_id
''',
					order_id=order_id,
					product_id=product_id)

		quantity = rows[0][1]
		product_amount = rows[0][0] * rows[0][1]
		seller_id = rows[0][2]

		# cancel from Orders
		app.db.execute('''
DELETE 
FROM Orders
WHERE order_id=:order_id AND product_id=:product_id
''',
					order_id=order_id,
					product_id=product_id)

		# Update Orders_summary
		rows = app.db.execute('''
SELECT * FROM Orders
WHERE order_id=:order_id
''',
					order_id=order_id)

		# if no other products under the same order
		if len(rows) == 0:
			app.db.execute('''
DELETE 
FROM Orders_summary
WHERE order_id=:order_id
''',
					order_id=order_id)
		# if there are other products under the same order
		else:
			app.db.execute('''
UPDATE Orders_summary
SET total_amount = total_amount - :product_amount
WHERE order_id=:order_id
''',
					order_id=order_id,
					product_amount=product_amount)	

		# add money back to consumer
		rows = app.db.execute('''
UPDATE Current_Balance
SET current_balance=current_balance + :product_amount
WHERE user_id=:user_id
RETURNING current_balance
''',
					product_amount=product_amount,
					user_id=user_id)

		current_balance = rows[0][0]

		app.db.execute('''
INSERT INTO Balance(trans_date, user_id, trans, trans_description, balance)
VALUES (:trans_date, :user_id, :trans, :trans_description, :balance)
''',
					trans_date = date.today(),
					user_id = user_id, 
					trans = product_amount, 
					trans_description='Retract product %s from order %s' % (product_id, order_id),
					balance = current_balance)

		# retract money from seller
		rows = app.db.execute('''
UPDATE Current_Balance
SET current_balance=current_balance - :product_amount
WHERE user_id=:user_id
RETURNING current_balance
''',
					product_amount=product_amount,
					user_id=seller_id)

		current_balance = rows[0][0]

		app.db.execute('''
INSERT INTO Balance(trans_date, user_id, trans, trans_description, balance)
VALUES (:trans_date, :user_id, :trans, :trans_description, :balance)
''',
					trans_date = date.today(),
					user_id = seller_id, 
					trans = product_amount, 
					trans_description='Retract product %s from order %s' % (product_id, order_id),
					balance = current_balance)

		# add back inventory
		app.db.execute('''
UPDATE Products
SET units_avail = units_avail + :quantity
WHERE product_id = :product_id
''',
					quantity=quantity,
					product_id=product_id)

		return "Success"





		





