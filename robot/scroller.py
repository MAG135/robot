import random
import time
import traceback

import selenium.common.exceptions

import parsers.html_parser as html_parser
import parsers.response_parser as response_parser
from algorithms.common import AlgorithmState
from algorithms.handlers import Handler
from robot.robot import TikTokRobot

"""
Скроллер ориентированный на работу с алгоритмами
"""


class Scroller:
    def __init__(self, robot: TikTokRobot, handler: Handler):
        self.robot = robot
        self.handler = handler

    def start(self):
        count = 0
        recommend_publications_dict = dict()

        retry = 0

        while True:
            try:
                content = self.robot.get_publications_from_main_page()
                if len(content) == count:
                    print(f"len(content) == count. {len(content)} == {count}")
                    retry += 1
                    time.sleep(1)

                for i in range(count, len(content)):
                    retry = 0
                    print("Получаем следующее видео в ленте")
                    self.robot.scroll_to_element(content[i])

                    time.sleep(0.8)  # Чтобы скролл успел отработать

                    publication_id = html_parser.get_publication_id(content[i])
                    if publication_id == -1:
                        print(f"publication_id == -1. Пробуем еще через 3 секунды")
                        time.sleep(3)
                        publication_id = html_parser.get_publication_id(content[i])
                        print(publication_id)

                    if publication_id in recommend_publications_dict:
                        publication = recommend_publications_dict[publication_id]
                    else:
                        publication = html_parser.parse_publication(content[i])

                    print(f"Проверяем, что продолжительность видео не 0. Длина: {publication.video.duration}")
                    if publication.video.duration == 0:
                        print(f"Задаем продолжительность видео по-умолчанию")
                        publication.video.duration = 10

                    print(f"Запускаем обработку публикации")
                    flag, alg_state = self.handler.handle(publication)
                    if flag:
                        if alg_state == AlgorithmState.AT_FIRST:
                            break

                    time.sleep(random.randint(4, 10))

                if retry == 15:
                    print(f"retry == 15")
                    self._revive()
                    retry = 0
                    count = 0
                    continue

                # TODO подумать куда это вынести
                print(f"Получаем новые видео из ленты")
                responses = self.robot.get_recommend_videos()
                self.robot.del_requests_history()

                recommend_publications_list = list()

                for r in responses:
                    recommend_publications_list += response_parser.videos_from_response(r)

                for p in recommend_publications_list:
                    recommend_publications_dict[p.publication_id] = p

                count = len(content)
            except Exception as ex:
                print("--------------------Упал---------------------------")
                print(traceback.format_exc())
                self._revive()
                retry = 0
                continue

    def _revive(self):
        r = False

        while not r:
            try:
                self.robot.driver_get_to("")
                r = True
            except selenium.common.exceptions.TimeoutException:
                print("Получили исключение по таймауту. Спим 3 минуты")
                time.sleep(180)
