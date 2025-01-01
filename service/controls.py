from playwright.async_api import Browser, Page, Playwright, async_playwright
from pydantic import BaseModel


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


class PageState(BaseModel):
    auto_login: bool = False
    storage_state: str = ""  # Session Info
    service: str = "instagram.com"
    custom_url: str = ""
    scrape: bool = False
    allow_delay: bool = True
    execute: bool = False


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
        await PageManager.clear()
        return


class PageManager:
    class PageStorage:
        def __init__(self, page: Page, state: PageState):
            self.page: Page = page
            self.state: PageState = state

    pages: dict[int, PageStorage] = {}
    id: int = 0

    @classmethod
    async def addPage(cls, page: Page, state: PageState) -> int:
        cls.pages[cls.id] = cls.PageStorage(page=page, state=state)
        cls.id += 1
        return cls.id - 1

    @classmethod
    async def updatePage(cls, id: int, state: PageState) -> bool:
        if id < 0 or id > cls.id:
            print(f"Illegal id, recieved {id}")
            return False
        cls.pages[id].state = state
        return True

    @classmethod
    async def getPage(cls, id: int) -> tuple[Page, PageState]:
        if id < 0 or id > cls.id:
            print(f"Illegal id, recieved {id}")
        return (cls.pages[id].page, cls.pages[id].state)

    @classmethod
    async def clear(cls) -> None:
        cls.id = 0
        cls.pages = {}
        return


appstate = AppState()
pagestate = PageState()
