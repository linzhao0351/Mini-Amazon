from flask import current_app as app


class Inventory:
    def __init__(self, id, seller_id, name, price, units_avail, available, short_desc, long_desc, type_id, ptype):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.price = price        
        self.units_avail = units_avail
        self.available = available
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.type_id = type_id
        self.ptype = ptype

# display inventory information
    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT P.*, T.ptype
FROM Products AS P, Product_type AS T
WHERE P.seller_id = :seller_id AND P.type_id = T.type_id
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
    def add_product(seller_id, name, price, units_avail, available, short_desc, long_desc, type_id):
        try:
            rows = app.db.execute("""
INSERT INTO Products(seller_id, name, price, units_avail, available, short_desc, long_desc, type_id)
VALUES(:seller_id, :name, :price, :units_avail, :available, :short_desc, :long_desc, :type_id)
""",
                                  seller_id = seller_id,
                                  name = name,
                                  price=price,
                                  units_avail = units_avail,
                                  available = available,
                                  short_desc=short_desc,
                                  long_desc=long_desc,
                                  type_id=type_id)
            
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
    def update(product_id, seller_id, price, units_avail,available,short_desc,long_desc,type_id):
        res = app.db.execute('''
UPDATE Products
SET price =:price, units_avail=:units_avail, available=:available, short_desc=:short_desc, long_desc=:long_desc, type_id=:type_id
WHERE product_id=:product_id AND seller_id=:seller_id
''',
					seller_id=seller_id,
					product_id=product_id,
                    price=price,
                    units_avail=units_avail,
                    available=available,
                    short_desc=short_desc,
                    long_desc=long_desc,
                    type_id=type_id)
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

