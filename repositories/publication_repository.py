from db import db
from db.db import PublicationEntity


def save(publication: PublicationEntity):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        publication.save()
