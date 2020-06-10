import threading
import sqlite3

from models import Employee

connection = sqlite3.connect('projects_data.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class EmployeeMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_employee):
        statment = f"SELECT ID_EMPLOYEE, NAME, SURNAME " \
                   f"FROM EMPLOYEE WHERE ID_EMPLOYEE=?"

        self.cursor.execute(statment, (id_employee, ))
        result = self.cursor.fetchall()
        if result:
            return Employee(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id_employee} '
                                          f'not found')

    def insert(self, employee):
        statment = f'INSERT INTO EMPLOYEE (NAME, SURNAME) VALUES (?, ?)'

        self.cursor.execute(statment, (employee.name, employee.surname))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, employee):
        statment = f'UPDATE PERSON SET NAME=?, SURNAME=? WHERE ID_EMPLOYEE=?'
        self.cursor.execute(statment, (employee.name, employee.surname,
                                       employee.id_employee))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, employee):
        statment = f'DELETE FROM EMPLOYEE WHERE ID_EMPLOYEE=?'
        self.cursor.execute(statment)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


employee_mapper = EmployeeMapper(connection)
employee_1 = employee_mapper.find_by_id(2)
print(employee_1.__dict__)
