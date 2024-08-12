from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse
from typing import Literal

class Model:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self._base_url = "https://www.forexfactory.com/calendar"

    def launch(self, url) -> (Literal[False] | None):
        parsed_url = urlparse(url)
        if self._base_url not in url and not all([parsed_url.scheme, parsed_url.netloc]):
            return False
        
        self.driver.get(url)

    def scroller(self) -> None:
        while True:
            # Record the current scroll position
            before_scroll = self.driver.execute_script("return window.pageYOffset;")
            
            # Scroll down a fixed amount
            self.driver.execute_script("window.scrollTo(0, window.pageYOffset + 500);")
            
            # Wait for a short moment to allow content to load
            time.sleep(1)
            
            # Record the new scroll position
            after_scroll = self.driver.execute_script("return window.pageYOffset;")
            
            # If the scroll position hasn't changed, we've reached the end of the page
            if before_scroll == after_scroll:
                break
