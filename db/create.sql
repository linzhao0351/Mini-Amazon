DROP TABLE User_browsing_history;
DROP TABLE Orders;
DROP TABLE Orders_summary;
DROP TABLE User_cart;
DROP TABLE Products;
DROP TABLE Users;

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    product_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    seller_id INT NOT NULL REFERENCES Users(id),
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    units_avail INT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);


CREATE TABLE User_cart (
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Orders_summary (
    order_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12,2) NOT NULL
);


CREATE TABLE Orders (
    order_id INT NOT NULL,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    fulfillment_status INT NOT NULL DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES Orders_summary(order_id)
);


CREATE TABLE User_browsing_history (
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    view_times INT NOT NULL,
    last_view_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);