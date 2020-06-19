BEGIN TRANSACTION;
DROP TABLE IF EXISTS employee;
CREATE TABLE position (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));
CREATE TABLE status (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));
CREATE TABLE priority (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));
CREATE TABLE task (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), owner VARCHAR (32), responsible VARCHAR (32), from_date VARCHAR (32), to_date VARCHAR (32), priority VARCHAR (32), status VARCHAR (32));
CREATE TABLE departament (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), employees VARCHAR (32));
CREATE TABLE employee (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32),surname VARCHAR (32));
CREATE TABLE project (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32), from_date VARCHAR (32), to_date VARCHAR (32), manager VARCHAR (32), employees VARCHAR (32), tasks VARCHAR (32));

COMMIT TRANSACTION;