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

    def create_table(self, script_name):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            path_to_script_dir = os.path.dirname(os.path.abspath(__file__))
            path_to_script = os.path.join(path_to_script_dir, script_name)
            with open(path_to_script) as f:
                cur.executescript(f.read())

    def drop_table(self, table_name):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(f'DROP TABLE IF EXISTS {table_name}')

