create table people (
	id   VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255)
);

create table switches (
	id          INTEGER PRIMARY KEY,
	description VARCHAR(255)
);

create table person_to_switch (
	person VARCHAR(255),
	switch INTEGER,
	state  TINYINT,
	PRIMARY KEY (person, switch)
);
