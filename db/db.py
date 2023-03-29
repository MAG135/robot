from peewee import *
from playhouse.postgres_ext import ArrayField

tiktok_db = PostgresqlDatabase(database='tiktok', user='postgres', password='password', host='localhost', port='5432')


class BaseModel(Model):
    class Meta:
        database = tiktok_db


class VideoEntity(BaseModel):
    url = TextField()
    duration = IntegerField()  # секунды

    class Meta:
        db_table = "video"


class PublicationEntity(BaseModel):
    publication_id = TextField(null=True)
    publication_url = TextField(null=True)
    author_unique_id = TextField(null=True)
    desc = TextField(null=True)
    like_count = IntegerField(null=True)
    comment_count = IntegerField(null=True)
    view_count = IntegerField(null=True)
    share_count = IntegerField(null=True)
    hashtags = ArrayField(TextField, index=False, null=True)
    category = IntegerField(null=True)
    created_at = BigIntegerField(null=True)
    video = ForeignKeyField(VideoEntity, backref="publication", unique=True, null=True)

    class Meta:
        db_table = "publication"


class AuthorEntity(BaseModel):
    author_id = TextField()
    last_publication_id = TextField()
    category = IntegerField()
    is_working = BooleanField()
    is_deleted = BooleanField()

    class Meta:
        db_table = "author"


def init():
    with tiktok_db:
        VideoEntity.create_table()
        PublicationEntity.create_table()
        AuthorEntity.create_table()
