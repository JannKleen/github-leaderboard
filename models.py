# Local imports
from settings import db

# Contrib imports
from peewee import *


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    user_id = IntegerField(unique=True)
    name = CharField()
    etag = CharField()
