CREATE DATABASE IF NOT EXISTS phishing_db;
USE phishing_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scan_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id_ph INT NOT NULL,
    user_id INT NOT NULL,
    url VARCHAR(500),
    is_phishing BOOLEAN DEFAULT FALSE,
    confidence_score INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_scan_results
        FOREIGN KEY (user_id_ph)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_scan_results_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE INDEX ix_scan_results_url
    ON scan_results(url);
    
select * from users;

