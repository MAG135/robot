from db.db import VideoEntity, PublicationEntity
from models.publication_model import PublicationModel
from models.video_model import VideoModel


def to_video_entity(video: VideoModel) -> VideoEntity:
    return VideoEntity(url=video.url, duration=video.duration)


def to_publication_entity(publication: PublicationModel, video_entity: VideoEntity) -> PublicationEntity:
    return PublicationEntity(publication_id=publication.publication_id,
                             publication_url=publication.publication_url,
                             author_unique_id=publication.author_unique_id,
                             desc=publication.desc,
                             like_count=publication.like_count,
                             comment_count=publication.comment_count,
                             view_count=publication.view_count,
                             share_count=publication.share_count,
                             category=publication.category,
                             created_at=publication.created_at,
                             hashtags=publication.hashtags,
                             video=video_entity)
