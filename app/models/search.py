from flask import current_app as app

from .product import Product

class ProductType:
	def __init__(self, type_id, ptype):
		self.type_id = type_id
		self.ptype = ptype

class Search:
	def __init__(self):
		pass

	@staticmethod
	def search_product(search_kw, type_id):
		kw_list = search_kw.split(" ")

		regex = '''{d}'''.format(d='|'.join(kw_list))

		if type_id == '0':
			rows = app.db.execute("""
SELECT *
FROM Products
WHERE name ~* :regex
""",
					regex=regex)
		
		else:
			rows = app.db.execute("""
SELECT *
FROM Products
WHERE name ~* :regex AND type_id = :type_id
""",
					regex=regex,
					type_id=type_id)			

		if len(rows) == 0:
			return None

		return [Product(*row) for row in rows]

	@staticmethod
	def get_all_types():
		rows = app.db.execute('''
SELECT *
FROM Product_type
''')
		return [(row[0], row[1]) for row in rows]
