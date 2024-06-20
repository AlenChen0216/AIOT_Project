use AIOT;
show full tables;
SET SQL_SAFE_UPDATES = 0;
#delete  from `merchantransporting`;
create table `carStatus`(
	`carID` varchar(10),
    `status` varchar(20),
    `taskID` varchar(20),
    `accomodate` int
);
describe `tasksinglerow`;
describe `carstatus`;
alter table `merchantransporting` column add ;
select * from `merchantransporting`;
delete from `merchantransporting`;
select * from `tasktransporting`;
delete from `tasktransporting`;
update `tasksinglerow` set `executed`=0 where `executed`=2;
update `carstatus` set `status`='idle' where `status`='busy';
select * from `carstatus`;
drop table `carstatus`;
create table `carstatus`(
	`carid` varchar(10),
    `status` varchar(10),
    `taskID` varchar(20),
    `accomodate` varchar(20),
    `cartype` int
);
insert into `carstatus` values('0','busy','-1',5,0);
insert into `tasktransporting` values('1','1','1');
select * from `tasktransporting` where `taskid`='1' and `merchanid`='1';
describe `merchantransporting`;
drop table `merchantransporting`;
create table `merchantransporting`(
	`merchan` varchar(20),
    `quantity` int
);
select * from `tasksinglerow`;
select * from `carstatus`;
insert into `carstatus` values('0','idle','-1',5);
describe `carstatus`;
select * from `tasksinglerow` where `executed`=0;
describe `tasktransporting`;
describe `merchantransporting`;
flush privileges;
#alter table `tasktransporting` add `quantity` int;
select * from mysql.user; 
ALTER USER 'root'@'localhost' WITH MAX_QUERIES_PER_HOUR 0;
insert into `id2remain` values('2',3);