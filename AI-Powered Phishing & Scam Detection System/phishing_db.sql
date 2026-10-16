CREATE DATABASE IF NOT EXISTS phishing_db;
USE phishing_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
    
select * from users;



