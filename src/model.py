from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse
from typing import Literal

from src.utils import reformat_scraped_data
from src.config import ALLOWED_ELEMENT_TYPES, ICON_COLOR_MAP


class Model:
    def __init__(self) -> None:
        self.driver = None
        self.url: str = ""
        self.base_url = "https://www.forexfactory.com/calendar"
        self._data = []
        self._table = None

    def launch(self) -> Literal[False] | None:
        self.driver = webdriver.Chrome()
        parsed_url = urlparse(self.url)
        if self.base_url not in self.url and not all(
            [parsed_url.scheme, parsed_url.netloc]
        ):
            return False

        self.driver.get(self.url)
        self._table = self.driver.find_element(By.CLASS_NAME, "calendar__table")

    def scroller(self) -> None:
        while True:
            # Record the current scroll position
            before_scroll = self.driver.execute_script("return window.pageYOffset;")

            # Scroll down a fixed amount
            self.driver.execute_script("window.scrollTo(0, window.pageYOffset + 500);")

            # Wait for a short moment to allow content to load
            time.sleep(0.5)

            # Record the new scroll position
            after_scroll = self.driver.execute_script("return window.pageYOffset;")

            # If the scroll position hasn't changed, we've reached the end of the page
            if before_scroll == after_scroll:
                break

    def scraper(self):
        for row in self._table.find_elements(By.TAG_NAME, "tr"):
            row_data = []
            for element in row.find_elements(By.TAG_NAME, "td"):
                class_name = element.get_attribute("class")
                if class_name in ALLOWED_ELEMENT_TYPES:
                    if element.text:
                        row_data.append(element.text)
                    elif "calendar__impact" in class_name:
                        impact_elements = element.find_elements(By.TAG_NAME, "span")
                        for impact in impact_elements:
                            impact_class = impact.get_attribute("class")
                            color = ICON_COLOR_MAP[impact_class]
                        if color:
                            row_data.append(color)
                        else:
                            row_data.append("impact")

            if len(row_data):
                self._data.append(row_data)

        reformat_scraped_data(self._data, "test")

    def shutdown(self):
        self.driver.close()
