DROP TABLE Balance;

CREATE TABLE Balance (
    trans_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    trans_date DATE DEFAULT CURRENT_TIMESTAMP,
    id INT NOT NULL,
    trans FLOAT DEFAULT 0,
    balance FLOAT DEFAULT 0
    
);

INSERT INTO Balance (trans_id, trans_date, id, trans, balance)
VALUES (1, '2019-02-23 20:02:21.550', 1, 0, 0);

INSERT INTO Balance (trans_id, trans_date, id, trans, balance)
VALUES (2, '2020-02-23 20:02:21.550', 1, 20, 20);

INSERT INTO Balance (trans_id, trans_date, id, trans, balance)
VALUES (3, '2020-02-23 20:02:21.550', 2, 50, 50);