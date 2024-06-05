CREATE TABLE zone(
id 			int not null generated always as identity primary key,
name 		varchar(20) not null,
designation varchar(20) not null,
openingdate date not null, 
closingdate date not null,
constraint date_ch check (openingdate < closingdate),
constraint designation_ch check (designation in ('food', 'music', 'info'))
);

CREATE TABLE employee(
	id 				int not null generated always as identity primary key,
	name 			varchar(20) not null,
	surname 		varchar(20) not null,
	datofbirth 		date not null,
	gender 			char(1) not null,
	status 			varchar(20) not null,
	salary 			float not null,
	expdescription 	varchar(150) null,
	constraint gender_ch check (gender in ('f', 'm')),
	constraint status_ch check (status in ('working', 'vacation', 'quit'))
);

CREATE TABLE participant(
	id 				int not null generated always as identity primary key,
	name 			varchar(20) not null,
	surname 		varchar(20) not null,
	datofbirth 		date not null,
	gender 			char(1) not null,
	preferedzone 	int not null,
	constraint pref_zone_fk foreign key(preferedzone) references zone(id) on delete cascade
);

CREATE TABLE employeezones(
	emp_id 		int not null, 
	zone_id 	int not null,
	startdate 	date not null,
	enddate 	date null,
	constraint date_check check (startdate < enddate),
	constraint emp_zones_pk primary key (emp_id, zone_id),
	constraint zone_fk foreign key (zone_id) references zone(id) on delete cascade,
	constraint emp_fk foreign key (emp_id) references employee(id) on delete cascade
);
