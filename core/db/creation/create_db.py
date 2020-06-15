import sqlite3
import os


class DbDirector:
    def __init__(self):
        self._builder = None

    def construct(self, builder):
        self._builder = builder
        self._builder.create_employees()

    def destruct(self):
        self._builder.drop_employees()


class Sqlite3Builder:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_employees(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
            path_to_script = os.path.join(path_to_script_dir,
                                          'create_employee.sql')
            with open(path_to_script) as f:
                cur.executescript(f.read())

    def drop_employees(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('DROP TABLE IF EXISTS employee')

