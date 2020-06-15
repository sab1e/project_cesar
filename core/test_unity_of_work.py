import unittest
import sqlite3
from .db.unity_of_work import UnitOfWork
from .db.mappers import MapperRegistry, EmployeeMapper
from .db.creation.create_db import Sqlite3Builder
from .models import Employee


class TestUnityOfWork(unittest.TestCase):
    def setUp(self):
        self.db_name = 'test_mapper_db.sqlite'
        self.builder = Sqlite3Builder(self.db_name)
        self.builder.create_employees()
        self.conn = sqlite3.connect(self.db_name)

    def test_work(self):
        UnitOfWork.new_current()
        self.uw = UnitOfWork.get_current()
        self.uw.set_mapper_registry(MapperRegistry(self.conn, Employee))

        self.employee = Employee(4, 'Petr', 'Petrov')
        self.employee.mark_new()

        UnitOfWork.get_current().commit()

        mapper = EmployeeMapper(self.conn, Employee)
        self.assertEqual(mapper.count(), 4)
        new_employee = mapper.find_by_id(4)
        self.assertEqual(new_employee.name, 'Petr')

        new_employee.name = 'Serg'
        new_employee.mark_dirty()
        UnitOfWork.get_current().commit()
        self.assertEqual(mapper.count(), 4)

        changed_employee = mapper.find_by_id(4)
        self.assertEqual(changed_employee.name, 'Serg')

        changed_employee.mark_removed()
        UnitOfWork.get_current().commit()
        self.assertEqual(mapper.count(), 3)

    def tearDown(self):
        self.builder.drop_employees()


if __name__ == '__main__':
    unittest.main()
