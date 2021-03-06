"""Unit-тесты models.py"""

import unittest
from models import Employee, Departament, Position, Project, Tasks, Status,\
    Priority


class TestEmployee(unittest.TestCase):
    """Класс тестов для Employee()"""
    def setUp(self):
        self.departament = Departament('project')
        self.position = Position('engineer')
        self.employee = Employee('Ivan', 'Ivanov',
                                 self.position, self.departament)

    def test_init(self):
        self.assertEqual(self.employee.name, 'Ivan')
        self.assertEqual(self.employee.surname, 'Ivanov')
        self.assertEqual(self.employee.position.name, 'engineer')
        self.assertEqual(self.employee.departament.name, 'project')

    def test_str(self):
        self.assertEqual(str(self.employee), 'employee: Ivan Ivanov\n'
                                             'departament: project\n'
                                             'position: engineer')


class TestDepartament(unittest.TestCase):
    """Класс тестов для Departament()"""
    def setUp(self):
        self.departament = Departament('project')
        self.employee_ivan = Employee('Ivan',
                                      'Ivanov',
                                      'engineer',
                                      'project')
        self.employee_petr = Employee('Petr',
                                      'Petrov',
                                      'lead_engineer',
                                      'project')
        self.departament.add_empoyees(self.employee_ivan)
        self.departament.add_empoyees(self.employee_petr)

    def test_init(self):
        self.assertEqual(self.departament.name, 'project')

    def test_str(self):
        self.assertEqual(str(self.departament), 'project')

    def test_add_employee(self):
        self.assertEqual(self.departament.employees,
                         [self.employee_ivan, self.employee_petr])

    def test_remove_employee(self):
        self.departament.remove_employee(self.employee_petr)
        self.assertEqual(self.departament.employees, [self.employee_ivan])


class TestTasks(unittest.TestCase):
    """Класс тестов для Tasks()"""
    def setUp(self):
        self.priotity = Priority('quickly')
        self.status = Status('in progress')
        self.task = Tasks('calculation', '01.01.2020', '07.01.2020',
                          self.priotity, self.status)

    def test_init(self):
        self.assertEqual(self.task.name, 'calculation')
        self.assertEqual(self.task.from_date, '01.01.2020')
        self.assertEqual(self.task.to_date, '07.01.2020')
        self.assertEqual(self.task.priority.name, 'quickly')
        self.assertEqual(self.task.status.name, 'in progress')

    def test_str(self):
        self.assertEqual(str(self.task), 'calculation from: 01.01.2020 '
                                         'to: 07.01.2020\n'
                                         'priority: quickly, '
                                         'status: in progress')


class TestStatus(unittest.TestCase):
    """Класс тестов для Status()"""
    def setUp(self):
        self.position = Position('engineer')

    def test_init(self):
        self.assertEqual(self.position.name, 'engineer')

    def test_str(self):
        self.assertEqual(str(self.position), 'engineer')


class TestPriotity(unittest.TestCase):
    """Класс тестов для Priority()"""
    def setUp(self):
        self.priority = Priority('quickly')

    def test_init(self):
        self.assertEqual(self.priority.name, 'quickly')

    def test_str(self):
        self.assertEqual(str(self.priority), 'quickly')


class TestProject(unittest.TestCase):
    """Класс тестов для Project()"""
    def setUp(self):
        self.manager = Employee('Petr',
                                'Petrov',
                                'lead_engineer',
                                'project')
        self.project = Project('Umbrella', '01.01.2020', '07.01.2020',
                               self.manager)
        self.employee_ivan = Employee('Ivan',
                                      'Ivanov',
                                      'engineer',
                                      'project')
        self.employee_alex = Employee('Alex',
                                      'Alexandrov',
                                      'engineer',
                                      'bilding')
        self.project.employees.append(self.employee_ivan)
        self.project.employees.append(self.employee_alex)

    def test_init(self):
        self.assertEqual(self.project.name, 'Umbrella')
        self.assertEqual(self.project.from_date, '01.01.2020')
        self.assertEqual(self.project.to_date, '07.01.2020')
        self.assertEqual(self.project.manager.name, 'Petr')

    def test_append(self):
        self.assertEqual(self.project.employees,
                         [self.employee_ivan,self.employee_alex])

    def test_remove(self):
        self.project.employees.remove(self.employee_alex)
        self.assertEqual(self.project.employees, [self.employee_ivan])


if __name__ == '__main__':
    unittest.main()
