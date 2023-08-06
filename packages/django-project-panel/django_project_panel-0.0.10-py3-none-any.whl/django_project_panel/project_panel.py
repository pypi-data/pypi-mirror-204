from django.conf import settings
from django.apps import apps
from django.db import connections

import psutil, os, copy


class ProjectPanel:
    KB, MB, GB, TB = 'kb', 'mb', 'gb', 'tb'
    UNIT_SIZE = {KB: 1, MB: 2, GB: 3, TB: 4}
    bsize = 1024

    def __init__(self):
        self.DATABASES = copy.copy(settings.DATABASES)
        self.MEDIA_ROOT = copy.copy(settings.MEDIA_ROOT)
        self.PROJECT_PANEL = copy.copy(settings.PROJECT_PANEL)

    @classmethod
    def bytesto(cls, bytes, to):
        return bytes / (cls.bsize ** cls.UNIT_SIZE[to])

    @classmethod
    def bytes_display(cls, bytes):
        for i in reversed(list(cls.UNIT_SIZE.keys())):
            size = cls.bytesto(bytes, i)
            if size > 1:
                return (round(size, 2), i)
        return (round(cls.bytesto(bytes, to=cls.KB), 2), cls.KB)

    @classmethod
    def folders_files_size(cls, dir):
        size = 0
        files = 0
        for f in os.listdir(dir):
            path = os.path.join(dir, f)
            if os.path.isfile(path):
                size += os.path.getsize(path)
                files += 1
            else:
                res = cls.folders_files_size(path)
                size += res[0]
                files += res[1]
        return (size, files)

    def virtual_memory(self):
        ram = psutil.virtual_memory()
        return {
            'total': self.bytes_display(ram.total),
            'available': self.bytes_display(ram.available),
            'percent': ram.percent,
        }

    def hard_disk(self):
        hard = psutil.disk_usage('/')
        return {
            'total': self.bytes_display(hard.total),
            'free': self.bytes_display(hard.free),
            'percent': hard.percent,
        }

    def get_db_report(self, alias, table=None):
        return [{'name': i[0], 'size': self.bytes_display(i[1]), 'rows': i[2]} for i in DataBase(alias).report(table)]

    def databases(self):
        clean = self.PROJECT_PANEL.get('clean_model', {})
        result = []
        for alias, data in self.DATABASES.items():
            db = {'name': data['NAME'], 'alias': alias, 'tables': self.get_db_report(alias)}
            for table in db['tables']:
                table['clean'] = clean.get(f'{alias}.{table["name"]}')
            result.append(db)
        return result

    def folders_files(self):
        folders_files = copy.copy(self.PROJECT_PANEL.get('folders_files', []))
        folders_files.insert(0, {'path': self.MEDIA_ROOT, 'label': 'Медиа файлы'})
        for i in folders_files:
            size, count = self.folders_files_size(i['path'])
            folders_files[folders_files.index(i)] = {**i, 'size': self.bytes_display(size), 'count': count}
        return folders_files

    def clean_table(self, alias, *args, **kwargs):
        return DataBase(alias).clean_table(*args, **kwargs)

    def models(self, ):
        return [{'model': m, 'table': m._meta.db_table, 'rows': m.objects.all().count()} for c in apps.get_app_configs() for m in c.get_models()]


class DataBase:
    def __init__(self, alias):
        self.alias = alias
        self.db = copy.copy(settings.DATABASES)[self.alias]
        self.connection = connections[self.alias]

    def report(self, table=None):
        name = self.db['NAME']
        table = f" AND table_name = '{table}'" if table else ''

        sql_set = {
            'django.db.backends.mysql': "SELECT table_name AS `Table`, round((data_length + index_length), 2) AS `Size`, table_rows AS `Rows`"
                                        "FROM information_schema.TABLES "
                                        f"WHERE table_schema = '{name}'{table} "
                                        "ORDER BY round((data_length + index_length), 2) DESC;",
            'django.db.backends.postgresql': "select TABLE_NAME AS Table, pg_relation_size(quote_ident(TABLE_NAME)) AS SIZE, '-' AS Rows "
                                             "from information_schema.tables "
                                             f"where table_schema = 'public'{table} "
                                             "order BY 2 desc;"}
        sql = sql_set.get(self.db['ENGINE'])
        if not sql:
            raise Exception(f'Движок базы не поддерживается {self.db["ENGINE"]}')
        with self.connection.cursor() as c:
            c.execute(sql)
            return c.fetchall()

    def clean_table(self, table, field, value, bild_sql=False):
        sql_set = {
            'django.db.backends.mysql': f"DELETE FROM `{table}` WHERE `{field}` < '{value}'",
            'django.db.backends.postgresql': f"DELETE FROM `{table}` WHERE `{field}` < '{value}'"
        }
        sql = sql_set.get(self.db['ENGINE'])
        if not sql:
            raise Exception(f'Движок базы не поддерживается {self.db["ENGINE"]}')
        if bild_sql:
            return sql
        with self.connection.cursor() as c:
            c.execute(sql)


