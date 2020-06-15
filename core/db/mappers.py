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


class MapperRegistry:
    def __init__(self, connection, Employee):
        self.connection = connection
        self.Employee = Employee

    def get_mapper(self, obj):
        if isinstance(obj, self.Employee):
            return EmployeeMapper(self.connection, self.Employee)
        else:
            raise Exception(f'Не существует отображения для объекта {type(obj)}')
