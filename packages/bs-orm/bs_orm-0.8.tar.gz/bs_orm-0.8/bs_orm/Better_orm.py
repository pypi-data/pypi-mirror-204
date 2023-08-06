import models
from .DataTypes import *
import sqlite3
import os
import datetime


class empty:
    pass


class db_settings:
    path = 'database.db'


def for_size(content, request):
    try:
        if content.size:
            request += f'({content.size})'
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


def for_pk(content, request):
    try:
        if content.primary_key:
            request += f'PRIMARY KEY '
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


def for_auto_increment(content, request):
    try:
        if content.auto_increment:
            request += f'AUTOINCREMENT '
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


def for_null(content, request):
    try:
        if not content.nullable:
            request += f'NOT NULL '
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


def for_unique(content, request):
    try:
        if content.unique:
            request += f'UNIQUE '
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


def for_default(content, request):
    try:
        if content.default:
            request += f'DEFAULT {content.default}'
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


def for_check(content, request):
    try:
        if content.check:
            request += f'CHECK {content.check} '
        return ['ok', request]
    except Exception as ex:
        return ['error', ex]


CHECKS = [for_size, for_pk, for_auto_increment,
          for_null, for_unique, for_default, for_check]
a = {}
last_filename = ''


def get_snapshot(table_name, table):
    global a
    for key, value in table.items():
        a[table_name][key] = value.__dict__


def get_table(table_name: str, table: dict):
    returned = f'CREATE TABLE IF NOT EXISTS "{table_name}"('
    global a
    for column, info_column in table.items():
        try:
            if info_column.__class__.__weakref__.__objclass__ == DataType:
                returned += f'"{column}" {info_column.name} '
                a[table_name] = {}
                get_snapshot(table_name, table)
                if info_column.__class__.__name__ == 'ForeignKey':
                    returned += info_column.column + ' '
                else:
                    for check in CHECKS:
                        res = check(info_column, returned)
                        if res[0] == 'ok':
                            returned = res[1]
                returned = returned+', '

        except Exception as ex:
            raise Exception(
                "Fuck you ugly motherless. Do you understand that in file models.py you need have only table name as class?")
    if 'PRIMARY KEY' not in returned:
        returned += f'"id" INTEGER PRIMARY KEY  '
    returned = returned[:-2]+')'
    return returned


def create_execute():
    request = ''
    for mod_name, value in models.__dict__.items():
        if hasattr(value, '__module__') and value.__module__ == 'models':
            table_name = mod_name
            mod = dict(value.__dict__)
            for i in empty.__dict__:
                if i in mod:
                    mod.pop(i)
            request += get_table(table_name, mod)+';\n'
    # print(request)
    return request


def create_tables():
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    cur.executescript(create_execute() +
                      'CREATE TABLE IF NOT EXISTS "migrations"(filename TEXT)')
    conn.commit()
    conn.close()


def write(table, **qwargs):
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    try:
        request = 'INSERT INTO '
        for mod_name, value in models.__dict__.items():
            if table == value:
                request += f'{mod_name}('
                req_val = 'VALUES('
                for k, v in qwargs.items():
                    request += k+', '
                    if v.__class__ == str:
                        req_val += f'\'{v}\','
                    else:
                        req_val += f'{v},'
                request = request[:-2]+') '
                req_val = req_val[:-1]+') '
                request += req_val
                cur.execute(request)
                conn.commit()
                conn.close()
                return True
    except Exception as ex:
        raise Exception(
            f'well congratulations your father goes fucking you with a chair on the head with these words: {ex}')


def migrate():
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    cur.execute('SELECT sql FROM sqlite_master WHERE type="table"')
    old_data = ';\n'.join([x[0] for x in cur.fetchall()])
    new_data = create_execute()
    for_old = [
        'CREATE TABLE "migrations"(filename TEXT)', 'CREATE TABLE ', ';']
    for_new = ['CREATE TABLE IF NOT EXISTS ', ';']
    for param in for_old:
        old_data = old_data.replace(param, '')
    for param in for_new:
        new_data = new_data.replace(param, '')
    old_data = old_data.replace('\n\n', '\n').strip('\n')
    new_data = new_data.replace('\n\n', '\n').strip('\n')

    add_list = []
    remove_list = []
    update_list_r = []
    update_list_a = []
    FD_add_list = []
    FD_remove_list = []
    FD_update_list_r = []
    FD_update_list_a = []

    def get_line(data, table_name):
        table_name = table_name.replace('"', '')
        for table in data.split('\n'):
            table = table.replace('"', '')
            if table_name in table and not table[table.find(table_name)+\
                                                 len(table_name)].isalnum():
                return table
        return ''

    for old_t in old_data.split('\n'):
        old_table = old_t.split('(')[0]
        if old_table not in new_data:
            remove_list.append(f'DROP TABLE {old_table}')
            FD_remove_list.append(f'CREATE TABLE IF NOT EXISTS {old_t}')
        else:
            if old_t.replace('"', '') not in new_data:
                old_t = old_t.split('(')
                table = get_line(new_data, old_t[0])
                for atr in [x \
                            for x in "(".join(old_t[1:]).strip(')').split(',')\
                                if (x != '' and x != ' ' and x != [])]:
                    if atr.replace('"', '').strip() not in table:
                        col_name = atr.split('"')[1]
                        update_list_r.append(
                            f'ALTER TABLE {old_t[0]} DROP COLUMN {col_name}')
                        FD_update_list_r.append(
                            f'ALTER TABLE {old_t[0]} ADD COLUMN {atr}')

    for new_t in new_data.split('\n'):
        new_table = new_t.split('"')[1]
        if new_t.split('"')[1] not in old_data:
            add_list.append(f'CREATE TABLE IF NOT EXISTS {new_t}')
            FD_add_list.append(f'DROP TABLE {new_table}')
        else:
            if new_t not in old_data:
                new_t = new_t.split('"')
                table = get_line(old_data, new_t[1])
                for atr in ('"'+'"'.join(new_t[3:])[:-1]).split(','):
                    if atr.replace('"', '').strip() not in table:
                        update_list_a.append(
                            f'ALTER TABLE "{new_t[1]}" ADD COLUMN {atr[:-1]}')
                        atr = atr.split('"')[1]
                        FD_update_list_a.append(
                            f'ALTER TABLE "{new_t[1]}" DROP COLUMN {atr}')

    def concatenete_data(string, list_string):
        for i in list_string:
            if string != '\n':
                string += ';\n'
            string += ";\n".join(i)
        return string

    upgrade = '\n'
    upgrade = concatenete_data(
        upgrade, [add_list, remove_list, update_list_a, update_list_r])
    downgrade = '\n'
    downgrade = concatenete_data(
        downgrade, [FD_add_list, FD_remove_list, \
                    FD_update_list_a, FD_update_list_r])

    textFromPattern = f'''import sqlite3
from better_orm import db_settings

def upgrade():
    upgrade_execut = """{upgrade}"""
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    cur.executescript(upgrade_execut)

def downgrade():
    downgrade_execut = """{downgrade}"""
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    cur.executescript(downgrade_execut)'''

    try:
        os.mkdir('migrations')
    except:
        pass

    fileName = str(datetime.datetime.now().timestamp())
    with open(f'./migrations/{fileName}.py', 'w') as f:
        f.write(textFromPattern)

    print(upgrade)

    cur.execute(f'INSERT INTO migrations (filename) VALUES({fileName})')
    cur.executescript(upgrade)
    conn.commit()
    conn.close()

    # debugging
