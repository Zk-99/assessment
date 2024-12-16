-- create database
CREATE DATABASE sales_data;
USE sales_data;

-- create sales table
CREATE TABLE sales (
    transaction_date DATETIME,
    sales_qty INT,
    product_code VARCHAR(10),
    store_code VARCHAR(10),
    PRIMARY KEY (transaction_date, product_code, store_code)
);

-- create product table
CREATE TABLE product (
    product_code VARCHAR(10) PRIMARY KEY,
    product_description VARCHAR(255),
    product_category VARCHAR(100),
    cost FLOAT,
    price FLOAT
);

-- create store table
CREATE TABLE store (
    store_code VARCHAR(10) PRIMARY KEY,
    store_name VARCHAR(255),
    store_region VARCHAR(100)
);

-- insert data into sales table
INSERT INTO sales (transaction_date, sales_qty, product_code, store_code) VALUES
('2024-01-01', 120, 'P001', 'S001'),
('2024-01-02', 85, 'P002', 'S002'),
('2024-01-03', 50, 'P003', 'S003'),
('2024-01-04', 110, 'P004', 'S004'),
('2024-01-05', 75, 'P005', 'S005'),
('2024-01-06', 95, 'P006', 'S006'),
('2024-01-07', 200, 'P007', 'S007'),
('2024-01-08', 180, 'P008', 'S008'),
('2024-01-09', 65, 'P009', 'S009'),
('2024-01-10', 150, 'P010', 'S010'),
('2024-01-11', 130, 'P011', 'S001'),
('2024-01-12', 90, 'P012', 'S002'),
('2024-01-13', 140, 'P013', 'S003'),
('2024-01-14', 120, 'P014', 'S004'),
('2024-01-15', 60, 'P015', 'S005'),
('2024-01-16', 175, 'P016', 'S006'),
('2024-01-17', 115, 'P017', 'S007'),
('2024-01-18', 160, 'P018', 'S008'),
('2024-01-19', 105, 'P019', 'S009'),
('2024-01-20', 155, 'P020', 'S010');

-- insert data into product table
INSERT INTO product (product_code, product_description, product_category, cost, price) VALUES
('P001', 'Product 1', 'Electronics', 40, 80),
('P002', 'Product 2', 'Clothing', 30, 60),
('P003', 'Product 3', 'Groceries', 10, 20),
('P004', 'Product 4', 'Electronics', 50, 100),
('P005', 'Product 5', 'Clothing', 25, 50),
('P006', 'Product 6', 'Groceries', 15, 30),
('P007', 'Product 7', 'Electronics', 60, 120),
('P008', 'Product 8', 'Clothing', 20, 40),
('P009', 'Product 9', 'Groceries', 12, 24),
('P010', 'Product 10', 'Electronics', 70, 140),
('P011', 'Product 11', 'Clothing', 35, 70),
('P012', 'Product 12', 'Groceries', 18, 36),
('P013', 'Product 13', 'Electronics', 45, 90),
('P014', 'Product 14', 'Clothing', 28, 56),
('P015', 'Product 15', 'Groceries', 22, 44),
('P016', 'Product 16', 'Electronics', 65, 130),
('P017', 'Product 17', 'Clothing', 32, 64),
('P018', 'Product 18', 'Groceries', 20, 40),
('P019', 'Product 19', 'Electronics', 55, 110),
('P020', 'Product 20', 'Clothing', 38, 76);

-- insert data into store table
INSERT INTO store (store_code, store_name, store_region) VALUES
('S001', 'Store 1', 'North'),
('S002', 'Store 2', 'South'),
('S003', 'Store 3', 'East'),
('S004', 'Store 4', 'West'),
('S005', 'Store 5', 'Central'),
('S006', 'Store 6', 'North'),
('S007', 'Store 7', 'South'),
('S008', 'Store 8', 'East'),
('S009', 'Store 9', 'West'),
('S010', 'Store 10', 'Central');