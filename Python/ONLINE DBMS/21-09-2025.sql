create database if not exists company_db;
use company_db;

create table employee
(
emp_id int primary key,
name varchar(50),
hire_date date default(current_date),
probation_end date default '2023-06-01'
);

insert into employee (emp_id,name,hire_date,probation_end) values
(1,'Alice','2022-02-15','2022-08-15'),
(2,'Bob','2021-10-01','2022-04-01'),
(3,'Charlie','2023-01-10','2023-07-10'),
(4,'Diana','2024-03-01','2024-09-01'),
(5,'Ethan',default,defaul
);

Select CURRENT_TIMESTAMP() as employee;
select CURRENT_DATE() as employee;
Select CURRENT_TIME() as employee;
Select DATE_ADD(current_date, INTERVAL 6 month) from employee;
select date_sub("2021-10-01", interval 15 day) as employee;
