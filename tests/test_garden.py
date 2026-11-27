from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import Browser, Page, sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[1]
PLANT_ASSETS = {
    "plant.svg": "A leafy green plant in a terracotta pot",
    "cactus.svg": "A green cactus in a terracotta pot",
    "sunflower.svg": "A yellow sunflower in a terracotta pot",
    "succulent.svg": "A rosette succulent in a terracotta pot",
}


class QuietRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture(scope="session")
def base_url():
    handler = lambda *args, **kwargs: QuietRequestHandler(
        *args, directory=str(REPO_ROOT), **kwargs
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url)
    yield page
    context.close()


def test_initial_state_is_empty(page: Page) -> None:
    assert page.get_by_text("Plants planted: 0").is_visible()
    assert page.get_by_role("group", name="Your garden").locator("img").count() == 0


def test_planting_adds_one_valid_image_and_updates_count(page: Page) -> None:
    plant_button = page.get_by_role("button", name="Plant a seedling")
    garden = page.get_by_role("group", name="Your garden")

    for expected_count in range(1, 4):
        plant_button.click()
        assert garden.locator("img").count() == expected_count
        assert page.locator("#count").inner_text() == str(expected_count)

    images = garden.locator("img")
    for image in images.all():
        source = image.get_attribute("src")
        assert source in PLANT_ASSETS
        assert image.get_attribute("alt") == PLANT_ASSETS[source]
        assert image.evaluate(
            "(img) => img.complete && img.naturalWidth > 0"
        ), f"Plant image did not load: {source}"
        response = page.request.get(f"{page.url.rsplit('/', 1)[0]}/{source}")
        assert response.ok
        assert "image/svg+xml" in response.headers.get("content-type", "")


def test_reset_clears_garden_and_planting_still_works(page: Page) -> None:
    plant_button = page.get_by_role("button", name="Plant a seedling")
    garden = page.get_by_role("group", name="Your garden")
    plant_button.click()
    plant_button.click()
    assert garden.locator("img").count() == 2

    page.get_by_role("button", name="Reset").click()
    assert garden.locator("img").count() == 0
    assert page.locator("#count").inner_text() == "0"

    plant_button.click()
    assert garden.locator("img").count() == 1
    assert page.locator("#count").inner_text() == "1"


def test_actions_are_keyboard_reachable_and_activatable(page: Page) -> None:
    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.id") == "plant"
    page.keyboard.press("Enter")
    assert page.locator("#count").inner_text() == "1"

    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.id") == "reset"
    page.keyboard.press("Enter")
    assert page.locator("#count").inner_text() == "0"

    page.keyboard.press("Shift+Tab")
    assert page.evaluate("document.activeElement.id") == "plant"
    page.keyboard.press("Space")
    assert page.locator("#count").inner_text() == "1"
