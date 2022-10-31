import random
import time

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
        while True:
            content = self.robot.get_publications_from_main_page()
            for i in range(count, len(content)):
                self.robot.scroll_to_element(content[i])

                time.sleep(0.5)  # Чтобы скролл успел отработать

                publication_id = html_parser.get_publication_id(content[i])

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

                time.sleep(random.randint(1, 2))

            # TODO подумать куда это вынести
            print(f"Получаем новые новые из ленты")
            responses = self.robot.get_recommend_videos()
            self.robot.del_requests_history()

            recommend_publications_list = list()

            for r in responses:
                recommend_publications_list += response_parser.videos_from_response(r)

            for p in recommend_publications_list:
                recommend_publications_dict[p.publication_id] = p

            count = len(content)
