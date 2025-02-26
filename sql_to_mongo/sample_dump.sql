-- Create Users Table
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

-- Insert Data into Users
INSERT INTO users (id, name, email) VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com'),
(3, 'Charlie', 'charlie@example.com');

-- Create Orders Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    status VARCHAR(50)
);

-- Insert Data into Orders
INSERT INTO orders (order_id, user_id, amount, status) VALUES
(101, 1, 250.50, 'Completed'),
(102, 2, 99.99, 'Pending'),
(103, 3, 450.00, 'Shipped');

-- Create Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

-- Insert Data into Products
INSERT INTO products (product_id, name, price) VALUES
(1001, 'Laptop', 75000.00),
(1002, 'Mouse', 1500.50),
(1003, 'Keyboard', 2500.00);
