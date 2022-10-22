"""
Алгоритм настройки ленты

1) Ищем видео по хэштегу:
1) прыгаем в профиль автора
2) смотри 2 видео и ставим им лайки
3) идем в рекомендации
4) скачиваем 5 первых видео
"""
import logging
import random
import time

from enums.button_type import ButtonType
from mapper import mapper
from models.publication_model import PublicationModel
from parsers import html_parser
from robot.robot import TikTokRobot
from utils import utils


def _save(publication: PublicationModel):
    video_entity = mapper.to_video_entity(publication.video)
    publication_entity = mapper.to_publication_entity(publication, video_entity)

    video_entity.save()
    publication_entity.save()


class AlgorithmCustomization:
    def __init__(self, robot: TikTokRobot):
        self.robot = robot

    def step_1_search_by_hashtag(self, hashtag: str):
        self.robot.search_by_hashtags(hashtag)

    def step_2_watch_two_videos_and_like(self, count: int):
        print(f"Открываем первое видео")
        self.robot.open_first_publication(count)
        duration = self.robot.get_video_duration()
        print(f"Смотрим первое видео {duration} секунд")
        time.sleep(duration)
        print(f"Лайкаем первое видео")
        self.robot.press_button(ButtonType.LIKE_IN_PUBLISH)
        time.sleep(2)
        print(f"Включаем второе видео")
        self.robot.press_button(ButtonType.NEXT_VIDEO)
        duration = self.robot.get_video_duration()
        print(f"Смотрим второе видео {duration} секунд")
        time.sleep(duration)
        self.robot.press_button(ButtonType.LIKE_IN_PUBLISH)
        time.sleep(1)

    def step_3_move_to_recommend(self):
        self.robot.driver_get_to("")

    def step_4_download_five_videos(self):
        count = 5  # Количество видео, которое нужно выгрузить
        publications = list()

        content = self.robot.get_publications_from_main_page()
        # TODO: в случае, если на странице будет меньше нужного количества элементов, это работать не будет. ПОДУМАТЬ!
        for i in range(count):
            print(f"Скроллим на видео {i + 1}")
            self.robot.scroll_to_element(content[i])
            print(f"Скроллим видео {i + 1}")
            time.sleep(random.randint(5, 12))

            print(f"Получаем инфорацию по видео {i + 1}")
            publication = html_parser.parse_publication(content[i])
            print(f"{publication}")
            print(f"Проверяем ссылку видео")
            self.check_blob(publication)

            print(f"Сохраняем информацию о публикации {publication.publication_id} в базу")
            _save(publication)

    def start(self):
        count = 0

        while True:
            hashtags = utils.format_hashtags(utils.get_hashtags_from_file())

            i = 0
            while i != len(hashtags):
                try:
                    try:
                        tags_group = [hashtags[i], hashtags[i + 1]]
                        i += 2
                    except IndexError:
                        tags_group = [hashtags[i]]
                        i += 1

                    for tag in tags_group:
                        print(f"Ищем видео по хэштегу {tag}")
                        self.step_1_search_by_hashtag(tag)
                        print(f"Начинаем смотреть видео по хэштегу {tag}")
                        self.step_2_watch_two_videos_and_like(count)
                    print(f"Идем в ленту рекомендаций")
                    self.step_3_move_to_recommend()
                    print(f"Начинаем смотреть 5 видео")
                    self.step_4_download_five_videos()
                except Exception as ex:
                    logging.error(ex, exc_info=True)
                    continue
            count += 1

    def check_blob(self, publication: PublicationModel):
        if publication.video.url.startswith('blob'):
            logging.info(
                f"Нашли видео с кривой ссылкой {publication.video.url} для публикации {publication.publication_id}")
            print(f"Пробуем исправить ссылку")
            url = self.robot.get_url_by_key(publication.publication_id)
            if url != "":
                print(f"Ссылку исправили")
                publication.video.url = url
                return
            print(f"Не удалось исправить ссылку для публикации {publication.publication_id}")
