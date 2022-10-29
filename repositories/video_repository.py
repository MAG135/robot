from db import db
from db.db import VideoEntity


def save(video: VideoEntity):
    with db.tiktok_db:
        db.tiktok_db.connect(reuse_if_open=True)
        video.save()
