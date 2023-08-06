# better-orm Python 

История такова:

> Писал я значит проект и меня так сильно затрахала привязанность 
либо к одному фреймворку либо отсутствие миграций как например в 
SQLAlhimy (либо я просто не разобрался как они работают) что решил 
ебануть свою orm минут за 30 я понял что это относительно не сложно 
и начал хуярить

## How to use?

Consider how to use

---

### Create DB

you need create file
> models.py

in this file you need keep only your model and variables your model

example of a filling file

```Python
from better_orm import DataTypes

class a(DataTypes.Table_Engine):
    var1 = DataTypes.String(default='default', size=10)
    var2 = DataTypes.Integer(primary_key=True, auto_increment=True) 

class abob(DataTypes.Table_Engine):
    name = DataTypes.String(primary_key=True)
```

then you need run function `create_db()`

---

if you need custom name db you need `import DataType` and in replace `db_settings.path`

you can add in your code this line

```python
from better_orm import DataTypes

DataTypes.db_settings.path = 'database.db'
```
---

`create_db_from_models.py` creates your database. With this data you get next data base:

| a | aboba |
|-----:|-----------|
|var1|name|
|var2| |

---

## Write data

For write data with this library you need using function `write_row(table_name, **data)`

Example:
```python
write_row(models.a, var1='value1')
```

with this function your database get next value
Table a:

| var1 | var2 |
|-----:|-----------|
|"value1"|1|

or using models

```Python
mod = a.add(var1="oaoaoaoa")
mod.save()
```

if you use this code you get the same result as with funcrions write_db

---

after write data you need and read it. for read using your class with model

Exemple:
```python
from models import *

response = a.read()
```
in result you get list object 'a' with variables var1 and var2

<picture>
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://im.wampi.ru/2023/03/10/image1cf39d530b24f1ae.png">
</picture>

further more.
stages of development:
1. adding complex values such as datetime
2. Validations for programmer errors when creating a database
3. Adding migration capability
4. Injection protection