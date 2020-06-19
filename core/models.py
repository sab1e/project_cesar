import abc

from .db.unity_of_work import DomainObject


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

    def __init__(self, id, name, surname, position=None, departament=None):
        self.id_employee = id
        self.name = name
        self.surname = surname
        self.position = position
        self.departament = departament

    def __str__(self):
        return f'{self.name} {self. surname}'


class Departament:

    def __init__(self, id, name, employees=[]):
        self.id_departament = id
        self.name = name
        self.employees = employees

    def __str__(self):
        return self.name

    def add_empoyee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)


class Position:

    def __init__(self, id, name):
        self.id_position = id
        self.name = name

    def __str__(self):
        return self.name


class Tasks(Subject):

    def __init__(self, id, name, owner, responsible=None, from_date=None,
                 to_date=None, priority=None, status=None):
        super().__init__()
        self.id_task = id
        self.name = name
        self.owner = owner
        self.responsible = responsible
        self.from_date = from_date
        self.to_date = to_date
        self._priority = priority
        self._status = status

    def __str__(self):
        return f'{self.name}'

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

    def __init__(self, id, name):
        self.id_status = id
        self.name = name

    def __str__(self):
        return self.name


class Priority:

    def __init__(self, id, name):
        self.id_priority = id
        self.name = name

    def __str__(self):
        return self.name


class Project(DomainObject):

    def __init__(self, id, name, from_date=None, to_date=None, manager=None,
                 employees=[], tasks=[]):
        self.id_project = id
        self.name = name
        self.from_date = from_date
        self.to_date = to_date
        self.manager = manager
        self.employees = employees
        self.tasks = tasks

    def __str__(self):
        return f'{self.name}'

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)


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
