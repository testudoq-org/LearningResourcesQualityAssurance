"""
These tests cover DuckDuckGo searches using data driven with a text file.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import pytest
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import expect, Page


# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

DUCKDUCKGO_URL = 'https://duckduckgo.com/'
ANIMALS_FILE_PATH = 'animals.txt'  # Update with the correct path

# Load animals from plain text file
def load_animals(file_path: str) -> list[str]:
    """Load a list of animals from a plain text file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

ANIMALS = load_animals(ANIMALS_FILE_PATH)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def load_homepage(search_page: DuckDuckGoSearchPage) -> None:
    """Load the DuckDuckGo homepage."""
    search_page.load()


def perform_search(search_page: DuckDuckGoSearchPage, phrase: str) -> None:
    """Perform a search on DuckDuckGo."""
    search_page.search(phrase)


def verify_search_results(
    result_page: DuckDuckGoResultPage,
    page: Page,
    phrase: str) -> None:
    """Verify the search results page."""
    expect(result_page.search_input).to_have_value(phrase)
    assert result_page.result_link_titles_contain_phrase(phrase)
    expect(page).to_have_title(f'{phrase} at DuckDuckGo')


# ------------------------------------------------------------
# Test Function
# ------------------------------------------------------------

@pytest.mark.parametrize('phrase', ANIMALS)
def test_basic_duckduckgo_search(
    phrase: str,
    page: Page,
    search_page: DuckDuckGoSearchPage,
    result_page: DuckDuckGoResultPage) -> None:
    """
    Test searching for a phrase on DuckDuckGo.
    
    :param phrase: Search phrase to use.
    :param page: Playwright page object.
    :param search_page: DuckDuckGo search page object.
    :param result_page: DuckDuckGo result page object.
    """
    # Given the DuckDuckGo home page is displayed
    load_homepage(search_page)

    # When the user searches for a phrase
    perform_search(search_page, phrase)

    # Then the search result query is the phrase
    # And the search result links pertain to the phrase
    # And the search result title contains the phrase
    verify_search_results(result_page, page, phrase)
