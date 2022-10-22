class VideoModel:
    def __init__(self, url: str, duration: int):
        self.url = url
        self.duration = duration

    def __str__(self):
        return f"<Video url:{self.url}, duration:{self.duration}"
