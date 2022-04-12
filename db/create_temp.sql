DROP TABLE User_browsing_history;

CREATE TABLE User_browsing_history (
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    view_times INT NOT NULL,
    last_view_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);