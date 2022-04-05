from flask import current_app as app

from .product import Product

class Recommend:

	def __init__(self):
		pass


	@staticmethod
	def update_footprint(user_id, product_id):
		rows = app.db.execute("""
SELECT view_times
FROM User_browsing_history
WHERE user_id=:user_id AND product_id=:product_id
""",
				user_id=user_id,
				product_id=product_id)

		if len(rows) == 0:
			res = app.db.execute("""
INSERT INTO User_browsing_history (user_id, product_id, view_times)
VALUES (:user_id, :product_id, 1)
""",
				user_id=user_id,
				product_id=product_id)
			view_times = 1
		else:
			view_times = rows[0][0] + 1
			res = app.db.execute("""
UPDATE User_browsing_history
SET view_times=:view_times, last_view_ts=CURRENT_TIMESTAMP
WHERE user_id=:user_id AND product_id=:product_id
""",
				user_id=user_id,
				product_id=product_id,
				view_times=view_times)

		print(view_times)
		return res


	@staticmethod
	def rec_most_viewed_item(user_id):
		rows = app.db.execute("""
SELECT p.id, p.name, p.price, p.available, h.view_times
FROM Products AS p, User_browsing_history AS h
WHERE h.user_id = :user_id AND p.id = h.product_id
ORDER BY h.view_times DESC
""",
				user_id=user_id)

		if len(rows) == 0:
			return None

		print(rows)
		return [Product(*row[0:4]) for row in rows]

	@staticmethod
	def rec_recent_viewed_item(user_id):
		rows = app.db.execute("""
SELECT p.id, p.name, p.price, p.available, h.last_view_ts
FROM Products AS p, User_browsing_history AS h
WHERE h.user_id = :user_id AND p.id = h.product_id
ORDER BY h.last_view_ts DESC
""",
				user_id=user_id)

		if len(rows) == 0:
			return None

		print(rows)
		return [Product(*row[0:4]) for row in rows]





