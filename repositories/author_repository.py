from db import db
from db.db import AuthorEntity


def save(author: AuthorEntity):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author.save()


def add_authors(authors: list[str], category: int):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)

        authors_copy = authors.copy()

        new_authors = AuthorEntity.select().where(
            (AuthorEntity.author_id.in_(authors_copy)) & (AuthorEntity.category == category))

        for i in new_authors:
            if i.author_id in authors_copy:
                authors_copy.remove(i.author_id)

        for a in authors_copy:
            AuthorEntity(author_id=a, last_publication_id='', category=category).save()


def remove_authors(authors: list[str], category: int):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)

        AuthorEntity.delete().where(
            (AuthorEntity.author_id.not_in(authors)) & (AuthorEntity.category == category))


def update_last_publication_id(author_id: str, last_publication_id: str, category: int):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author = AuthorEntity.get((AuthorEntity.author_id == author_id) & (AuthorEntity.category == category))
        author.last_publication_id = last_publication_id
        author.save()


def get_last_publication_id(author_id: str, category: int):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author = AuthorEntity.get((AuthorEntity.author_id == author_id) & (AuthorEntity.category == category))
        return author.last_publication_id


def get_all_authors():
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)

        resp = AuthorEntity.select()

        authors = list()
        for a in resp:
            authors.append(a)

        return authors


def get_all_authors_without_deleted():
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)

        resp = AuthorEntity.select().where(AuthorEntity.is_deleted == False)

        authors = list()
        for a in resp:
            authors.append(a)

        return authors


def set_is_working(author: str, is_working: bool):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author = AuthorEntity.get(AuthorEntity.author_id == author)
        author.is_working = is_working
        author.save()


def set_is_deleted(author: str, is_deleted: bool):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        author = AuthorEntity.get(AuthorEntity.author_id == author)
        author.is_deleted = is_deleted
        author.save()
