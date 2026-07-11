<?php
// Database connection settings — update these to match your MySQL setup
$DB_HOST = "localhost";
$DB_NAME = "Expense";
$DB_USER = "root";
$DB_PASS = "";

try {
    $pdo = new PDO(
        "mysql:host=$DB_HOST;dbname=$DB_NAME;charset=utf8mb4",
        $DB_USER,
        $DB_PASS,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}

/*
Actual schema (from Expense.sql):

CREATE TABLE reg (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    password VARCHAR(255) NOT NULL,   -- widened from 25, see fix below
    contact_no VARCHAR(15) NOT NULL,  -- widened from INT, see fix below
    email VARCHAR(25) NOT NULL
);

CREATE TABLE tracking (
    tracking_id INT PRIMARY KEY AUTO_INCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    id INT NOT NULL,                  -- foreign key -> reg(id), i.e. the user who owns this row
    FOREIGN KEY (id) REFERENCES reg(id)
);

REQUIRED FIXES — run these once in phpMyAdmin / MySQL CLI:

ALTER TABLE reg MODIFY password VARCHAR(255) NOT NULL;
ALTER TABLE reg MODIFY contact_no VARCHAR(15) NOT NULL;
*/
