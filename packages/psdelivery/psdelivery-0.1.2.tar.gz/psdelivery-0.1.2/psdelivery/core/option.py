from abc import ABCMeta, abstractmethod
from typing import final

from selenium import webdriver


class CrawlerOption(metaclass=ABCMeta):
    @abstractmethod
    def generate(self) -> webdriver.ChromeOptions: ...

@final
class DefaultSeleniumCrawlerOption(CrawlerOption):
    def generate(self) -> webdriver.ChromeOptions:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        return chrome_options
