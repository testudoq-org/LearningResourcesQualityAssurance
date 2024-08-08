"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo result page.
"""

from playwright.sync_api import Page, Locator
from typing import List


class DuckDuckGoResultPage:
    """Page object for the DuckDuckGo result page."""
    
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.result_links: Locator = page.locator('a[data-testid="result-title-a"]')
        self.search_input: Locator = page.locator('#search_form_input')

    def result_link_titles(self) -> List[str]:
        """
        Retrieve all result link titles from the result page.

        Returns:
            List[str]: A list of result link titles.
        """
        # Wait for the links to be available to ensure we retrieve the correct data
        self.result_links.first.wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        """
        Check if the result link titles contain the given phrase.

        Args:
            phrase (str): The phrase to search for in the link titles.
            minimum (int, optional): Minimum number of titles that should contain the phrase. Defaults to 1.

        Returns:
            bool: True if the number of titles containing the phrase meets or exceeds the minimum, otherwise False.
        """
        titles = self.result_link_titles()
        # Use a list comprehension to find matching titles
        matches = [title for title in titles if phrase.lower() in title.lower()]
        return len(matches) >= minimum
