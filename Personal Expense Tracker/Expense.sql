create database Expense;
use Expense;

CREATE TABLE tracking(
    id INTEGER PRIMARY KEY auto_increment,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL
);
