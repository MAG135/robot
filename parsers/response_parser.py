import json

from models.video_model import VideoModel
from models.publication_model import PublicationModel
from utils.utils import generate_publication_url
from seleniumwire.request import Response


def videos_from_response(response: Response):
    item_list = json.loads(response.body.decode("utf-8"))['itemList']
    publications = list()

    for item in item_list:
        publications.append(get_publication_info(item))

    return publications


def get_publication_info(item: str):
    author_unique_id = get_author_unique_id(item)
    publication_id = get_publication_id(item)

    return PublicationModel(
        publication_url=generate_publication_url(author_unique_id, publication_id),
        publication_id=publication_id,
        author_unique_id=author_unique_id,
        desc=get_desc(item),
        like_count=get_like_count(item),
        comment_count=get_comment_count(item),
        view_count=get_view_count(item),
        share_count=get_share_count(item),
        hashtags=get_hashtags(item),
        video=VideoModel(get_video_url(item), get_duration(item))
    )


def get_desc(item):
    desc = ''

    try:
        desc = item['desc']
    except Exception:
        print(f"Не удалось получить описание видео")

    return desc


def get_author_unique_id(item):
    author_unique_id = ''

    try:
        author_unique_id = item['author']['uniqueId']
    except Exception:
        print(f"Не удалось получить идентификатор автора")

    return author_unique_id


def get_like_count(item):
    like_count = -1

    try:
        like_count = item['stats']['diggCount']
    except Exception:
        print(f"Не удалось получить количество лайков")

    return like_count


def get_comment_count(item):
    comment_count = -1

    try:
        comment_count = item['stats']['commentCount']
    except Exception:
        print(f"Не удалось получить количество комментариев")

    return comment_count


def get_share_count(item):
    share_count = -1
    
    try:
        share_count = item['stats']['shareCount']
    except Exception:
        print(f"Не удалось получить количество репостов")
    
    return share_count


def get_publication_id(item):
    publication_id = -1

    try:
        publication_id = item['id']
    except Exception:
        print(f"Не удалось получить идентификатор публикации")

    return publication_id


def get_video_url(item):
    video_url = -1

    try:
        video_url = item['video']['downloadAddr']
    except Exception:
        print(f"Не удалось получить url видео")

    return video_url


def get_hashtags(item):
    hashtags = list()

    try:
        if 'textExtra' in item:
            hashtags = [t['hashtagName'] for t in item['textExtra']]
        elif 'challenges' in item:
            hashtags = [t['title'] for t in item['challenges']]
    except Exception:
        print(f"Не удалось получить хэштеги")

    return hashtags


def get_duration(item):
    duration = 0

    try:
        duration = item['video']['duration']
    except Exception:
        print(f"Не удалось получить продолжительность видео")

    return duration


def get_view_count(item):
    view_count = -1

    try:
        view_count = item['stats']['playCount']
    except Exception:
        print(f"Не удалось получить количество просмотров")

    return view_count
