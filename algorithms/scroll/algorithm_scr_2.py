"""
Алгоритм применяемый во время скроллинга

1) Попадаем на видео
2) Проверяем есть ли в хэштегах слова из словаря
ИЛИ Проверяем есть ли в описании слова из словаря
ИЛИ Проверяем есть автор в нашем списке
3) Лайк
"""
import random
import time

from algorithms.common import IAlgorithmScroll, Algorithm, AlgorithmState, save
from enums.button_type import ButtonType
from models.publication_model import PublicationModel
from robot.robot import TikTokRobot
from utils.utils import get_key_words, format_words


class AlgorithmScroll2(IAlgorithmScroll):
    def __init__(self, robot: TikTokRobot):
        self.robot = robot
        self.publication = None

    def step_1_download(self):
        print(f"Скачиваем видео")
        print(self.publication)

        save(self.publication)

    def step_2_watching_video(self):
        print(f"Смотрим видео")
        time.sleep(5)  # Время на прогрузку видео
        time.sleep(self.publication.video.duration)

    def step_3_like(self):
        chance = random.randint(1, 10)

        if chance >= 5:
            self.robot.press_button(ButtonType.LIKE_IN_RECOMMEND)

    def start(self, publication: PublicationModel):
        print(f"Стартует Алгоритм_2")
        self.publication = publication

        self.step_1_download()
        self.step_2_watching_video()
        #TODO: Ломается скролл
        #self.step_3_like()

        self.publication = None

        return AlgorithmState.CONTINUE

    def get_priority(self):
        return 10

    def get_name(self):
        return Algorithm.ALGORITHM_2


def analysis_hashtags(hashtags: list[str]):
    print(f"Анализируем хэштеги: {hashtags}")
    if len(hashtags) == 0:
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


def analysis_author(author: str):
    # TODO: реализовать когда будет список авторов
    return False
