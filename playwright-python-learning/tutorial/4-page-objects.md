# Part 4: Refactoring Using Page Objects

In the previous part, we saw how concise Playwright calls can be. While it might be tempting to use raw Playwright calls in all tests, doing so can lead to code duplication. In this part, we will refactor our DuckDuckGo search test using the [Page Object Model (POM)](https://www.selenium.dev/documentation/guidelines/page_object_models/). Page objects provide structure and reusability, making them superior to raw Playwright calls, especially when automating multiple tests.

## The Search Page

Our search test interacts with two pages:
1. The DuckDuckGo search page
2. The DuckDuckGo result page

Each page should be modeled by its own class. Page object classes should be located in a package outside of the `tests` directory so that they can be imported by tests.

Create a new directory named `pages`, and inside it, create the following files:
* `__init__.py`
* `search.py`
* `result.py`

Your project directory should look like this:
```
playwright-python-tutorial
├── pages
│   ├── __init__.py
│   ├── search.py
│   └── result.py
└── tests
    └── test_search.py
```

The `__init__.py` file turns the `pages` directory into a Python package, and it will stay empty. The `search.py` and `result.py` modules will contain the search and result page object classes, respectively.

### Implementing the Search Page

A page object class typically has three main parts:
1. Dependency injection of the browser automator through a constructor
2. Locators and other data stored as variables
3. Interaction methods that use the browser automator and the selectors

Inside `pages/search.py`, import Playwright's `Page` class:
```python
from playwright.sync_api import Page
```

Add a class definition for the page object:
```python
class DuckDuckGoSearchPage:
```

Inside this class, add the DuckDuckGo URL:
```python
    URL = 'https://www.duckduckgo.com'
```

> **Warning:** Base URLs should typically be passed into automation code as an input, not hard-coded in a page object. We are doing this here for simplicity.

Next, handle dependency injection for the browser automator. Add the following initializer method to the class:
```python
    def __init__(self, page: Page) -> None:
        self.page = page
```

Add locators for search page elements to the constructor:
```python
        self.search_button = page.locator('#search_button_homepage')
        self.search_input = page.locator('#search_form_input_homepage')
```

Add a method to load the DuckDuckGo search page:
```python
    def load(self) -> None:
        self.page.goto(self.URL)
```

Add a method to perform a search:
```python
    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.search_button.click()
```

The completed search page object class should look like this:
```python
from playwright.sync_api import Page

class DuckDuckGoSearchPage:

    URL = 'https://www.duckduckgo.com'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_button = page.locator('#search_button_homepage')
        self.search_input = page.locator('#search_form_input_homepage')
    
    def load(self) -> None:
        self.page.goto(self.URL)
    
    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.search_button.click()
```

### Refactoring the Test Case

Replace the old code in `tests/test_search.py` with the new code:
```python
from pages.search import DuckDuckGoSearchPage

def test_basic_duckduckgo_search(page: Page) -> None:
    search_page = DuckDuckGoSearchPage(page)
    
    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('testudo')
```

The new code imports `DuckDuckGoSearchPage` from the `pages.search` module. The test constructs a `DuckDuckGoSearchPage` object and uses it to perform interactions. The test case no longer has hard-coded selectors or URLs, making the code more self-documenting.

Run the test (`python3 -m pytest tests --headed --slowmo 1000`). The test should pass.

## The Result Page

After writing the search page class, the result page class will be straightforward. The main difference is that each interaction method in the result page class will return a value because test assertions will check page values.

### Implementing the Result Page

Add the following imports for type checking to `pages/result.py`:
```python
from playwright.sync_api import Page
from typing import List
```

Add the class definition:
```python
class DuckDuckGoResultPage:
```

Add dependency injection with locators:
```python
    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
```

Add methods to get all result link titles and check if the list of result link titles contains a phrase:
```python
    def result_link_titles(self) -> List[str]:
        self.result_links.nth(4).wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum
```

The full code for `pages/result.py` should look like this:
```python
from playwright.sync_api import Page
from typing import List

class DuckDuckGoResultPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.result_links = page.locator('a[data-testid="result-title-a"]')
        self.search_input = page.locator('#search_form_input')
    
    def result_link_titles(self) -> List[str]:
        self.result_links.nth(4).wait_for()
        return self.result_links.all_text_contents()
    
    def result_link_titles_contain_phrase(self, phrase: str, minimum: int = 1) -> bool:
        titles = self.result_link_titles()
        matches = [t for t in titles if phrase.lower() in t.lower()]
        return len(matches) >= minimum
```

### Refactoring the Test Case

Rewrite the test case in `tests/test_search.py` to use `DuckDuckGoResultPage`:
```python
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import expect, Page

def test_basic_duckduckgo_search(page: Page) -> None:
    search_page = DuckDuckGoSearchPage(page)
    result_page = DuckDuckGoResultPage(page)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('testudo')

    # Then the search result query is the phrase
    expect(result_page.search_input).to_have_value('testudo')

    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase('testudo')

    # And the search result title contains the phrase
    expect(page).to_have_title('panda at DuckDuckGo')
```

Run the test to ensure it still works.

## Page Object Fixtures

To maximize the value of our new page objects, we can create fixtures to automatically construct them. In pytest, shared fixtures belong in a module under the `tests` directory named `conftest.py`. Create a new file at `tests/conftest.py` and add the following code:
```python
import pytest

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import Page

@pytest.fixture
def result_page(page: Page) -> DuckDuckGoResultPage:
    return DuckDuckGoResultPage(page)

@pytest.fixture
def search_page(page: Page) -> DuckDuckGoSearchPage:
    return DuckDuckGoSearchPage(page)
```

Rewrite the test case in `tests/test_search.py` to use these fixtures:
```python
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage
from playwright.sync_api import expect, Page

def test_basic_duckduckgo_search(
    page: Page,
    search_page: DuckDuckGoSearchPage,
    result_page: DuckDuckGoResultPage) -> None:
    
    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for a phrase
    search_page.search('testudo')

    # Then the search result query is the phrase
    expect(result_page.search_input).to_have_value('testudo')

    # And the search result links pertain to the phrase
    assert result_page.result_link_titles_contain_phrase('testudo')

    # And the search result title contains the phrase
    expect(page).to_have_title('panda at DuckDuckGo')
```

Run the test one more time to ensure everything works as expected.

Congratulations! You have successfully refactored your test case using page objects. You can learn more about Playwright and Python from the [Playwright documentation](https://playwright.dev/python/docs/intro).

This concludes the tutorial. Thank you for following along. I hope you found this material useful.
