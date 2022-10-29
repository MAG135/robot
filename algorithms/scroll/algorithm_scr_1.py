"""
Алгоритм применяемый во время скроллинга

Если встречаем видео с прописанными хэштегами:
1) прыгаем в профиль автора
2) смотри 2 видео и ставим им лайки
3) идем в рекомендации
4) скачиваем 5 первых видео
"""
import time

from algorithms.common import IAlgorithmScroll, Algorithm, AlgorithmState
from enums.button_type import ButtonType
from models.publication_model import PublicationModel
from models.video_model import VideoModel
from robot.robot import TikTokRobot


class AlgorithmScroll1(IAlgorithmScroll):
    def __init__(self, robot: TikTokRobot):
        self.robot = robot
        self.publication = None

    def step_1_finish_watching_video(self):
        time.sleep(self.publication.video.duration)

    def step_2_move_to_author_account(self):
        self.robot.press_button(ButtonType.ACCOUNT_LINK)
        pass

    def step_3_watch_two_videos_and_like(self):
        self.robot.open_publication()
        # TODO: Добавить delay
        time.sleep(self.publication.video.duration)
        self.robot.press_button(ButtonType.LIKE_IN_PUBLISH)
        time.sleep(5)
        self.robot.press_button(ButtonType.NEXT_VIDEO)
        time.sleep(5)
        self.robot.press_button(ButtonType.LIKE_IN_PUBLISH)
        pass

    def step_4_move_to_recommend(self):
        self.robot.press_button(ButtonType.CLOSE_VIDEO)
        time.sleep(5)
        self.robot.press_button(ButtonType.RECOMMEND)
        pass

    def step_5_download_five_videos(self):
        pass

    def start(self, publication: PublicationModel):
        self.publication = publication

        self.step_1_finish_watching_video()
        self.step_2_move_to_author_account()
        self.step_3_watch_two_videos_and_like()
        self.step_4_move_to_recommend()
        self.step_5_download_five_videos()

        self.publication = None

        return AlgorithmState.AT_FIRST

    def get_priority(self):
        return 1

    def get_name(self):
        return Algorithm.ALGORITHM_1
