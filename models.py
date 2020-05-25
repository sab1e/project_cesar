import abc


class Employee:

    def __init__(self, name, surname, position, departament):
        self.name = name
        self.surname = surname
        self.position = position
        self.departament = departament


class Departament:

    def __init__(self, name):
        self.name = name


class Position:

    def __init__(self, name):
        self.name = name


class Tasks:

    def __init__(self, name, from_date=None, to_date=None):
        self.name = name
        self.from_date = from_date
        self.to_date = to_date

    def change_status(self, status):
        pass

    def change_priority(self, priority):
        pass


class Status:

    def __init__(self, name):
        self.name = name


class Priority:

    def __init__(self, name):
        self.name = name


class Project:

    def __init__(self, name):
        self.name = name
        self.from_date = None
        self.to_date = None
        self.manager = None
        self.employees = []
        self.tasks = []

    def __str__(self):
        return f'{self.name}:\n' \
               f'manager - {self.manager}\n' \
               f'project team - {self.employees}\n' \
               f'start project - {self.from_date}\n' \
               f'finish project - {self.to_date}\n' \
               f'project tasks - {self.tasks}'


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


builder = ProjectBuilder('umbrella')
builder.add_manager('Ivanov')
builder.add_employees('Semenov')
builder.add_employees('Petrov')
builder.set_from_date('01.01.2020')
builder.set_to_date('01.01.2021')
builder.add_tasks('bought equipment')

print(builder.get_project())

