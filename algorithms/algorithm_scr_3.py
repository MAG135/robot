"""
Алгоритм применяемый во время скроллинга

1) Переходим на страницу автора
2) Скроллим до последнего просмотренного видео, сохраняем ссылки на новые
3) Переходим на публикацию
4) Анализируем хэштеги
5) Сохраняем
"""
import time
import traceback

from selenium.webdriver.remote.webelement import WebElement

import utils.utils
from db.db import PublicationEntity
from enums.publication_category import PublicationCategory
from repositories import author_repository, publication_repository
from robot.robot import TikTokRobot
from utils.utils import get_key_words, format_words, format_author, get_authors


class AlgorithmScroll3:
    def __init__(self, robot: TikTokRobot):
        self.robot = robot
        self.publication = None

    def step_1_go_to_author(self, author):
        print(f"Открываем профиль {author}")
        self.robot.driver_get_to("@" + author)

    def step_2_get_new_videos(self, last_publication):
        print(f"Получаем новые видео")
        new_publications = list()
        count = 0

        while True:
            # TODO: Добавить обработку случая, когда будет ошибка
            publications = self.robot.get_publications_from_page()

            if count == len(publications):
                return new_publications

            for i in range(count, len(publications)):  # Ожидается, что мы будем забирать первые 30 видео при загрузке страницы
                url = self.robot.get_publication_url_from_element(publications[i])
                if check_last_publication(url, last_publication):
                    return new_publications

                new_publications.append(publications[i])

            count = len(publications)

            self.robot.scroll_to_element(new_publications[-1])
            time.sleep(3)

            if self.robot.check_captcha():
                return new_publications

    # TODO:  Подумать нужен ли вообще анализ хэштегов, все аккаунты целевые, но не у всех видео есть хэштеги
    def step_3_analysis_hashtags(self, publications: list[WebElement]):
        best_publication = list()

        for p in publications:
            # if analysis_hashtags(self.robot.get_publication_hashtags_author_page(p)):
            #     best_publication.append(p)
            best_publication.append(p)

        return best_publication

    def step_4_download(self, author: str, category: str, publications: list[WebElement]):
        print(f"Сохраняем публикации в БД")
        for p in publications:
            publication_repository.save(PublicationEntity(
                publication_id=self.robot.get_publication_id_from_element(p),
                publication_url=self.robot.get_publication_url_from_element(p),
                author_unique_id=author,
                # decs=html_parser.get_desc(p), #TODO: это будет работать????
                # view_count= TODO: дописать парсер
                category=category,
                created_at=int(time.time()),
                hashtags=self.robot.get_publication_hashtags_author_page(p))
            )

    def start(self):

        while True:
            try:
                start_time = time.time()

                for category in list(PublicationCategory):

                    print(f"Смотрим категорию: {category.name}")

                    authors = format_author(get_authors(category.name.lower()))

                    author_repository.add_authors(authors, category.value)

                    for author in authors:
                        self.step_1_go_to_author(author)

                        last_publication = author_repository.get_last_publication_id(author, category.value)
                        print(f"Последняя публикация {author} : {last_publication}")
                        new_publications = self.step_2_get_new_videos(last_publication)

                        print(f"Найдено публикаций {len(new_publications)}")

                        if len(new_publications) != 0:
                            print(
                                f"Последния публикация {self.robot.get_publication_url_from_element(new_publications[0])}")
                            print(f"Извлекаем id публикации")
                            author_repository.update_last_publication_id(
                                author, self.robot.get_publication_id_from_element(new_publications[0]), category.value)

                        self.step_4_download(author, category.value, self.step_3_analysis_hashtags(new_publications))

                end_time = time.time()

                sleep = 2 * 60 * 60

                print(f"Закончили цикл просмотра аккаунтов. Потрачено минут: {(end_time - start_time) / 60}. Спим 2 часа")
                time.sleep(sleep)

            except Exception as ex:
                print(f"Алгоритм 3. Упали в основном цикле")
                print(traceback.format_exc())


def analysis_hashtags(hashtags: list[str]):
    print(f"Анализируем хэштеги: {hashtags}")
    try:

        if len(hashtags) == 0 or hashtags is None:
            return False
    except Exception as ex:
        return False

    words = format_words(get_key_words())

    for w in words:
        if w in hashtags:
            print(f"Нашли совпадение: {w}")
            return True

    print(f"Не нашли совпадений")
    return False


def analysis_decs(desc: str):
    print(f"Анализируем описание: {desc}")
    words = format_words(get_key_words())

    for w in words:
        if w in desc:
            print(f"Нашли совпадение: {w}")
            return True

    print(f"Не нашли совпадений")
    return False


def check_last_publication(url: str, last_publication: str):
    if utils.utils.get_publication_id_from_url(url) == last_publication:
        return True

    return False
