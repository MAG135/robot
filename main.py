import logging

from algorithms.customization.algorithm_customization import AlgorithmCustomization
from db import db
from robot.robot import TikTokRobot

#logging.basicConfig(level = logging.INFO)

if __name__ == "__main__":
    robot = TikTokRobot("https://www.tiktok.com/", "./robot/chromedriver/chromedriver.exe")
    db.init()

    try:
        robot.start()
        input("После аутентификации перейдите в ленту рекомендаций. В консоли нажмите Enter")
        print("Окно браузера сделайте активным")

        # Инициализация скроллера с алгоритмами
        # algs = list()
        # algs.append(AlgorithmScroll1(robot))
        # handler = Handler(algs)
        # scroller = Scroller(robot, handler)
        # scroller.start()

        a = AlgorithmCustomization(robot)
        try:
            a.start()
        except Exception as ex:
            print(ex.__traceback__)

    except Exception as ex:
        logging.error(ex, exc_info=True)
    finally:
        robot.stop()