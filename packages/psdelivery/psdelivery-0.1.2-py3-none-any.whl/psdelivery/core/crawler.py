from typing import List, Any, final
from abc import ABCMeta, abstractmethod

from selenium.common.exceptions import NoSuchElementException

from psdelivery.utils.type_checker import must_be_type
from psdelivery.core.engine import CrawlingEngine
from psdelivery.core.item import ProblemItem
from psdelivery.utils.logger import print_status, LogStatus


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
    def get_list(self, page: int = 1, logging: bool = False) -> List[ProblemItem]:
        self.target_url: str = self.generate_url_by_page_index(page)
        if page < 0:
            raise ValueError('page is must not be under 0.')

        print_status(logging, LogStatus.PROGRESS, 'Open Website...')
        self.open()
        self.open_web(self.target_url)
        print_status(logging, LogStatus.SUCCESS, 'Open Website...')

        print_status(logging, LogStatus.PROGRESS, 'Collect Problems...')
        self.access_to_problem_list()
        items = self.get_problem_elements(page)
        print_status(logging, LogStatus.SUCCESS, 'Collect Problems...')

        print_status(logging, LogStatus.PROGRESS, 'Parsing Problems...')
        problems: List[ProblemItem] = []
        sum_cnt = len(items)
        for i, item in enumerate(items):
            try:
                problem = self.parse_problem_from_problem_element(item)
                print_status(logging, None, f'Parsing Problem {i+1}/{sum_cnt}')
            except NoSuchElementException:
                continue
            else:
                if problem:
                    problems.append(problem)
        print_status(logging, LogStatus.SUCCESS, 'Parsing Problems...')

        print_status(logging, LogStatus.PROGRESS, 'Close Website...')
        self.close()
        print_status(logging, LogStatus.SUCCESS, 'Close Website...')

        return problems
