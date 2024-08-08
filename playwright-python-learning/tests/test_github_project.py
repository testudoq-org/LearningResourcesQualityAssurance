"""
These tests cover API interactions for GitHub projects.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import time
from playwright.sync_api import APIRequestContext, Page, expect

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

GITHUB_LOGIN_URL = 'https://github.com/login'
GITHUB_PROJECTS_URL = 'https://github.com/users/{username}/projects/{project_number}'

LOGIN_FIELD_SELECTOR = 'id=login_field'
PASSWORD_FIELD_SELECTOR = 'id=password'
LOGIN_BUTTON_SELECTOR = 'input[name="commit"]'


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def login(page: Page, username: str, password: str) -> None:
    """Log into GitHub."""
    page.goto(GITHUB_LOGIN_URL)
    page.locator(LOGIN_FIELD_SELECTOR).fill(username)
    page.locator(PASSWORD_FIELD_SELECTOR).fill(password)
    page.locator(LOGIN_BUTTON_SELECTOR).click()


def get_card_xpath(column_id: str, note: str) -> str:
    """Generate the XPath for a card in a column based on the note."""
    return f'//div[@id="column-cards-{column_id}"]//p[contains(text(), "{note}")]'


# ------------------------------------------------------------
# A pure API test
# ------------------------------------------------------------

def test_create_project_card(
    gh_context: APIRequestContext,
    project_column_ids: list[str]
) -> None:
    """
    Test creating a new project card via API and verifying its creation.
    """
    # Prep test data
    now = time.time()
    note = f'A new task at {now}'

    # Create a new card
    create_response = gh_context.post(
        f'/projects/columns/{project_column_ids[0]}/cards',
        data={'note': note}
    )
    expect(create_response).to_be_ok()
    assert create_response.json()['note'] == note

    # Retrieve the newly created card
    card_id = create_response.json()['id']
    retrieve_response = gh_context.get(f'/projects/columns/cards/{card_id}')
    expect(retrieve_response).to_be_ok()
    assert retrieve_response.json() == create_response.json()


# ------------------------------------------------------------
# A hybrid UI/API test
# ------------------------------------------------------------

def test_move_project_card(
    gh_context: APIRequestContext,
    gh_project: dict,
    project_column_ids: list[str],
    page: Page,
    gh_username: str,
    gh_password: str
) -> None:
    """
    Test moving a project card from one column to another using both API and UI.
    """
    # Prep test data
    source_col = project_column_ids[0]
    dest_col = project_column_ids[1]
    now = time.time()
    note = f'Move this card at {now}'

    # Create a new card via API
    create_response = gh_context.post(
        f'/projects/columns/{source_col}/cards',
        data={'note': note}
    )
    expect(create_response).to_be_ok()

    # Log in via UI
    login(page, gh_username, gh_password)

    # Load the project page
    project_url = GITHUB_PROJECTS_URL.format(username=gh_username, project_number=gh_project["number"])
    page.goto(project_url)

    # Verify the card appears in the first column
    card_xpath = get_card_xpath(source_col, note)
    expect(page.locator(card_xpath)).to_be_visible()

    # Move a card to the second column via web UI
    page.drag_and_drop(f'text="{note}"', f'id=column-cards-{dest_col}')

    # Verify the card is in the second column via UI
    card_xpath = get_card_xpath(dest_col, note)
    expect(page.locator(card_xpath)).to_be_visible()

    # Verify the backend is updated via API
    card_id = create_response.json()['id']
    retrieve_response = gh_context.get(f'/projects/columns/cards/{card_id}')
    expect(retrieve_response).to_be_ok()
    assert retrieve_response.json()['column_url'].endswith(str(dest_col))
