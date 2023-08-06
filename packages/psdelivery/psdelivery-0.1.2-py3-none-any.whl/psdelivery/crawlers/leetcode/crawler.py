import time
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from psdelivery.core.crawler import ProblemCrawler
from psdelivery.core.engine import SeleniumEngine
from psdelivery.crawlers.leetcode.item import LeetcodeProblemItem


class LeetcodeCrawler(ProblemCrawler):
    base_url = 'https://leetcode.com/problemset/all'
    engine = SeleniumEngine()
    difficulty_str_to_int = {'Easy': 1,  'Medium': 2, 'Hard': 3}

    def generate_url_by_page_index(self, page: int = 1) -> str:
        return self.base_url + '/?page=' + str(page)

    def access_to_problem_list(self) -> None:
        time.sleep(2)

    def get_problem_elements(self, page: int = 1) -> List[WebElement]:
        maxinum_page = int(
            self.engine() \
                .find_element(By.XPATH, '//nav[@role = "navigation"]') \
                .find_elements(By.TAG_NAME, 'button')[-2].text
        )
        if page > maxinum_page:
            return []

        return self.engine() \
                .find_element(By.XPATH, '//div[@role = "rowgroup"]') \
                .find_elements(By.XPATH, './/div[@role="row"]')
    
    def parse_problem_from_problem_element(
            self, item: WebElement) -> LeetcodeProblemItem | None:
        title, difficulty, seq, website = None, None, None, None
        
        attr_iter = enumerate(
            item.find_elements(By.XPATH, './/div[@role="cell"]'))
        for i, attr in attr_iter:
            if i == 1:
                title_raw: str = attr.find_element(
                    By.XPATH, './/div[@class="truncate"]/a').text
                
                title = '.'.join(title_raw.split('.')[1:])[1:]
                seq = title.lower().replace(' ', '-')
                website = f'https://leetcode.com/problems/{seq}/'

            elif i == 4:
                raw_difficulty = attr.find_element(By.TAG_NAME, 'span').text
                difficulty = self.difficulty_str_to_int[raw_difficulty]

        return LeetcodeProblemItem(seq, title, website, difficulty)
