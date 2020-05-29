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

    # def create_project(self, name, from_date=None, to_date=None, manager=None):
    #     return Project(name, from_date, to_date, manager)


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


builder = ProjectBuilder('umbrella')
builder.add_manager('Ivanov')
builder.add_employees('Semenov')
builder.add_employees('Petrov')
builder.set_from_date('01.01.2020')
builder.set_to_date('01.01.2021')
builder.add_tasks('designing')
builder.add_tasks('bought equipment')
builder.add_tasks('building')

print(builder.project.get_tasks())

