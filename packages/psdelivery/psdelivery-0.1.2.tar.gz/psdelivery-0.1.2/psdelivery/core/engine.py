from typing import Any, final
from abc import ABCMeta, abstractmethod
import time

import requests
from requests import Response
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from psdelivery.core.option import CrawlerOption, DefaultSeleniumCrawlerOption
from psdelivery.exc import RequestTimeout, RequestFailed, WebdriverIsNotLoaded


class CrawlingEngine(metaclass=ABCMeta):
    engine: Any | None = None
    
    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def open_web(self, url: str) -> None: ...

    @final
    def __call__(self) -> Any | None:
        return self.engine


@final
class BeautifulSoupEngine(CrawlingEngine):
    engine: BeautifulSoup | None = None

    def open(self) -> None: ...
    def close(self) -> None: ...

    def open_web(self, url: str) -> None:
        try:
            response: Response = requests.get(url, timeout=30)
        except TimeoutError:
            raise RequestTimeout('Request timeout.')

        if response.status_code == 200:
            self.engine = BeautifulSoup(response.text, 'html.parser')
        else:
            raise RequestFailed('Request failed to web.')


@final
class SeleniumEngine(CrawlingEngine):
    engine: webdriver.Chrome
    option_generator: CrawlerOption = DefaultSeleniumCrawlerOption()

    def open(self) -> None:
        self.engine = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.option_generator.generate())
        
    def close(self) -> None:
        if self.engine:
            self.engine.quit()

    def open_web(self, url: str) -> None:
        if self.engine:
            self.engine.get(url)
            time.sleep(2)
        else:
            raise WebdriverIsNotLoaded('Selenium webdriver is not loaded.')
