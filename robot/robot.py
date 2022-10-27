import base64
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from seleniumwire import webdriver

from enums.button_type import ButtonType
from utils.utils import convert_str_time_to_seconds

BASE_ULR = "http://tiktok.com/"


def _get_driver_options():
    options = webdriver.ChromeOptions()

    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    #options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    return options


# Вынеcти в main ?
def _get_seleniumwire_options():
    # Декодирование тела ответа
    return {'disable_encoding': True}


class TikTokRobot:

    def __init__(self, url: str, driver_path: str):
        self.url = url
        self.driver_path = driver_path

        self.driver = webdriver.Chrome(
            executable_path=driver_path,
            seleniumwire_options=_get_seleniumwire_options(),
            chrome_options=_get_driver_options()
        )

        self.current_element = WebElement(None, None)

    def start(self):
        self.driver.get(self.url)

    def stop(self):
        self.driver.close()
        self.driver.quit()

    def scroll_to_element(self, to: WebElement):
        # ширина верхнего объекта на странице
        # TODO: в конфиги
        header_with = 60

        self.driver.execute_script("arguments[0].scrollIntoView();", to)
        self.driver.execute_script(f"window.scrollBy(0, {header_with * (-1)});")

        self.current_element = to

    def del_requests_history(self):
        del self.driver.requests

    def press_button(self, type: ButtonType):
        if type == ButtonType.ACCOUNT_LINK:
            self.current_element.find_element(By.CLASS_NAME, "tiktok-1lqhxf7-StyledAuthorAnchor").click()
            self.switch_to_new_window()
            # self.driver.find_element(By.CLASS_NAME, "tiktok-q6kzcs-MainDetailWrapper") - когда подает ошибка при открытии профиля

            self.open_first_publication()

            print()
            return

        if type == ButtonType.LIKE_IN_RECOMMEND:
            self.current_element.find_element(By.CLASS_NAME, "tiktok-1ok4pbl-ButtonActionItem").click()
            return

        if type == ButtonType.LIKE_IN_PUBLISH:
            self.driver.find_element(By.CLASS_NAME, "tiktok-z2k845-ButtonActionItem").click()
            return

        if type == ButtonType.NEXT_VIDEO:
            self.driver.find_element(By.CLASS_NAME,
                                     "tiktok-1yqxr7q-ButtonBasicButtonContainer-StyledVideoSwitchV2").click()

        if type == ButtonType.CLOSE_VIDEO:
            self.driver.find_element(By.CLASS_NAME,
                                     "iktok-1t78v6u-ButtonBasicButtonContainer-StyledCloseIconContainer").click()

        if type == ButtonType.RECOMMEND:
            self.driver.find_element(By.CLASS_NAME, "tiktok-1431rw4-StyledLinkLogo").click()

    def switch_to_new_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def driver_get_to(self, to: str):
        self.driver.get(f"{BASE_ULR}{to}")

    def get_url_by_key(self, key: str):
        requests = self.driver.requests

        for request in requests:
            if request.url.__contains__(key):
                return request.url

        return ""

    # Получение ответов на запросы получения рекомендованных видео
    def get_recommend_videos(self):

        requests = self.driver.requests
        # self.driver.requests.clear()
        responses = list()

        for request in requests:
            if request.path == "/api/recommend/item_list/":
                responses.append(request.response)

        return responses

    def get_publications_from_main_page(self):
        return self.driver.find_elements(By.CLASS_NAME, "tiktok-1nncbiz-DivItemContainer")

    # Открытие первого видео на странице автора, на странице с хэштегами
    def open_first_publication(self, count=0):
        try:
            self.driver.find_elements(By.CLASS_NAME, "tiktok-x6y88p-DivItemContainerV2")[1 + count * 2].click()
            self.switch_to_new_window()
        except Exception:
            print("open_first_publication. Не удалось найти публикации")
            self.open_first_publication()

    def get_video_duration(self):
        flag = False
        duration = 0
        attempts = 15

        # BUG
        while (not flag) & (attempts != 0):
            try:
                duration = convert_str_time_to_seconds(self.driver.find_element(By.CLASS_NAME, "tiktok-o2z5xv-DivSeekBarTimeContainer").text.split("/")[1])
                flag = True
            except Exception:
                flag = False
                time.sleep(1)
                attempts -= 1

        return duration

    def search_by_hashtags(self, hashtag: str):
        self.driver_get_to(f"tag/{hashtag}")
