CREATE DATABASE House_db;
USE House_db;

select * FROM users;

select * FROM predictions;
ALTER TABLE predictions DROP COLUMN created_at;
ALTER TABLE predictions DROP COLUMN price;


INSERT INTO users (name, email, password) VALUES
('Ishaan Khanna', 'ishaan.khanna21@gmail.com', 'Ishaan@123'),
('Ritika Jain', 'ritika.jain34@yahoo.com', 'Ritika#456'),
('Aditya Nair', 'aditya.nair56@gmail.com', 'Aditya@789'),
('Meera Iyer', 'meera.iyer78@outlook.com', 'Meera#321'),
('Siddharth Malhotra', 'siddharth.malhotra90@gmail.com', 'Sid@654'),
('Kavya Reddy', 'kavya.reddy11@yahoo.com', 'Kavya#987'),
('Arjun Das', 'arjun.das22@gmail.com', 'Arjun@111'),
('Nisha Kulkarni', 'nisha.kulkarni33@outlook.com', 'Nisha#222'),
('Manish Yadav', 'manish.yadav44@gmail.com', 'Manish@333'),
('Divya Bansal', 'divya.bansal55@yahoo.com', 'Divya#444');


INSERT INTO predictions
(user_id, area, bedrooms, bathrooms, predicted_price, guest_room, basement, air_conditioning, parking, furnishing_status, city, state)
VALUES
(2, 1500, 2, 2, 4800000, 'no', 'no', 'no', 1, 'unfurnished', 'Surat', 'Gujarat'),
(3, 1500, 3, 1, 4500000, 'no', 'no', 'no', 0, 'unfurnished', 'Rajkot', 'Gujarat'),
(1, 1500, 4, 3, 7000000, 'no', 'no', 'no', 2, 'unfurnished', 'Ahmedabad', 'Gujarat');

INSERT INTO contacts (name, email, subject, message) VALUES
('Aarav Patel', 'aarav.patel@gmail.com', 'Property Inquiry', 'I am interested in a 2BHK apartment. Please share more details.'),
('Riya Sharma', 'riya.sharma@yahoo.com', 'Site Visit Request', 'Can I schedule a visit this weekend for the listed property?'),
('Sneha Verma', 'sneha.verma@gmail.com', 'Loan Assistance', 'Do you provide any home loan assistance or guidance?'),
('Rajesh Kumar', 'rajesh.kumar@yahoo.com', 'Availability Check', 'Is the property still available or already sold?');


INSERT INTO contacts (name, email, subject, message) VALUES
('Aditya Shah', 'aditya.shah@gmail.com', 'Property Details', 'Please send complete details of the property including amenities.'),
('Neha Joshi', 'neha.joshi@yahoo.com', 'Visit Appointment', 'I would like to book a visit for tomorrow evening.'),
('Vikram Singh', 'vikram.singh@outlook.com', 'Budget Inquiry', 'Do you have options available under my budget range?'),
('Pooja Desai', 'pooja.desai@gmail.com', 'Location Info', 'Can you share exact location and nearby facilities?'),
('Manish Gupta', 'manish.gupta@yahoo.com', 'Loan Query', 'Is there any bank tie-up for easy loan approval?'),
('Anjali Mehta', 'anjali.mehta@gmail.com', 'Availability', 'Is the 3BHK flat still available?'),
('Amit Choudhary', 'amit.choudhary@outlook.com', 'Builder Info', 'Can you provide details about the builder reputation?'),
('Sonal Bansal', 'sonal.bansal@gmail.com', 'Legal Documents', 'Are all legal documents clear and verified?');

INSERT INTO predictions
(user_id, area, bedrooms, bathrooms, predicted_price, guest_room, basement, air_conditioning, parking, furnishing_status, city, state)
VALUES
(11, 950, 2, 1, 3500000.00, 'no', 'no', 'no', 1, 'unfurnished', 'Lucknow', 'Uttar Pradesh'),
(12, 1600, 3, 2, 7500000.00, 'yes', 'no', 'yes', 2, 'furnished', 'Hyderabad', 'Telangana'),
(13, 1250, 2, 2, 5200000.00, 'no', 'no', 'yes', 1, 'semi-furnished', 'Indore', 'Madhya Pradesh'),
(22, 1550, 3, 2, 7200000.00, 'yes', 'no', 'yes', 1, 'furnished', 'Amritsar', 'Punjab'),
(23, 900, 2, 1, 3000000.00, 'no', 'no', 'no', 0, 'unfurnished', 'Agra', 'Uttar Pradesh'),
(24, 1750, 3, 3, 8500000.00, 'yes', 'yes', 'yes', 2, 'furnished', 'Coimbatore', 'Tamil Nadu');

INSERT INTO property_enquiries
(name, email, phone, property_type, city, budget, bedrooms, message)
VALUES
('Aarav Patel', 'aarav.patel@gmail.com', '9876543210', 'Apartment', 'Ahmedabad', '50-70 Lakhs', '2', 'Looking for a family home.'),
('Riya Sharma', 'riya.sharma@yahoo.com', '9823456781', 'Villa', 'Surat', '80-120 Lakhs', '3', 'Need a spacious villa.'),
('Kunal Mehta', 'kunal.mehta@outlook.com', '9898765432', 'Apartment', 'Vadodara', '30-50 Lakhs', '2', ''),
('Sneha Verma', 'sneha.verma@gmail.com', '9811122233', 'Independent House', 'Mumbai', '1-2 Cr', '3', 'Prefer near station.'),
('Suresh Patel', 'suresh.patel@yahoo.com', '9654321098', 'Independent House', 'Ahmedabad', '70-90 Lakhs', '3', 'Need parking space.'),
('Sonal Bansal', 'sonal.bansal@gmail.com', '8543210987', 'Apartment', 'Chandigarh', '70-100 Lakhs', '3', 'Ready to buy soon.');

-- ============================================================
-- Jyesta Corporate Entity – Database Setup
-- Run this file in MySQL to create all required tables
-- ============================================================

CREATE DATABASE IF NOT EXISTS House_db;
USE House_db;

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Users table (with email + created_at)
CREATE TABLE IF NOT EXISTS users (
    user_id    INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL,
    email      VARCHAR(150) UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table (with created_at)
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT NOT NULL,
    area             DOUBLE NOT NULL,
    bedrooms         INT NOT NULL,
    bathrooms        INT NOT NULL,
    guest_room       VARCHAR(5) DEFAULT 'no',
    basement         VARCHAR(5) DEFAULT 'no',
    air_conditioning VARCHAR(5) DEFAULT 'no',
    parking          INT DEFAULT 0,
    furnishing_status VARCHAR(30),
    city             VARCHAR(100),
    state            VARCHAR(100),
    predicted_price  DECIMAL(15,2) NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pred_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE
);

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL,
    subject    VARCHAR(255),
    message    TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Property enquiries table
CREATE TABLE IF NOT EXISTS property_enquiries (
    enquiry_id    INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL,
    phone         VARCHAR(20),
    property_type VARCHAR(100),
    city          VARCHAR(100),
    budget        VARCHAR(100),
    bedrooms      VARCHAR(20),
    amenities     TEXT,
    message       TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- About sections table
CREATE TABLE IF NOT EXISTS about_sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    title      VARCHAR(255) NOT NULL,
    body       TEXT,
    image_path VARCHAR(255) DEFAULT '',
    sort_order INT DEFAULT 0
);

-- ── Seed Data ────────────────────────────────────────────────
-- Default admin  (password: admin123)
INSERT IGNORE INTO admin (username, password)
VALUES ('admin', '$2b$12$ix7gAHb8gPNUMRpEyuMO5eXGPuT7V2qUqk5e9S.B3A6rCWkNbMkHy');
-- NOTE: The hash above is for 'admin123'.
-- To set a new admin password run: python set_admin_password.py

-- Sample about sections
INSERT IGNORE INTO about_sections (title, body, sort_order) VALUES
('Who We Are', 'Jyesta Corporate Entity is a technology-driven real estate analytics platform providing house price predictions across 20 major Indian cities using data science and regression modelling.', 1),
('Our Mission', 'To make real estate pricing transparent and accessible to every Indian homebuyer by providing accurate, instant price estimates powered by machine learning.', 2),
('Our Technology', 'Our prediction engine uses Linear Regression trained on thousands of real property transactions. Inputs like area, BHK, bathrooms, amenities, and city are used to compute a reliable price estimate.', 3);

select * from predictions;
