import logging
import platform
import time

from algorithms.algorithm_scr_3 import AlgorithmScroll3
from db import db
from robot.robot import TikTokRobot

# logging.basicConfig(level = logging.INFO)

if __name__ == "__main__":
    chromedriver = ""

    if platform.system() == "Linux":
        chromedriver = "chromedriver"
    elif platform.system() == "Windows":
        chromedriver = "chromedriver.exe"
    else:
        raise Exception("Не удалось подобрать драйвер")

    db.init()

    while True:
        robot = TikTokRobot("https://www.tiktok.com/", f"./robot/chromedriver/{chromedriver}")

        try:
            AlgorithmScroll3(robot).start()
        except Exception as ex:
            logging.error(ex, exc_info=True)
        finally:
            robot.stop()
            print("Закрыли браузер. Спим 5 минут!")
            time.sleep(5)


# ЗАПУСК АЛГОРИТМА ПО СКРОЛЛИНГУ ЛЕНТЫ С ХЭШТЕГАМИ
def alg_scroll_with_hashatgs_start():
    # robot.start()
    # input("После аутентификации перейдите в ленту рекомендаций. В консоли нажмите Enter")
    # print("Окно браузера сделайте активным")
    #
    # # Инициализация скроллера с алгоритмами
    # algs = list()
    # algs.append(AlgorithmScroll2(robot))
    # handler = Handler(algs)
    # scroller = Scroller(robot, handler)
    # scroller.start()
    #
    # a = AlgorithmCustomization(robot)
    # try:
    #     a.start()
    # except Exception as ex:
    #     print(ex.__traceback__)
    pass
