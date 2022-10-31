import logging
import platform

from algorithms.customization.algorithm_customization import AlgorithmCustomization
from algorithms.handlers import Handler
from algorithms.scroll.algorithm_scr_1 import AlgorithmScroll1
from algorithms.scroll.algorithm_scr_2 import AlgorithmScroll2
from db import db
from robot.robot import TikTokRobot

# logging.basicConfig(level = logging.INFO)
from robot.scroller import Scroller

if __name__ == "__main__":
    chromedriver = ""

    if platform.system() == "Linux":
        chromedriver = "chromedriver"
    elif platform.system() == "Windows":
        chromedriver = "chromedriver.exe"
    else:
        raise Exception("Не удалось подобрать драйвер")

    robot = TikTokRobot("https://www.tiktok.com/", f"./robot/chromedriver/{chromedriver}")

    db.init()

    try:
        robot.start()
        input("После аутентификации перейдите в ленту рекомендаций. В консоли нажмите Enter")
        print("Окно браузера сделайте активным")

        # Инициализация скроллера с алгоритмами
        algs = list()
        algs.append(AlgorithmScroll2(robot))
        handler = Handler(algs)
        scroller = Scroller(robot, handler)
        scroller.start()

        # a = AlgorithmCustomization(robot)
        # try:
        #     a.start()
        # except Exception as ex:
        #     print(ex.__traceback__)

    except Exception as ex:
        logging.error(ex, exc_info=True)
    finally:
        robot.stop()
