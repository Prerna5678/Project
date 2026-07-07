create database Expense;
use Expense;

create table reg(
id int primary key auto_increment,
name varchar(25) not null,
password varchar(25) not null
);

create table login(
login_id int primary key auto_increment,
name varchar(25) not null,
password varchar(25) not null
);

CREATE TABLE tracking(
    tracking_id INTEGER PRIMARY KEY auto_increment,
    date TEXT not null,
    category TEXT not null,
    description TEXT not null,
    amount REAL not null
	
);

ALTER TABLE login
ADD COLUMN id INT NOT NULL,
ADD CONSTRAINT fk_login_user
FOREIGN KEY (id) REFERENCES reg(id);

ALTER TABLE tracking
ADD COLUMN id INT NOT NULL,
ADD CONSTRAINT fk_tracking_user
FOREIGN KEY (id) REFERENCES reg(id);

ALTER TABLE REG
ADD column contact_no int not null;

ALTER TABLE REG
ADD column email varchar(25) not null;

select * from tracking;

select * from reg;