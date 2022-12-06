from db import db
from db.db import AuthorEntity


def save(author: AuthorEntity):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author.save()


def add_authors(authors: list[str]):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)

        authors_copy = authors.copy()

        new_authors = AuthorEntity.select().where(AuthorEntity.author_id.in_(authors_copy))

        for i in new_authors:
            if i.author_id in authors_copy:
                authors_copy.remove(i.author_id)

        for a in authors_copy:
            AuthorEntity(author_id=a, last_publication_id='').save()


def update_last_publication_id(author_id: str, last_publication_id: str):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author = AuthorEntity.get(AuthorEntity.author_id == author_id)
        author.last_publication_id = last_publication_id
        author.save()


def get_last_publication_id(author_id: str):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author = AuthorEntity.get(AuthorEntity.author_id == author_id)
        return author.last_publication_id