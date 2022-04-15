from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Product_Review:
    def __init__(self, review_id, buyer_id, product_id, review_content, upvote):
        self.review_id = review_id
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.review_content = review_content
        self.upvote = upvote

    @staticmethod
    def get(review_id):
        rows = app.db.execute("""SELECT r.review_id, r.buyer_id, r.product_id, r.review_content, r.upvote
        FROM Product_review AS R
        WHERE r.review_id = :review_id
        """, review_id = review_id)
        if rows is None:
            return None
        return [Product_Review(*row) for row in rows]

    @staticmethod
    def add_review(buyer_id, product_id,review_content, rating, upvote):
        rows = app.db.execute('''INSERT INTO Product_review(buyer_id, product_id, review_content, rating, upvote)
        VALUES(:buyer_id, :product_id, :review_content, :rating, :upvote)
        RETURNING review_id
        ''', 
        review_content = review_content,
        buyer_id = buyer_id,
        product_id = product_id,
        rating = rating,
        upvote = upvote)
        review_id = rows[0][0]
        return Product_Review.get(review_id)

    @staticmethod
    def get_all_reviews(buyer_id):
        rows = app.db.execute('''
        SELECT * FROM Product_review
        WHERE buyer_id = :buyer_id
        ORDER BY review_ts DESC''',
        buyer_id = buyer_id)
        return rows

    @staticmethod
    def get_top_upvotes(product_id):
        rows = app.db.execute('''
        SELECT *
        FROM Product_review
        WHERE product_id = :product_id
        ORDER BY upvote DESC, review_ts DESC
        LIMIT 3
        ''', 
        product_id = product_id)
        return rows
    @staticmethod
    def get_most_recent(product_id):
        rows = app.db.execute('''
        (SELECT * FROM Product_review
        WHERE product_id = :product_id
        ORDER BY review_ts DESC)
        EXCEPT
        (SELECT *
        FROM Product_review
        WHERE product_id = :product_id
        ORDER BY upvote DESC, review_ts DESC
        LIMIT 3)
        ''',
        product_id = product_id)
        return rows

    @staticmethod
    def upvote(user_id, review_id):
        rows = app.db.execute('''
        INSERT INTO upvotes(user_id, review_id) VALUES (:user_id, :review_id)''',
        user_id = user_id, review_id = review_id)
        app.db.execute('''
        UPDATE Product_review 
        SET upvote = upvote + 1
        WHERE review_id = :review_id''', 
        review_id = review_id)
        return rows

    @staticmethod
    def upvote_exists(user_id, review_id):
        rows = app.db.execute('''
        SELECT * FROM upvotes WHERE user_id = :user_id AND review_id = :review_id''',
         user_id = user_id, review_id = review_id)
        return len(rows) > 0

    @staticmethod
    def downvote(user_id, review_id):
        rows = app.db.execute('''
        DELETE FROM upvotes WHERE user_id = :user_id AND review_id = :review_id''',
        user_id = user_id, review_id = review_id)
        app.db.execute('''
        UPDATE Product_review 
        SET upvote = upvote - 1
        WHERE review_id = :review_id''', 
        review_id = review_id)
        return rows

    @staticmethod
    def get_current_review(buyer_id, product_id):
        rows = app.db.execute('''
        SELECT review_content
        FROM Product_review
        WHERE buyer_id = :buyer_id AND product_id = :product_id''',
        buyer_id = buyer_id,
        product_id = product_id)
        return rows

    @staticmethod
    def update_review(buyer_id, product_id, new_content, new_rating):
        rows = app.db.execute('''
        UPDATE Product_review
        SET review_content = :new_content, rating = :new_rating
        WHERE buyer_id = :buyer_id AND product_id = :product_id''',
        new_content = new_content,
        buyer_id = buyer_id,
        product_id = product_id,
        new_rating = new_rating)

    @staticmethod
    def delete_review(buyer_id, product_id):
        rows = app.db.execute('''
        DELETE
        FROM Product_review
        WHERE buyer_id = :buyer_id AND product_id = :product_id''',
        buyer_id = buyer_id,
        product_id = product_id)

    @staticmethod
    def total_reviews(product_id):
        rows = app.db.execute('''
        SELECT * FROM Product_review WHERE product_id = :product_id''', product_id = product_id)
        return len(rows)

    @staticmethod
    def average_rating(product_id):
        rows = app.db.execute('''
        SELECT ROUND(AVG(rating),2) FROM Product_Review WHERE product_id = :product_id''', product_id = product_id)
        return rows[0][0]


    @staticmethod
    def get_all_reviews_seller(seller_id):
        rows = app.db.execute('''
        SELECT P.seller_id, R.*
        FROM Products AS P, Product_review AS R
        WHERE P.seller_id=:seller_id AND R.product_id=P.product_id
        ORDER BY R.review_ts DESC
        ''', seller_id=seller_id)
        return rows

    @staticmethod
    def check_order(buyer_id, product_id):
        rows = app.db.execute('''
        SELECT O.product_id, S.buyer_id
        FROM Orders AS O, Orders_summary AS S
        WHERE O.product_id = :product_id AND S.buyer_id=:buyer_id AND O.order_id=S.order_id
        ''', product_id=product_id, buyer_id=buyer_id)

        if len(rows) == 0:
            return False

        return True



class Seller_Review:
    def __init__(self, review_id, buyer_id, seller_id, review_content, upvote):
        self.review_id = review_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.review_content = review_content
        self.upvote = upvote

    @staticmethod
    def get(review_id):
        rows = app.db.execute("""SELECT r.review_id, r.buyer_id, r.seller_id, r.review_content, r.upvote
        FROM Seller_review AS R
        WHERE r.review_id = :review_id
        """, review_id = review_id)
        if rows is None:
            return None
        return [Seller_Review(*row) for row in rows]

    @staticmethod
    def add_review(buyer_id, seller_id,review_content, rating, upvote):
        rows = app.db.execute('''INSERT INTO Seller_review(buyer_id, seller_id, review_content, rating, upvote)
        VALUES(:buyer_id, :seller_id, :review_content, :rating, :upvote)
        RETURNING review_id
        ''', 
        review_content = review_content,
        buyer_id = buyer_id,
        seller_id = seller_id,
        rating = rating,
        upvote = upvote)
        review_id = rows[0][0]
        return Seller_Review.get(review_id)

    @staticmethod
    def get_all_reviews(buyer_id):
        rows = app.db.execute('''
        SELECT * FROM Seller_review
        WHERE buyer_id = :buyer_id
        ORDER BY review_ts DESC''',
        buyer_id = buyer_id)
        return rows

    @staticmethod
    def get_top_upvotes(seller_id):
        rows = app.db.execute('''
        SELECT *
        FROM Seller_review
        WHERE seller_id = :seller_id
        ORDER BY upvote DESC, review_ts DESC
        LIMIT 3
        ''', 
        seller_id = seller_id)
        return rows
    @staticmethod
    def get_most_recent(seller_id):
        rows = app.db.execute('''
        (SELECT * FROM Seller_review
        WHERE seller_id = :seller_id
        ORDER BY review_ts DESC)
        EXCEPT
        (SELECT *
        FROM Seller_review
        WHERE seller_id = :seller_id
        ORDER BY upvote DESC, review_ts DESC
        LIMIT 3)
        ''',
        seller_id = seller_id)
        return rows

    @staticmethod
    def upvote(user_id, review_id):
        rows = app.db.execute('''
        INSERT INTO seller_upvotes(user_id, review_id) VALUES (:user_id, :review_id)''',
        user_id = user_id, review_id = review_id)
        app.db.execute('''
        UPDATE Seller_review 
        SET upvote = upvote + 1
        WHERE review_id = :review_id''', 
        review_id = review_id)
        return rows

    @staticmethod
    def upvote_exists(user_id, review_id):
        rows = app.db.execute('''
        SELECT * FROM seller_upvotes WHERE user_id = :user_id AND review_id = :review_id''',
         user_id = user_id, review_id = review_id)
        return len(rows) > 0

    @staticmethod
    def downvote(user_id, review_id):
        rows = app.db.execute('''
        DELETE FROM seller_upvotes WHERE user_id = :user_id AND review_id = :review_id''',
        user_id = user_id, review_id = review_id)
        app.db.execute('''
        UPDATE Seller_review 
        SET upvote = upvote - 1
        WHERE review_id = :review_id''', 
        review_id = review_id)
        return rows

    @staticmethod
    def get_current_review(buyer_id, seller_id):
        rows = app.db.execute('''
        SELECT review_content
        FROM Seller_review
        WHERE buyer_id = :buyer_id AND seller_id = :seller_id''',
        buyer_id = buyer_id,
        seller_id = seller_id)
        return rows

    @staticmethod
    def update_review(buyer_id, seller_id, new_content, new_rating):
        rows = app.db.execute('''
        UPDATE Seller_review
        SET review_content = :new_content, rating = :new_rating
        WHERE buyer_id = :buyer_id AND seller_id = :seller_id''',
        new_content = new_content,
        buyer_id = buyer_id,
        seller_id = seller_id,
        new_rating = new_rating)

    @staticmethod
    def delete_review(buyer_id, seller_id):
        rows = app.db.execute('''
        DELETE
        FROM Seller_review
        WHERE buyer_id = :buyer_id AND seller_id = :seller_id''',
        buyer_id = buyer_id,
        seller_id = seller_id)

    @staticmethod
    def total_reviews(seller_id):
        rows = app.db.execute('''
        SELECT * FROM Seller_review WHERE seller_id = :seller_id''', seller_id = seller_id)
        return len(rows)

    @staticmethod
    def average_rating(seller_id):
        rows = app.db.execute('''
        SELECT ROUND(AVG(rating),2) FROM Seller_review WHERE seller_id = :seller_id''', seller_id = seller_id)
        return rows[0][0]

    @staticmethod
    def get_all_reviews_seller(seller_id):
        rows = app.db.execute('''
        SELECT *
        FROM Seller_review
        WHERE seller_id=:seller_id
        ORDER BY review_ts DESC
        ''', seller_id=seller_id)
        return rows

    @staticmethod
    def check_order(buyer_id, seller_id):
        rows = app.db.execute('''
        SELECT O.product_id, S.buyer_id
        FROM Orders AS O, Orders_summary AS S
        WHERE O.seller_id = :seller_id AND S.buyer_id=:buyer_id AND O.order_id=S.order_id
        ''', seller_id=seller_id, buyer_id=buyer_id)

        if len(rows) == 0:
            return False

        return True
