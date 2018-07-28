from peewee import *

db = SqliteDatabase("db.sqlite3")


class Link(Model):
    id = CharField(max_length=6, primary_key=True)
    url = CharField(max_length=300)

    class Meta:
        database = db

