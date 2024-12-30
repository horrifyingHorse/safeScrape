from playwright.async_api import Browser, Playwright, async_playwright


class AppState:
    def __init__(self):
        self.auto_launch: bool = False
        self.index: int = 0  # Service Index
        self.services: list[str] = [
            "instagram.com",
            "github.com",
            "discord.com",
        ]
        self.status: bool = True  # Playwright is running?


class PageState:
    def __init__(self):
        self.auto_login: bool = False
        self.storage_state: str = ""  # Session Info
        self.service: str = "instagram.com"
        self.custom_url: str = ""
        self.scrape: bool = False
        self.allow_delay: bool = True
        self.execute: bool = False


# Singleton Approach
class BrowserManager:
    playwright_instance: Playwright | None = None
    browser: Browser | None = None

    @classmethod
    async def getBrowser(cls) -> Browser:
        if cls.browser is not None:
            print("exists: ", cls.browser)
            return cls.browser

        if cls.playwright_instance is None:
            cls.playwright_instance = await async_playwright().start()

        cls.browser = await cls.playwright_instance.chromium.launch(headless=False)
        print("created: ", cls.browser)
        return cls.browser

    @classmethod
    async def killBrowser(cls) -> None:
        if cls.browser is not None:
            await cls.browser.close()
            cls.browser = None
        if cls.playwright_instance is not None:
            await cls.playwright_instance.stop()
            cls.playwright_instance = None
        return


appstate = AppState()
pagestate = PageState()
