create database retailDB;
use retailDB;

create table customer(
	customer_id int auto_increment primary key,
    name varchar(50),
    city varchar(50),
    phone varchar(15)
);

create table product(
	product_id int auto_increment primary key,
    product_name varchar(50),
    category varchar(50),
    price decimal(10,2)
);

create table orders(
	order_id int auto_increment primary key,
    customer_id int,
    order_date date,
    foreign key(customer_id) references customer(customer_id)
);

create table orderDetails(
	order_detail_id int auto_increment primary key,
    order_id int,
    product_id int,
    quantity int,
    foreign key(order_id) references orders(order_id),
    foreign key(product_id) references product(product_id)
);

-- INSERTION

INSERT INTO Customer (name, city, phone) VALUES
('Rahul', 'Mumbai', '9876543210'),
('Priya', 'Delhi', '9876501234'),
('Arjun', 'Bengaluru', '9876512345'),
('Neha', 'Hyderabad', '9876523456');


INSERT INTO Product (product_name, category, price) VALUES
('Laptop', 'Electronics', 60000.00),
('Smartphone', 'Electronics', 30000.00),
('Headphones', 'Accessories', 2000.00),
('Shoes', 'Fashion', 3500.00),
('T-Shirt', 'Fashion', 1200.00);


INSERT INTO Orders (customer_id, order_date) VALUES
(1, '2025-09-01'),
(2, '2025-09-02'),
(3, '2025-09-03'),
(1, '2025-09-04');


INSERT INTO OrderDetails (order_id, product_id, quantity) VALUES
(1, 1, 1),   -- Rahul bought 1 Laptop
(1, 3, 2),   -- Rahul bought 2 Headphones
(2, 2, 1),   -- Priya bought 1 Smartphone
(3, 4, 1),   -- Arjun bought 1 Shoes
(4, 5, 3);   -- Rahul bought 3 T-Shirts

select * from customer;
select * from product;
select * from orders;
select * from orderDetails;

-- Stored Procedure

delimiter $$ -- changes the ending character for a query

create procedure getallprod()
begin
	select product_id, product_name, price, category
    from product;
end$$

delimiter ;
call getallprod();

-- example 2
delimiter $$
create procedure getorder_and_customer()
begin
	select o.order_id, o.order_date, c.name as customer_name
    from
    orders o join customer c on
    o.customer_id = c.customer_id;
end$$

delimiter ;
call getorder_and_customer();

-- example 3
delimiter $$
create procedure get_full_orderDetails()
begin
	select o.order_id, c.name as customer_name, p.product_name, od.quantity, p.price, (p.price * od.quantity) as total
    from orders o
    join customer c on o.customer_id = c.customer_id
    join orderDetails od on o.order_id = od.order_id
    join product p on od.product_id = p.product_id;
end$$

delimiter ;

call get_full_orderDetails();
    
drop procedure if exists get_full_orderDetails;

-- example 4

delimiter $$
CREATE PROCEDURE GetCustomerOrders (IN cust_id int)
BEGIN
SELECT o.order_id,
o.order_date,
p.product_name,
od.quantity,
p.price,
(od.quantity * p.price) AS total
FROM Orders o
JOIN OrderDetails od ON o.order_id = od.order_id
JOIN Product p ON od.product_id = p.product_id
WHERE o.customer_id = cust_id;
END$$

DELIMITER ;
CALL GetCustomerOrders (1);

drop procedure if exists GetCustomerOrders;

-- example 5

delimiter $$
create  procedure get_monthly_sales(in month_no int, in year_no int)
begin
	select MONTH(o.order_date) as month, YEAR(o.order_date) as year, sum(od.quantity * p.price) as total_sales
    from orders o
    join orderDetails od on o.order_id = od.order_id
    join product p  on od.product_id = p.product_id
    where MONTH(o.order_date) = month_no and YEAR(o.order_date) = year_no
    group by month, year;
end$$

delimiter ;
call get_monthly_sales(9, 2025);
drop procedure if exists get_monthly_sales;

-- example 6

delimiter $$
create procedure top_selling_products()
begin
	select p.product_name, sum(od.quantity * p.price) as revenue, sum(od.quantity) as total_sales
    from orderDetails od
    join product p on p.product_id = od.product_id
    group by p.product_id, p.product_name
    order by revenue desc
    limit 3;
end$$

delimiter ;
call top_selling_products();

drop procedure if exists top_selling_products;