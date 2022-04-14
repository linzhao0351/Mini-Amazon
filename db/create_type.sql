DROP TABLE Product_type;

CREATE TABLE Product_type (
    type_id INT NOT NULL,
    ptype VARCHAR(255) NOT NULL
);

INSERT INTO Product_type (type_id, ptype)
VALUES (0, 'All'), (1, 'Food'), (2, 'Digital');