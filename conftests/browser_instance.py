from playwright.sync_api import Page, sync_playwright, Browser, BrowserContext
from pytest import fixture

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


@fixture
def result_page(page: Page) -> DuckDuckGoResultPage:
    return DuckDuckGoResultPage(page)


@fixture
def search_page(page: Page) -> DuckDuckGoSearchPage:
    return DuckDuckGoSearchPage(page)


# Create Customize browser instance
@fixture(scope='session')
def browser(config):
    browser_config = config['browser']
    headed_mode_config = config['active_headed_mode']
    playwright = sync_playwright().start()
    browser_args = {"headless": False} if headed_mode_config else {}
    browsers = {
        "chrome": playwright.chromium,
        "firefox": playwright.firefox,
        "webkit": playwright.webkit,
    }
    browser_instance = browsers.get(browser_config, browsers['chrome']).launch(
        **browser_args
    )
    yield browser_instance
    browser_instance.close()


@fixture
def context(browser: Browser):
    context_instance = browser.new_context()
    return context_instance


@fixture
def page(context: BrowserContext):
    page_instance = context.new_page()
    yield page_instance
    page_instance.close()
