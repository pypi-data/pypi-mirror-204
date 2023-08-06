import time
from typing import List, Any, final
from abc import ABCMeta, abstractmethod

from selenium.common.exceptions import NoSuchElementException

from psdelivery.utils.type_checker import must_be_type
from psdelivery.core.engine import CrawlingEngine
from psdelivery.core.item import ProblemItem


class ProblemCrawler(metaclass=ABCMeta):
    base_url: str
    engine: CrawlingEngine

    @final
    def open(self) -> None:
        self.engine.open()

    @final
    def close(self) -> None:
        self.engine.close()

    @final
    def __del__(self) -> None:
        self.close()

    @final
    def open_web(self, url: str = None):
        if not url:
            url = self.base_url
        self.engine.open_web(url)

    @abstractmethod
    def generate_url_by_page_index(self, page: int = 1) -> str: ...

    @abstractmethod
    def access_to_problem_list(self, page: int = 1) -> None: ...

    @abstractmethod
    def get_problem_elements(self) -> List[Any]: ...

    @abstractmethod
    def parse_problem_from_problem_element(self, item: Any) -> ProblemItem | None: ...

    @final
    @must_be_type('page', int)
    def get_list(self, page: int = 1) -> List[ProblemItem]:
        self.target_url: str = self.generate_url_by_page_index(page)
        if page < 0:
            raise ValueError('page is must not be under 0.')

        self.open()
        self.open_web(self.target_url)
        self.access_to_problem_list()
        items = self.get_problem_elements(page)
        problems: List[ProblemItem] = []
        for item in items:
            try:
                problem = self.parse_problem_from_problem_element(item)
            except NoSuchElementException:
                continue
            else:
                if problem:
                    problems.append(problem)
        self.close()
        return problems
