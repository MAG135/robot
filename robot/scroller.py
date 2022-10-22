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
        recommend_videos_dict = dict()
        while True:
            content = self.robot.get_publications_from_main_page()
            for i in range(count, len(content)):
                self.robot.scroll_to_element(content[i])

                time.sleep(0.5)  # Чтобы скролл успел отработать

                publication_id = html_parser.get_publication_id(content[i])

                time_sleep = random.randint(4, 9)  # TODO: в конфиг

                if publication_id in recommend_videos_dict:
                    publication = recommend_videos_dict[publication_id]
                    # time_sleep = video.metadata.duration  # TODO: Добавить delay, т.к. видео запускаются не сразу
                else:
                    publication = html_parser.parse_publication(content[i])

                print(publication)
                flag, alg_state = self.handler.handle(publication)
                if flag:
                    if alg_state == AlgorithmState.AT_FIRST:
                        break

                time.sleep(time_sleep)

            # TODO подумать куда это вынести
            responses = self.robot.get_recommend_videos()
            self.robot.del_requests_history()

            recommend_videos_list = list()

            for r in responses:
                recommend_videos_list += response_parser.videos_from_response(r)

            for v in recommend_videos_list:
                recommend_videos_dict[v.metadata.publication_id] = v

            count = len(content)