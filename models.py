import abc


class Employee:

    def __init__(self, name, surname, position=None, departament=None):
        self.name = name
        self.surname = surname
        self.position = position
        self.departament = departament

    def __str__(self):
        return f'employee: {self.name} {self. surname}\n' \
               f'departament: {self.departament}\n' \
               f'position: {self.position}'

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_surname(self, surname):
        self.surname = surname

    def get_surname(self):
        return self.surname

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_departament(self, departament):
        self.departament = departament

    def get_departament(self):
        return self.departament

    # def create_project(self, name, from_date=None, to_date=None, manager=None):
    #     return Project(name, from_date, to_date, manager)


class Departament:

    def __init__(self, name):
        self.name = name
        self.employees = []

    def __str__(self):
        return self.name

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def add_empoyees(self, employees):
        self.employees.append(employees)

    def get_employees(self):
        return self.employees

    def remove_employee(self, name):
        self.employees.remove(name)


class Position:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Tasks:

    def __init__(self, name, from_date=None, to_date=None, priority=None,
                 status=None):
        self.name = name
        self.from_date = from_date
        self.to_date = to_date
        self.priority = priority
        self.status = status

    def __str__(self):
        return f'{self.name} from: {self.from_date} to: {self.to_date}\n' \
               f'priority: {self.priority}, status: {self.status}'

    def change_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def change_priority(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority


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

    def change_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_manager(self, manager):
        self.manager = manager

    def add_employees(self, employee):
        self.employees.append(employee)

    def set_from_date(self, date):
        self.from_date = date

    def set_to_date(self, date):
        self.to_date = date

    def add_tasks(self, task):
        self.tasks.append(task)


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

