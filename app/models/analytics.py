from flask import current_app as app

class Analytics:
    def __init__(self):
        pass

    @staticmethod
    def get_trendy_prod(seller_id):
        rows = app.db.execute('''
SELECT A.product_id, A.sales, B.name, B.units_avail
FROM        
(SELECT product_id, SUM(quantity) AS sales
FROM (SELECT T1.*, T2.ts
        FROM Orders AS T1, Orders_summary AS T2
        WHERE T1.seller_id = :seller_id AND T1.order_id = T2.order_id) AS T
WHERE ts > CURRENT_DATE - INTERVAL '3 months'
GROUP BY product_id) AS A, Products AS B
WHERE B.product_id = A.product_id
ORDER BY A.sales DESC
LIMIT 5
''',
                    seller_id=seller_id)
        
        return rows