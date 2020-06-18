import unittest
import sqlite3
from .db.mappers import EmployeeMapper, ProjectMapper, MapperRegistry
from .db.creation.create_db import Sqlite3Builder
from .models import Employee, Project

#
# class TestEmployeeMapper(unittest.TestCase):
#     def setUp(self):
#         self.db_name = 'test_mappers.sqlite'
#         self.builder = Sqlite3Builder(self.db_name)
#
#         self.builder.create_table('create_employee.sql')
#
#         connection = sqlite3.connect(self.db_name)
#         self.mapper = EmployeeMapper(connection, Employee)
#
#     def test_find_by_id(self):
#         employee = self.mapper.find_by_id(1)
#         self.assertEqual(employee.name, 'Ivan')
#
#     def test_insert(self):
#         new_employee_id = 4
#         new_employee_name = 'Petr'
#         new_employee_surname = 'Petrov'
#         new_employee = Employee(id=new_employee_id,
#                                 name=new_employee_name,
#                                 surname=new_employee_surname)
#         self.mapper.insert(new_employee)
#         employee = self.mapper.find_by_id(4)
#         self.assertEqual(employee.name, new_employee_name)
#
#     def test_update(self):
#         employee = self.mapper.find_by_id(1)
#         new_employee_name = 'Bogdan'
#         employee.name = new_employee_name
#         self.mapper.update(employee)
#         employee = self.mapper.find_by_id(1)
#         self.assertEqual(employee.name, new_employee_name)
#
#     def test_count(self):
#         self.assertEqual(self.mapper.count(), 3)
#
#     def test_delete(self):
#         employee = self.mapper.find_by_id(1)
#         self.mapper.delete(employee)
#         self.assertEqual(self.mapper.count(), 2)
#
#     def tearDown(self):
#         self.builder.drop_table('employee')
#
#
# class TestMapperRegistry(unittest.TestCase):
#     def setUp(self):
#         self.db_name = 'test_mappers.sqlite'
#         self.builder = Sqlite3Builder(self.db_name)
#
#         self.builder.create_table('create_employee.sql')
#
#         connection = sqlite3.connect(self.db_name)
#         self.mreg = MapperRegistry(connection, Employee)
#
#     def test_get_mapper(self):
#         employee = Employee(4, 'Petr', 'Petrov')
#         employee_mapper = self.mreg.get_mapper(employee)
#         self.assertIsInstance(employee_mapper, EmployeeMapper)
#
#     def tearDown(self):
#         self.builder.drop_table('employee')


class TestProjectMapper(unittest.TestCase):
    def setUp(self):
        self.db_name = 'test_mappers.sqlite'
        self.builder = Sqlite3Builder(self.db_name)

        self.builder.create_table('create_projects.sql')

        connection = sqlite3.connect(self.db_name)
        self.mapper = ProjectMapper(connection, Project)

    def test_get_all(self):
        projects = self.mapper.get_all()


if __name__ == '__main__':
    unittest.main()
