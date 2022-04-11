from flask import current_app as app


class Inventory:
    def __init__(self, id, uid, name, price, quantity, available):
        self.id = id
        self.uid = uid
        self.name = name
        self.price = price        
        self.quantity = quantity
        self.available = available

# display inventory information
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE uid = :uid 
ORDER BY id DESC
''',
                              uid=uid)
        if rows is None:
            return None
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_product(pid, uid):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE id=:pid AND uid = :uid 
''',
                              pid = pid,
                              uid=uid)
        if rows is None:
            return None
        return [Inventory(*row) for row in rows]        
        
# add inventory
    @staticmethod
    def add_product(uid, name, price, quantity, available):
        try:
            rows = app.db.execute("""
INSERT INTO Products(uid, name, price, quantity, available)
VALUES(:uid, :name, :price, :quantity, :available)
RETURNING id 
""",
                                  uid = uid,
                                  name = name,
                                  price=price,
                                  quantity = quantity,
                                  available = available)
            pid = rows[0][0]
            if rows is None:
                return None
            return [Inventory(*row) for row in rows]
        except Exception as e:
            print(str(e))
            return None 

# delete inventory item 
    @staticmethod
    def delete_product(pid, uid):
        product_delete = app.db.execute('''
DELETE 
FROM Products
WHERE uid=:uid AND id=:pid
''',
					uid=uid,
					pid=pid)
        return product_delete

# update inventory quantity and price manually by seller
    @staticmethod
    def update(pid, uid, price, quantity,available):
        res = app.db.execute('''
UPDATE Products
SET price =:price, quantity=:quantity, available=:available
WHERE id=:pid AND uid=:uid
''',
					uid=uid,
					pid=pid,
                    price=price,
                    quantity=quantity,
                    available=available)
        return res   


# change order status, once completed, inventory is naturally reduced


# inventory analytics
    @staticmethod
    def product_with_limited_inventory(uid, limited_stock):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE uid = :uid AND quantity<=:limited_stock
''',
                              uid=uid,
                              limited_stock=limited_stock)
        if rows is None:
            return None
        return [Inventory(*row) for row in rows]     

