INSERT INTO people VALUES
	("alice", "Alice"),
	("bob",   "Bob"),
	("cyril", "Cyril");

INSERT INTO switches VALUES
	(1, "Living Room Lights"),
	(2, "Bob's Room"),
	(3, "Sound System");

INSERT INTO person_to_switch VALUES
	("Alice", 1, 1),
	("bob",   1, 1),
	("cyril", 1, 1),
	("alice", 3, 0),
	("bob",   2, 1);

