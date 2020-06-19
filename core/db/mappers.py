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


class BaseMapper:
    def __init__(self, connection, cls):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cls = cls
        self.tablename = None

    def find_by_id(self, id):
        statment = f"SELECT * FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statment, (id,))
        result = self.cursor.fetchall()
        if result:
            return self.cls(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def get_all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)

        items = []
        for item in self.cursor.fetchall():
            item = self.cls(*item)
            items.append(item)
        return items

    def delete(self, cls):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (cls.id, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def count(self):
        statement = f"SELECT count(*) from {self.tablename}"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()[0][0]
        return result


class EmployeeMapper(BaseMapper):
    def __init__(self, conection, cls):
        super().__init__(conection, cls)
        self.tablename = 'employee'

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
                   f'WHERE id=?'
        self.cursor.execute(statment, (employee.name, employee.surname,
                                       employee.id_employee))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, employee):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (employee.id_employee, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class ProjectMapper(BaseMapper):
    def __init__(self, connection, cls):
        super().__init__(connection, cls)
        self.tablename = 'project'

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
                   f'WHERE id=?'
        self.cursor.execute(statment, (project.name, project.from_date,
                                       project.to_date, project.manager,
                                       project.employees, project.tasks,
                                       project.id_project))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, project):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (project.id_project, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class DepartamentMapper(BaseMapper):

    def __init__(self, connection, cls):
        super().__init__(connection, cls)
        self.tablename = 'departament'

    def insert(self, departament):
        statment = f'INSERT INTO {self.tablename}' \
                   f'(name, employees) VALUES (?, ?)'

        self.cursor.execute(statment, (departament.name,
                                       departament.employees))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, departament):
        statment = f'UPDATE {self.tablename} SET name=?, employees=? ' \
                   f'WHERE id=?'
        self.cursor.execute(statment, (departament.name, departament.surname,
                                       departament.id_departament))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, departament):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (departament.id_departament,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class PositionMapper(BaseMapper):

    def __init__(self, connection, cls):
        super().__init__(connection, cls)
        self.tablename = 'position'

    def insert(self, position):
        statment = f'INSERT INTO {self.tablename}' \
                   f'(name) VALUES (?)'

        self.cursor.execute(statment, (position.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, position):
        statment = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statment, (position.name, position.id_position))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, position):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (position.id_position,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class TasksMapper(BaseMapper):
    def __init__(self, connection, cls):
        super().__init__(connection, cls)
        self.tablename = 'tasks'

    def insert(self, task):
        statment = f'INSERT INTO {self.tablename} ' \
                   f'(name, owner, responsible, from_date, to_date, priority, ' \
                   f'status) VALUES (?, ?, ?, ?, ?, ?, ?)'

        self.cursor.execute(statment, (task.name, task.owner, task.responsible,
                                       task.from_date, task.to_date,
                                       task.priority, task.status))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, task):
        statment = f'UPDATE {self.tablename} SET name=?, owner=?, ' \
                   f'responsible=?, from_date=?, to_date=?, ' \
                   f'priority=?, status=? WHERE id=?'
        self.cursor.execute(statment, (task.name, task.from_date,
                                       task.to_date, task.manager,
                                       task.employees, task.tasks,
                                       task.id_project))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, task):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (task.id_task, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class StatustMapper(BaseMapper):

    def __init__(self, connection, cls):
        super().__init__(connection, cls)
        self.tablename = 'status'

    def insert(self, status):
        statment = f'INSERT INTO {self.tablename}' \
                   f'(name) VALUES (?)'

        self.cursor.execute(statment, (status.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, status):
        statment = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statment, (status.name, status.id_status))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, status):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (status.id_status,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class PriorityMapper(BaseMapper):

    def __init__(self, connection, cls):
        super().__init__(connection, cls)
        self.tablename = 'priority'

    def insert(self, priority):
        statment = f'INSERT INTO {self.tablename}' \
                   f'(name) VALUES (?)'

        self.cursor.execute(statment, (priority.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, priority):
        statment = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statment, (priority.name, priority.id_priority))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, priority):
        statment = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statment, (priority.id_priority,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:

    types = {
        'Employee': EmployeeMapper,
        'Project': ProjectMapper,
        'Departament': DepartamentMapper,
        'Position': PositionMapper,
        'Tasks': TasksMapper,
        'Status': StatustMapper,
        'Priority': PriorityMapper,
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
