# Part 1: Getting Started

In this section, you will learn how to set up a Python test automation project using pytest and Playwright. Please ensure you have read [README.md](../README.md) and [SETUP.md](/docs/SETUP.md) before proceeding.

## What is Playwright?

[Playwright](https://playwright.dev/python/) is a cutting-edge library that automates interactions with Chromium, Firefox, and WebKit browsers via a unified API. Developed by Microsoft, this open-source project is an excellent alternative to [Selenium WebDriver](https://www.selenium.dev/) for web UI testing.

Playwright offers several advantages over Selenium WebDriver, such as:

- Automatic waiting for elements to be ready during interactions.
- The ability to use one browser instance with multiple browser contexts for isolation.
- Device emulation for testing responsive web apps in mobile browsers.

For a detailed comparison, refer to [Why Playwright?](https://playwright.dev/python/docs/why-playwright/) in the documentation.

## Our Web Search Test

In this tutorial, we will demonstrate a test scenario for searching with DuckDuckGo, a search engine similar to Google or Yahoo.

The basic steps for a DuckDuckGo search are:

```gherkin
Given the DuckDuckGo home page is displayed
When the user searches for a phrase
Then the search result query is the phrase
And the search result links pertain to the phrase
And the search result title contains the phrase
```

Visit [DuckDuckGo](https://duckduckgo.com/) and try these steps manually with any search phrase of your choice. Always write a test *case* before writing test *code*, and manually test the scenario before automating it.

## Test Project Setup

Let's set up the test project from scratch. Use the GitHub repository as a reference for example code.

First, create a directory named `playwright-python-tutorial`:

```bash
$ mkdir playwright-python-tutorial
$ cd playwright-python-tutorial
```

Next, create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) using the [venv](https://docs.python.org/3/library/venv.html) module to manage dependencies locally:

```bash
$ python3 -m venv venv
```

This will create a subdirectory named `venv` that contains all virtual environment files, including dependency packages.

**Note about Python commands:** Python has two major versions: 2 and 3. Although Python 2 reached its end-of-life on January 1, 2020, many machines still run it. To ensure you're using Python 3, we will explicitly use `python3` and `pip3` in this tutorial.

Activate the virtual environment:

- On macOS or Linux:

  ```bash
  $ source venv/bin/activate
  ```

- On Windows command line:

  ```
  > venv\Scripts\activate.bat
  ```

You can verify the virtual environment is active if its name appears in the command prompt.

Install the necessary Python packages:

```bash
$ pip3 install playwright
$ pip3 install pytest
$ pip3 install pytest-playwright
```

> If you prefer to run tests from this repository instead of creating a new project, install the dependencies using:
>
> ```bash
> $ pip3 install -r requirements.txt
> ```

Playwright is a browser automation library, and pytest is a test framework. The [`pytest-playwright`](https://playwright.dev/python/docs/test-runners) plugin simplifies the integration of Playwright with pytest.

Verify the installed packages using `pip3 freeze`. The output should be similar to this:

```bash
$ pip3 freeze
attrs==21.2.0
certifi==2021.10.8
charset-normalizer==2.0.8
greenlet==1.1.2
idna==3.3
iniconfig==1.1.1
packaging==21.3
playwright==1.19.1
pluggy==1.0.0
py==1.11.0
pyee==8.1.0
pyparsing==3.0.6
pytest==7.0.1
pytest-base-url==1.4.2
pytest-playwright==0.2.3
python-slugify==5.0.2
requests==2.26.0
text-unidecode==1.3
toml==0.10.2
tomli==2.0.1
urllib3==1.26.7
websockets==10.1
```

It is a common practice to store this list of dependencies in a file named `requirements.txt`.

Next, install the browsers for Playwright using the `playwright install` command, which installs the latest versions of Chromium, Firefox, and WebKit:

```bash
$ playwright install
```

By default, pytest with the Playwright plugin will run headless Chromium. We'll show how to run tests on other browsers in Part 5.

Create a test function stub. By convention, all tests should be under a `tests` directory. Create this directory and a file named `test_search.py`:

```bash
$ mkdir tests
$ touch tests/test_search.py
```

Add the following code to `tests/test_search.py`:

```python
def test_basic_duckduckgo_search() -> None:
    # Given the DuckDuckGo home page is displayed
    # When the user searches for a phrase
    # Then the search result query is the phrase
    # And the search result links pertain to the phrase
    # And the search result title contains the phrase
    pass
```

The `test_basic_duckduckgo_search` function is a stub but follows best practices:

- It has a descriptive name.
- It outlines the behavior to test in comments.
- It can be executed immediately.

The `pass` statement is a no-op, not an indication that the test passes.

Remember, always write test *cases* before writing test *code*.

To ensure everything is set up correctly, run this test:

```bash
$ python3 -m pytest tests
```

pytest should discover, run, and pass the single test case under the `tests` directory.

**Note about the pytest command:** Some resources use the `pytest` command directly, such as `pytest tests`. However, this does not add the current directory to the Python path, which can cause failures if your tests reference anything outside their modules. Therefore, always use the full `python3 -m pytest tests` command.
