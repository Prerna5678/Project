CREATE DATABASE IF NOT EXISTS phishing_db;
USE phishing_db;

CREATE TABLE IF NOT EXISTS scan_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(500),
    is_phishing BOOLEAN DEFAULT FALSE,
    confidence_score INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_scan_results_id ON scan_results(id);
CREATE INDEX ix_scan_results_url ON scan_results(url);
