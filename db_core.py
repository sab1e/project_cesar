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


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Employee):
            return EmployeeMapper(connection)


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


#
# class Category(DomainObject):
#     def __init__(self, name):
#         self.name = name
#
#
# class CategoryMapper:
#     pass


# employee_mapper = EmployeeMapper(connection)
# employee_1 = employee_mapper.find_by_id(2)
# print(employee_1.__dict__)


