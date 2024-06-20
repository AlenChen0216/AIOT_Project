create database `AIOT`;
use AIOT;
create table `carstatus`(
	`carid` varchar(10),
    `status` varchar(10),
    `taskid` varchar(20),
    `accomodate` varchar(20),
    `cartype` int
);
create table  `id2remain`(
	`id` varchar(20),
    `remain` int
);
create table `merchantransporting`(
	`merchan` varchar(20),
    `quantity` int
);
create table `tasksinglerow`(
	`taskid` varchar(20),
    `merchanid` varchar(20),
    `quantity` int,
    `executed` int
);
create table  `tasktransporting`(
	`taskid` varchar(20),
    `merchanid` varchar(20),
    `quantity` int
);
/*ALTER USER 'root'@'localhost' WITH MAX_UPDATES_PER_HOUR 0;
FLUSH PRIVILEGES;
show full tables;
SET SQL_SAFE_UPDATES = 0;
delete from `tasksinglerow`;
describe `tasksinglerow`;
describe `tasktransporting`;
describe `merchantransporting`;
describe `carstatus`;
describe `id2remain`;
select * from `tasksinglerow`;
select * from `tasktransporting`;
delete from `tasktransporting`;
delete from `merchantransporting`;
delete from `tasksinglerow` where `taskid`=19;
update `tasksinglerow` set `executed`=0;
update `carstatus` set `status`='idle';
select * from `tasktransporting`;
select * from `merchantransporting`;
delete from `id2remain`;
insert into `id2remain` values('0',999);
select * from `carstatus`;
delete from `carstatus`;
insert into `carstatus` values('J1','idle','-1',999,0);
insert into `tasksinglerow` values('0','0','5','0');
update `tasksinglerow` set `taskid`=0 where `taskid`=;

create table `carstatus`(
	`carid` varchar(10),
    `status` varchar(10),
    `taskID` varchar(20),
    `accomodate` varchar(20),
    `cartype` int
);
create table `merchantransporting`(
	`merchan` varchar(20),
    `quantity` int
);
create table `id2remain`(
	`id` varchar(20),
    `remain` int
);
create table `tasksinglerow`(
	`taskid` varchar(20),
    `merchanid` varchar(20),
    `quantity` int,
    `executed` int
);
create table `tasktransporting`(
	`taskid` varchar(20),
    `merchanid` varchar(20),
    `quantity` int
);
describe `id2remain`;
insert into `carstatus` values('0','busy','-1',5,0);
insert into `tasktransporting` values('1','1','1');
select * from `tasktransporting` where `taskid`='1' and `merchanid`='1';
select * from `carstatus`;
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
insert into `id2remain` values('2',3);*/