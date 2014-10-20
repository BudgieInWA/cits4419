create table people (
	person VARCHAR(255) PRIMARY KEY
);

create table switches (
	switch      VARCHAR(255) PRIMARY KEY,
	description VARCHAR(255)
);

create table person_to_switch (
	person VARCHAR(255),
	switch VARCHAR(255),
	state  TINYINT
);
