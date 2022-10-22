from peewee import *
from playhouse.postgres_ext import ArrayField

db = PostgresqlDatabase(database='tiktok', user='postgres', password='password', host='localhost', port='5432')


class BaseModel(Model):
    class Meta:
        database = db


class VideoEntity(BaseModel):
    url = TextField()
    duration = IntegerField()  # секунды

    class Meta:
        db_table = "video"


class PublicationEntity(BaseModel):
    publication_id = TextField()
    publication_url = TextField()
    author_unique_id = TextField()
    desc = TextField()
    like_count = IntegerField()
    comment_count = IntegerField()
    view_count = IntegerField()
    share_count = IntegerField()
    hashtags = ArrayField(TextField, index=False)
    video = ForeignKeyField(VideoEntity, backref="publication", unique=True)

    class Meta:
        db_table = "publication"


def init():
    VideoEntity.create_table()
    PublicationEntity.create_table()
