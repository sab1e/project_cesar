import abc
import sqlite3
import threading


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Observer(metaclass=abc.ABCMeta):
    """Паттрен Observer следит за изменениями статуса и приоритета задачи
    При их изменении отправляет сообщение (пока принт в консоль)"""
    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, task_name, data, change_type):
        pass


class Subject(metaclass=abc.ABCMeta):
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self, task_name, data, change_type):
        for observer in self._observers:
            observer.update(task_name, data, change_type)


class Employee(DomainObject):

    def __init__(self, id_employee, name, surname, position=None, departament=None):
        self.id_employee = id_employee
        self.name = name
        self.surname = surname
        self.position = position
        self.departament = departament

    def __str__(self):
        return f'employee: {self.name} {self. surname}\n' \
               f'departament: {self.departament}\n' \
               f'position: {self.position}'


class Departament:

    def __init__(self, name):
        self.name = name
        self.employees = []

    def __str__(self):
        return self.name

    def add_empoyees(self, employees):
        self.employees.append(employees)

    def remove_employee(self, employee):
        self.employees.remove(employee)


class Position:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Tasks(Subject):

    def __init__(self, name, owner, responsible=None, from_date=None, to_date=None, priority=None,
                 status=None):
        super().__init__()
        self.name = name
        self.owner = owner
        self.responsible = responsible
        self.from_date = from_date
        self.to_date = to_date
        self._priority = priority
        self._status = status

    def __str__(self):
        return f'{self.name} from: {self.from_date} to: {self.to_date}\n' \
               f'priority: {self.priority}, status: {self._status}'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        self._notify(self.name, status, 'статус')

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        self._priority = priority
        self._notify(self.name, priority, 'приоритет')


class SendNotify(Observer):
    def update(self, task_name, data, change_type):
        print(f'{change_type} задачи {task_name} изменен на {data}')


class Status:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Priority:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Project:

    def __init__(self, name, from_date=None, to_date=None, manager=None):
        self.name = name
        self.from_date = from_date
        self.to_date = to_date
        self.manager = manager
        self.employees = []
        self.tasks = []

    def __str__(self):
        return f'{self.name}:\n' \
               f'manager - {self.manager}\n' \
               f'project team - {self.employees}\n' \
               f'start project - {self.from_date}\n' \
               f'finish project - {self.to_date}\n' \
               f'project tasks - {self.tasks}'

    def add_employees(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)

    def add_tasks(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_tasks(self):
        task_list = []
        for task in self.tasks:
            task_list.append(str(task))
        return '\n'.join(task_list)


class AbstractProjectBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_manager(self, manager):
        pass

    @abc.abstractmethod
    def add_employees(self, employee):
        pass

    @abc.abstractmethod
    def set_from_date(self, date):
        pass

    @abc.abstractmethod
    def set_to_date(self, date):
        pass

    @abc.abstractmethod
    def add_tasks(self, task):
        pass


class ProjectBuilder(AbstractProjectBuilder):
    def __init__(self, name):
        self.project = Project(name)

    def add_manager(self, manager):
        self.project.manager = manager

    def add_employees(self, employee):
        self.project.employees.append(employee)

    def set_from_date(self, date):
        self.project.from_date = date

    def set_to_date(self, date):
        self.project.to_date = date

    def add_tasks(self, task):
        self.project.tasks.append(task)

    def get_project(self):
        return self.project


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
        statment = f'UPDATE EMPLOYEE SET NAME=?, SURNAME=? WHERE ID_EMPLOYEE=?'
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


# builder = ProjectBuilder('umbrella')
# builder.add_manager('Ivanov')
# builder.add_employees('Semenov')
# builder.add_employees('Petrov')
# builder.set_from_date('01.01.2020')
# builder.set_to_date('01.01.2021')
# builder.add_tasks('designing')
# builder.add_tasks('bought equipment')
# builder.add_tasks('building')
#
# print(builder.project.get_tasks())

# priority_quickly = Priority('quickly')
# priority_important = Priority('important')
# status_in_progress = Status('in progress')
# status_correction = Status('correction')
# status_done = Status('done')
#
# task_1 = Tasks('first', 'Petrov', status=status_in_progress,
#                priority=priority_important)
#
# task_1.attach(SendNotify())
#
# task_1.status = status_correction
# task_1.priority = priority_quickly
# task_1.status = status_done
# task_1.priority = priority_important

# try:
UnitOfWork.new_current()
new_employee_1 = Employee(None, 'Petr', 'Petrov')
new_employee_1.mark_new()

new_employee_2 = Employee(None, 'Igor', 'Igorev')
new_employee_2.mark_new()

employee_mapper_2 = EmployeeMapper(connection)
exists_employee_1 = employee_mapper_2.find_by_id(1)
exists_employee_1.mark_dirty()
print(exists_employee_1.name)
exists_employee_1.name += ' Senior'
print(exists_employee_1.name)

exists_employee_2 = employee_mapper_2.find_by_id(2)
exists_employee_2.mark_removed()

print(UnitOfWork.get_current().__dict__)

UnitOfWork.get_current().commit()
# except Exception as e:
#     print(e.args)
# finally:
#     UnitOfWork.set_current(None)

print(UnitOfWork.get_current())