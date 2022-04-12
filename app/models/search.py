from flask import current_app as app

from .product import Product

class Search:
	def __init__(self):
		pass

	@staticmethod
	def search_product(search_kw):
		kw_list = search_kw.split(" ")

		regex = '''{d}'''.format(d='|'.join(kw_list))
	
		rows = app.db.execute("""
SELECT *
FROM Products
WHERE name ~* :regex
""",
					regex=regex)
		
		print(rows)
		if len(rows) == 0:
			return None

		return [Product(*row) for row in rows]

