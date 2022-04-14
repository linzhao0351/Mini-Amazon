from flask import current_app as app


class Product:
    def __init__(self, product_id, seller_id, name, price, units_avail, available, short_desc, long_desc):
        self.product_id = product_id
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.units_avail = units_avail
        self.available = available
        self.short_desc = short_desc
        self.long_desc = long_desc

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available AND units_avail > 0
''',
                            available=available)
        return [Product(*row) for row in rows]
