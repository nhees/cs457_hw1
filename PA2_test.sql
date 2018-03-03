--CS457 PA2

--Construct the database and table (0 points; expected to work from PA1)
CREATE DATABASE db1;
USE db1;
CREATE TABLE Product (pid int, name varchar(20), price float);

--Insert new data (20 points)
insert into Product values(1,	'Gizmo',      	19.99);
insert into Product values(2,	'PowerGizmo', 	29.99);
insert into Product values(3,	'SingleTouch', 	149.99);
insert into Product values(4,	'MultiTouch', 	199.99);
insert into Product values(5,	'SuperGizmo', 	49.99);

select * from Product;

--Modify data (20 points)
update Product 
set name = 'Gizmo' 
where name = 'SuperGizmo';

update Product 
set price = 14.99 
where name = 'Gizmo';

select * from Product;

--Delete data (20 points)
delete from Product 
where name = "Gizmo";

delete from Product 
where price > 150;

select * from Product;

--Query subsets (10 points)
select name, price 
from Product 
where pid != 3;

.exit

-- Expected output
--
-- Database CS457_PA2 created.
-- Using database CS457_PA2.
-- Table Product created.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- pid int|name varchar(20)|price float
-- 1|Gizmo|19.99
-- 2|PowerGizmo|29.99
-- 3|SingleTouch|149.99
-- 4|MultiTouch|199.99
-- 5|SuperGizmo|49.99
-- 1 record modified.
-- 2 records modified.
-- pid int|name varchar(20)|price float
-- 1|Gizmo|14.99
-- 2|PowerGizmo|29.99
-- 3|SingleTouch|149.99
-- 4|MultiTouch|199.99
-- 5|Gizmo|14.99
-- 2 records deleted.
-- 1 record deleted.
-- pid int|name varchar(20)|price float
-- 2|PowerGizmo|29.99
-- 3|SingleTouch|149.99
-- name varchar(20)|price float
-- SingleTouch|149.99
-- All done.