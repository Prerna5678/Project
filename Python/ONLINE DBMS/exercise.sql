create database company;
use company;

create table Dept(
Dept_id int primary Key,
Dept_name varchar(25) unique not null,
location varchar(25)
);

create table Emp(
Emp_id int primary key,
name varchar(25) not null,
email varchar(25) unique not null,
salary DECIMAL(10,2), CHECK (salary > 0),
Dept_id int not null,
FOREIGN KEY (Dept_id) REFERENCES Dept(Dept_id)
);

--  3.Insert at least 3 departments (HR, IT, Finance) into departments
insert into Dept values(1,"HR","Vapi");
insert into Dept values(2,"Finance","Surat");
insert into Dept values(3,"IT","Valsad");


-- 4.Insert 5 employees with varying departments. At least two should have the same name “Ajay” but different emails.
insert into Emp values
(1,"Ajay","ajay@gmail.com",55000,1),
(2,"Ajay","ajay1@gmail.com",23900,1),
(3,"Priya","priya@gmail.com",15000,1),
(4,"Riya","riya@gmail.com",17000,1),
(5,"Rajkamal","rajkamal@gmail.com",10000,1);

select * from Emp;

-- 5.Add a new column phone (varchar 15) to the employees table.
alter table Emp add phone varchar(15);

-- 6. Rename phone column to contact_no


-- 7.  Modify the size of contact_no column to varchar(20).


-- 9. Update the salary of all employees named “Ajay” in the HR department to 55000. 
update Emp
set salary=55000
where Emp_id=1;

-- 10. Delete all employees from the Finance department. 
Delete from Dept where Dept_name="Finance";

-- 11. Show all employees not in the IT department. 
select * from Dept where Dept_name != "IT";

-- 12. Show all employees who are in IT or HR department.
select * from Dept where Dept_name ="IT" or Dept_name ="HR";

-- 13.  Delete all rows from employees without dropping the table
delete from Emp;

