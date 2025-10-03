create database norma_prac;
use norma_prac;

create table badOrders(
	order_id int Primary key,
    order_date date,
    customer_id VARCHAR(200),
    customer_name VARCHAR(50),
    customer_city VARCHAR(50),
    product_id VARCHAR(200),
    product_name VARCHAR(200),
    unit_prices VARCHAR(200),
    quantities VARCHAR(200),
    order_total decimal(10,2)
);
INSERT INTO BadOrders VALUES
-- order_id, date, cust, name, city,     pids,      pnames, prices,        qtys,    total
(101, '2025-09-01', 1, 'Rahul', 'Mumbai', '1,3','Laptop,Headphones','60000,2000',  '1,2',   64000.00),
(102, '2025-09-02', 2, 'Priya', 'Delhi',  '2','Smartphone', '30000','1',     30000.00);


-- Creating 1NF
create table Orders_1nf(
	order_id int primary key,
    order_date	date,
    customer_id int,
    customer_name varchar(50),
    customer_city varchar(50)
);

CREATE TABLE OrderItems_1nf (
    order_id INT,
    line_no INT,
    product_id INT,
    product_name VARCHAR(50),
    unit_price DECIMAL(10,2),
    quantity INT,
    PRIMARY KEY (order_id, line_no),
    FOREIGN KEY (order_id) REFERENCES Orders_1nf(Order_id)
);

INSERT INTO Orders_1nf
SELECT order_id, order_date, customer_id, customer_name, customer_city
FROM BadOrders;

-- Order 101 had 2 items
INSERT INTO OrderItems_1nf VALUES 
(101, 1, 1, 'laptop', 60000, 1),
(101, 2, 3, 'Headphone', 2000 , 2);

-- Order 102 had 1 item
INSERT INTO OrderItems_1nf VALUES
(102, 1, 2, 'Smartphone', 30000 , 1);

