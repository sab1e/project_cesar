PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS employee;
CREATE TABLE employee (id_employee INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32),surname VARCHAR (32));
INSERT INTO employee (id_employee, name, surname) VALUES (1, 'Ivan', 'Ivanov');
INSERT INTO employee (id_employee, name, surname) VALUES (2, 'Boris', 'Borisov');
INSERT INTO employee (id_employee, name, surname) VALUES (3, 'Fedor', 'Fedorov');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;