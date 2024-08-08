"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""

from playwright.sync_api import Page, Locator


class DuckDuckGoSearchPage:
    """Page object for the DuckDuckGo search page."""

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page: Page) -> None:
        """
        Initialize the DuckDuckGo search page object.

        Args:
            page (Page): The Playwright Page object.
        """
        self.page: Page = page
        self.search_button: Locator = page.locator('#search_button_homepage')
        self.search_input: Locator = page.locator('#search_form_input_homepage')
    
    def load(self) -> None:
        """
        Load the DuckDuckGo search page.
        """
        self.page.goto(self.URL)
    
    def search(self, phrase: str) -> None:
        """
        Perform a search using the given phrase.

        Args:
            phrase (str): The search query to input.
        """
        self.search_input.fill(phrase)
        self.search_button.click()
        # Optionally, wait for the results to be visible or loaded
        self.page.locator('#search').wait_for()  # Adjust the selector as necessary
