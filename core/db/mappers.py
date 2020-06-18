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
    def __init__(self, connection, Employee):
        self.connection = connection
        self.cursor = connection.cursor()
        self.Employee = Employee
        self.tablename = 'employee'

    def find_by_id(self, id):
        statment = f"SELECT id_employee, name, surname " \
                   f"FROM {self.tablename} WHERE id_employee=?"

        self.cursor.execute(statment, (id, ))
        result = self.cursor.fetchall()
        if result:
            return self.Employee(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, employee):
        statment = f'INSERT INTO {self.tablename} ' \
                   f'(name, surname) VALUES (?, ?)'

        self.cursor.execute(statment, (employee.name, employee.surname))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, employee):
        statment = f'UPDATE {self.tablename} SET name=?, surname=? ' \
                   f'WHERE id_employee=?'
        self.cursor.execute(statment, (employee.name, employee.surname,
                                       employee.id_employee))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, employee):
        statment = f'DELETE FROM {self.tablename} WHERE id_employee=?'
        self.cursor.execute(statment, (employee.id_employee, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def count(self):
        statement = f"SELECT count(*) from {self.tablename}"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()[0][0]
        return result


class ProjectMapper:
    def __init__(self, connection, Project):
        self.connection = connection
        self.cursor = connection.cursor()
        self.Project = Project
        self.tablename = 'project'

    def get_all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)

    def find_by_id(self, id):
        statment = f'SELECT id_project, name, from_date, to_date, ' \
                   f'manager, employees, tasks FROM {self.tablename} ' \
                   f'WHERE id_employee=?'

        self.cursor.execute(statment, (id, ))
        result = self.cursor.fetchall()
        if result:
            return self.Project(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, project):
        statment = f'INSERT INTO {self.tablename} ' \
                   f'(name, from_date, to_date, manager, employees, tasks) ' \
                   f'VALUES (?, ?, ?, ?, ?, ?)'

        self.cursor.execute(statment, (project.name, project.from_date,
                                       project.to_date, project.manager,
                                       project.employees, project.tasks))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, project):
        statment = f'UPDATE {self.tablename} SET name=?, from_date=?,' \
                   f'to_date=?, manager=?, employees=?, tasks=? ' \
                   f'WHERE id_employee=?'
        self.cursor.execute(statment, (project.name, project.from_date,
                                       project.to_date, project.manager,
                                       project.employees, project.tasks,
                                       project.id_project))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, project):
        statment = f'DELETE FROM {self.tablename} WHERE id_project=?'
        self.cursor.execute(statment, (project.id_project, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def count(self):
        statement = f"SELECT count(*) from {self.tablename}"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()[0][0]
        return result


class MapperRegistry:

    types = {
        'Employee': EmployeeMapper,
        'Project': ProjectMapper,
    }

    def __init__(self, connection, item_type):
        self.connection = connection
        self.item_type = item_type

    def get_mapper(self, obj):
        if isinstance(obj, self.item_type):
            TypeMapper = MapperRegistry.types[self.item_type.__name__]
            return TypeMapper(self.connection, self.item_type)
        else:
            raise Exception(f'Не существует отображения для объекта {type(obj)}')
