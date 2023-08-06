import os
import sqlite3


class empty():
    pass
class DataType:
    def __init__(self, size=0, nullable=False, default=None, primary_key=False, check=None, unique=None):
        if primary_key and nullable:
            raise Exception("And so, are you sure you need to make a database? because what you're trying to do reminds me of self-castration. PK must not be null")
        self.size = size
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.check = check
        self.primary_key = primary_key

class String(DataType):
    name = "TEXT"

class Integer(DataType):
    name = "INTEGER"

class Float(DataType):
    name = "REAL"

class Binary(DataType):
    name = "BINARY"

class ForeignKey(DataType):
    name = "REFERENCES"
    def __init__(self, table_column, on_delete=None, on_update=None, size=0, nullable=False, default=None, primary_key=False, check=None, unique=None):
        self.column = ' ('.join(table_column.split('.'))+')'
        if on_delete != None:
            self.column += ' ON DELETE ' + on_delete
        if on_update != None:
            self.column += ' ON UPDATE ' + on_update

class Table_Engine:
    def __init__(self, **qwargs):
        for k, v in qwargs.items():
            self.__all__.__setattr__(k, v)
    
    @classmethod
    def read(cls):
        conn = sqlite3.connect(db_settings.path)
        cur = conn.cursor()
        request  = "SELECT * FROM " + cls.__name__ # fix this line
        cur.execute(request)
        conn.commit()
        values = cur.fetchall()
        returned = []
        obj = {}
        for line in values:
            column_names = iter(cur.description)
            for val in line:
                obj[next(column_names)[0]] = val
            returned.append(type(cls.__name__, (), obj))
        conn.commit()
        return returned

    @classmethod
    def save(cls):
        conn = sqlite3.connect(db_settings.path)
        cur = conn.cursor()
        try:
            request = 'INSERT INTO '+ cls.__name__ + ' ('
            values = 'VALUES ('
            for k, v in cls.__dict__.items():
                if k not in empty.__dict__.keys():
                    request+=f'{k}, '
                    if v.__class__ == str:
                        values+=f'"{v}", '
                    else:
                        values+=f'{v}, '
            request = request[:-2] + ')'
            values = values[:-2] + ')'
            cur.execute(request+values)
            conn.commit()
            return True
        except Exception as ex:
            raise Exception(f'well congratulations your father goes fucking you with a chair on the head with these words: {ex}')

    @classmethod
    def create(cls, **qwargs):
        obj = qwargs
        new_cls = type(cls.__name__, (Table_Engine,), obj)
        return new_cls

class db_settings:
    path = 'database.db'
    debug = False # добавить возможность с дебагом