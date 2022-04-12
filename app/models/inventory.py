from flask import current_app as app


class Inventory:
    def __init__(self, id, seller_id, name, price, units_avail, available):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.price = price        
        self.units_avail = units_avail
        self.available = available

# display inventory information
    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE seller_id = :seller_id 
ORDER BY product_id DESC
''',
                              seller_id=seller_id)
        if rows is None:
            return None
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_product(product_id, seller_id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE product_id=:product_id AND seller_id = :seller_id 
''',
                              product_id = product_id,
                              seller_id=seller_id)
        if rows is None:
            return None
        return [Inventory(*row) for row in rows]        
        
# add inventory
    @staticmethod
    def add_product(seller_id, name, price, units_avail, available):
        try:
            rows = app.db.execute("""
INSERT INTO Products(seller_id, name, price, units_avail, available)
VALUES(:seller_id, :name, :price, :units_avail, :available)
""",
                                  seller_id = seller_id,
                                  name = name,
                                  price=price,
                                  units_avail = units_avail,
                                  available = available)
            
            product_id = rows[0][0]
            if rows is None:
                return None
            
            return [Inventory(*row) for row in rows]
        
        except Exception as e:
            print(str(e))
            return None 

# delete inventory item 
    @staticmethod
    def delete_product(product_id, seller_id):
        product_delete = app.db.execute('''
DELETE 
FROM Products
WHERE seller_id=:seller_id AND product_id=:product_id
''',
					seller_id=seller_id,
					product_id=product_id)
        return product_delete

# update inventory units_avail and price manually by seller
    @staticmethod
    def update(product_id, seller_id, price, units_avail,available):
        res = app.db.execute('''
UPDATE Products
SET price =:price, units_avail=:units_avail, available=:available
WHERE product_id=:product_id AND seller_id=:seller_id
''',
					seller_id=seller_id,
					product_id=product_id,
                    price=price,
                    units_avail=units_avail,
                    available=available)
        return res   


# change order status, once completed, inventory is naturally reduced


# inventory analytics
    @staticmethod
    def product_with_limited_inventory(seller_id, limited_stock):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE seller_id = :seller_id AND units_avail<=:limited_stock
''',
                              seller_id=seller_id,
                              limited_stock=limited_stock)
        if rows is None:
            return None
        return [Inventory(*row) for row in rows]     

