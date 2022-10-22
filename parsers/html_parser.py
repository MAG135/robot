from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from models.publication_model import PublicationModel
from models.video_model import VideoModel
from utils.utils import convert_str_to_number, generate_publication_url


def get_desc(div: WebElement):
    desc = ""

    try:
        desc = div.find_element(By.CLASS_NAME, "tiktok-yf3ohr-DivContainer") \
            .find_element(By.CLASS_NAME, "tiktok-1itcwxg-ImgPoster").accessible_name
    except NoSuchElementException:
        print(f"Не удалось получить описание")

    return desc


def get_author_unique_id(div: WebElement):
    author_unique_id = ""

    try:
        author_unique_id = div.find_element(By.CLASS_NAME, "tiktok-debnpy-H3AuthorTitle").accessible_name
    except NoSuchElementException:
        print(f"Не удалось получить идентификатор автора")

    return author_unique_id


def get_like_count(div: WebElement):
    like_count = -1

    try:
        like_count = convert_str_to_number(div.find_elements(By.CLASS_NAME, "tiktok-1ok4pbl-ButtonActionItem")[0]
                                           .find_element(By.TAG_NAME, "strong").text)
    except NoSuchElementException:
        print(f"Не удалось получить количество лайков")

    return like_count


def get_comment_count(div: WebElement):
    comment_count = -1

    try:
        comment_count = convert_str_to_number(div.find_elements(By.CLASS_NAME, "tiktok-1ok4pbl-ButtonActionItem")[1]
                                              .find_element(By.TAG_NAME, "strong").text)
    except NoSuchElementException:
        print(f"Не удалось получить количество комментариев")

    return comment_count


def get_share_count(div: WebElement):
    share_count = -1

    try:
        share_count = convert_str_to_number(div.find_elements(By.CLASS_NAME, "tiktok-1ok4pbl-ButtonActionItem")[2]
                                            .find_element(By.TAG_NAME, "strong").text)
    except NoSuchElementException:
        print(f"Не удалось получить количество репостов")

    return share_count


def get_publication_id(div: WebElement):
    publication_id = -1

    try:
        publication_id = div.find_element(By.CLASS_NAME, "xgplayer-container").get_attribute("id").split("-")[-1]
    except NoSuchElementException:
        print(f"Не удалось получить идентификатор публикации")

    return publication_id


def get_video_url(div: WebElement):
    video_url = ""

    try:
        video_url = _parse_video_tag(div)
    except NoSuchElementException:
        print(f"Не удалось получить url видео")

    return video_url


def get_hashtags(div: WebElement):
    hashtags = list()

    try:
        hashtags = [t.text for t in div.find_elements(By.CLASS_NAME, "tiktok-f9vo34-StrongText")]
    except NoSuchElementException:
        print(f"Не удалось получить хэштеги")

    return hashtags


def parse_publication(div: WebElement):
    author_unique_id = get_author_unique_id(div)
    publication_id = get_publication_id(div)

    return PublicationModel(
        publication_url=generate_publication_url(author_unique_id, publication_id),
        publication_id=publication_id,
        author_unique_id=author_unique_id,
        desc=get_desc(div),
        like_count=get_like_count(div),
        comment_count=get_comment_count(div),
        view_count=0,  # Невозможно вытащить из html
        share_count=get_share_count(div),
        hashtags=get_hashtags(div),  # Невозможно вытащить из html
        video=VideoModel(get_video_url(div), 0)
    )


def _parse_video_tag(div: WebElement):
    video_url = ""

    try:
        video_url = div.find_element(By.CLASS_NAME, "tiktok-13egybz-DivBasicPlayerWrapper") \
            .find_elements(By.TAG_NAME, "source")[0].get_attribute("src")
    except Exception as ex:
        # Когда 2 source
        video_url = div.find_element(By.CLASS_NAME, "tiktok-13egybz-DivBasicPlayerWrapper") \
            .find_element(By.TAG_NAME, "video").get_attribute("src")

    return video_url
