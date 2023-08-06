from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from psdelivery.core.engine import SeleniumEngine

from psdelivery.crawlers.baekjoon.item import BaekjoonProblemItem
from psdelivery.core.crawler import ProblemCrawler


class BaekjoonProblemListItemParser:
    item: WebElement

    def __init__(self, item: WebElement):
        self.item = item

    @property
    def seq(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-1raije9')  \
                        .find_element(By.TAG_NAME, 'span').text

    @property
    def web_difficulty(self) -> str:
        img_url = self.item.find_element(By.CLASS_NAME, 'css-1raije9') \
                        .find_element(By.TAG_NAME, 'img').get_attribute('src')
        return img_url.split('/')[-1].split('.')[0]

    @property
    def title(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-d6mf5j') \
                        .find_element(By.CLASS_NAME, '__Latex__').text

    @property
    def website(self) -> str:
        return self.item.find_element(By.CLASS_NAME, 'css-d6mf5j') \
                    .find_element(By.TAG_NAME, 'a').get_attribute('href')


class BaekjoonCrawler(ProblemCrawler):
    base_url = 'https://solved.ac/search?query=*'
    engine = SeleniumEngine()
    
    def generate_url_by_page_index(self, page: int = 1) -> str:
        return self.base_url + '&page=' + str(page)

    def access_to_problem_list(self, page: int = 1):
        self.engine().refresh()
        self.engine().implicitly_wait(3)

    def get_problem_elements(self, page: int = 1) -> List[WebElement]:
        items = self.engine().find_elements(By.CLASS_NAME, 'css-1ojb0xa')
        return items
    
    def convert_difficulty_to_int(self, difficulty: str) -> int | None:
        if difficulty == 'nr' or difficulty == '0':
            # 난이도가 책정되어 있지 않은 문제는 제외시킴
            return None
        if difficulty == 'sprout':
            # 새싹문제는 브론즈5
            return 1
        return int(difficulty)

    def parse_problem_from_problem_element(
            self, item: WebElement) -> BaekjoonProblemItem | None:
        parser = BaekjoonProblemListItemParser(item)

        seq = parser.seq
        difficulty = self.convert_difficulty_to_int(parser.web_difficulty)
        title = parser.title
        website = parser.website
        
        if not difficulty:
            return None

        return BaekjoonProblemItem(seq, title, website, difficulty)
