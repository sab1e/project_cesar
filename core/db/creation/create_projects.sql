PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS project;
CREATE TABLE project (id_project INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), from_date VARCHAR (32), to_date VARCHAR (32), manager VARCHAR (32), employees VARCHAR (32), tasks VARCHAR (32));
INSERT INTO project (id, name, from_date, to_date, manager, employees, tasks) VALUES (1, 'Dreamscan', '01.01.2005', '01.12.2005', 'Ivanov', 'Petrov', 'make a plan');
INSERT INTO project (id, name, from_date, to_date, manager, employees, tasks) VALUES (2, 'Stargate', '03.06.2010', '01.06.2012', 'Borisov', 'Sidorov', 'bought equipment');
INSERT INTO project (id, name, from_date, to_date, manager, employees, tasks) VALUES (3, 'Mindwreaker', '15.08.2012', '01.03.2020', 'Fedorov', 'Semenov', 'build a team');
INSERT INTO project (id, name) VALUES (4, 'CHANI');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
