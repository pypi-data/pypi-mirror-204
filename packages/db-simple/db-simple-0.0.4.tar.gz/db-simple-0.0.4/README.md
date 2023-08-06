Модуль db_simple предоставляет простой способ работы с файлами JSON.

Для работы с модулем нужно создать объект класса Database, указав имя файла без расширения .json

```
from db_simple import File
database = File("путь").load()
database.data["имя переменной"] = значение
database.save()