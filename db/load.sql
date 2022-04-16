-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:

\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM Products),
                         false);

\COPY Orders_summary FROM 'Orders_summary.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_summary_order_id_seq',
                         (SELECT MAX(order_id)+1 FROM Orders_summary),
                         false);

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV

\COPY User_browsing_history FROM 'User_browsing_history.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Balance FROM 'Balance.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.balance_trans_id_seq',
                         (SELECT MAX(trans_id)+1 FROM Balance),
                         false);

\COPY Current_balance FROM 'Current_balance.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Seller_review FROM 'Seller_review.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.seller_review_review_id_seq',
                         (SELECT MAX(review_id)+1 FROM Seller_review),
                         false);

\COPY Product_review FROM 'Product_review.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.product_review_review_id_seq',
                         (SELECT MAX(review_id)+1 FROM Product_review),
                         false);                         

\COPY Seller_upvotes FROM 'Seller_upvotes.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Upvotes FROM 'Upvotes.csv' WITH DELIMITER ',' NULL '' CSV

\COPY System_messages FROM 'System_messages.csv' WITH DELIMITER ',' NULL '' CSV
