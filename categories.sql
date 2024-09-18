-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS take_a_bite_db;

-- Use the created database
USE take_a_bite_db;

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS categories (
    id CHAR(36) NOT NULL PRIMARY KEY,  -- Assuming you're using UUIDs as IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    name VARCHAR(128) NOT NULL UNIQUE
);

-- Insert categories only if they do not already exist
INSERT INTO categories (id, name)
SELECT '1e3b8f8b-5509-4c1e-812e-1c7e26d9a58b', 'Breakfast'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Breakfast');

INSERT INTO categories (id, name)
SELECT '4d4e1d1b-1b1b-4e1c-b2d8-fdfd23c1b3b4', 'Lunch'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Lunch');

INSERT INTO categories (id, name)
SELECT '6a5b8f9c-3b3c-4a6d-8b7e-2d9a0e8bfae6', 'Desserts'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Desserts');

INSERT INTO categories (id, name)
SELECT '8c7d9b6a-4f3e-4b1d-8d1f-3b8e6d1e0a8d', 'Beverages'
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name = 'Beverages');
