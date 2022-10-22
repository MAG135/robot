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
    return item['desc']


def get_author_unique_id(item):
    return item['author']['uniqueId']


def get_like_count(item):
    return item['stats']['diggCount']


def get_comment_count(item):
    return item['stats']['commentCount']


def get_share_count(item):
    return item['stats']['shareCount']


def get_publication_id(item):
    return item['id']


def get_video_url(item):
    return item['video']['downloadAddr']


def get_hashtags(item):
    hashtags = list()

    if 'textExtra' in item:
        hashtags = [t['hashtagName'] for t in item['textExtra']]
    elif 'challenges' in item:
        hashtags = [t['title'] for t in item['challenges']]

    return hashtags


def get_duration(item):
    return item['video']['duration']


def get_view_count(item):
    return item['stats']['playCount']
