from models.video_model import VideoModel


class PublicationModel:
    def __init__(self, publication_url: str, publication_id: str, author_unique_id: str,
                 desc: str, like_count: int, comment_count: int,
                 view_count: int, share_count: int, hashtags: list[str], video: VideoModel):
        self.publication_url = publication_url
        self.publication_id = publication_id
        self.author_unique_id = author_unique_id
        self.desc = desc
        self.like_count = like_count
        self.comment_count = comment_count
        self.view_count = view_count
        self.share_count = share_count
        self.hashtags = hashtags
        self.video = video

    def __str__(self):
        return f"<Publication publication_url:{self.publication_url}, publication_id:{self.publication_id}, " \
               f"author_unique_id:{self.author_unique_id}, desc:{self.desc}, like_count:{self.like_count}, " \
               f"comment_count:{self.comment_count}, view_count:{self.view_count}," \
               f"share_count:{self.share_count}, hashtags:{self.hashtags}, video:{self.video}"
