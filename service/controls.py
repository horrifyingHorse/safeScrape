import asyncio
from random import randint

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
    new_state: bool = False
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
    async def killBrowser(cls) -> tuple[bool, str]:
        if cls.browser is not None:
            await cls.browser.close()
            cls.browser = None
            if cls.playwright_instance is not None:
                await cls.playwright_instance.stop()
                cls.playwright_instance = None
        else:
            return (False, "Browser does not exist. No browser to close")
        await PageManager.clear()
        return (True, "success")


class ScrapedData(BaseModel):
    MsgId: int = -1
    ReplyTo: str | None = None
    Author: str = ""
    Content: str = ""


class PageManager:
    class PageStorage:
        def __init__(self, page: Page, state: PageState, ws_addr: int):
            self.page: Page = page
            self.state: PageState = state
            self.ws_addr: int = ws_addr

    pages: dict[int, PageStorage] = {}
    scrapedData: dict[int, list[ScrapedData]] = {}
    id: int = 0  # Static ID

    @classmethod
    async def insertData(
        cls,
        id: int,
        MsgId: int = -1,
        ReplyTo: str | None = None,
        Author: str = "",
        Content: str = "",
    ):
        if not await cls.idCheck(id):
            return False
        cls.scrapedData[id].append(
            ScrapedData(MsgId=MsgId, ReplyTo=ReplyTo, Author=Author, Content=Content)
        )
        return

    @classmethod
    async def pollData(cls, id: int) -> int:
        length: int = len(cls.scrapedData[id])
        while True:
            if len(cls.scrapedData[id]) != length:
                return len(cls.scrapedData[id]) - length
            await asyncio.sleep(0.5)

    @classmethod
    async def addPage(cls, page: Page, state: PageState) -> tuple[int, int]:
        ws_addr = randint(1000, 9999)
        cls.pages[cls.id] = cls.PageStorage(page=page, state=state, ws_addr=ws_addr)
        cls.scrapedData[cls.id] = []
        cls.id += 1
        return (cls.id - 1, ws_addr)

    @classmethod
    async def updatePage(cls, id: int, state: PageState) -> bool:
        if not await cls.idCheck(id):
            return False
        cls.pages[id].state = state
        return True

    @classmethod
    async def updateScrapeStatus(cls, id: int, status: bool) -> bool:
        if not await cls.idCheck(id):
            return False
        cls.pages[id].state.scrape = status
        return True

    @classmethod
    async def getPage(cls, id: int) -> tuple[Page, PageState, int]:
        if id < 0 or id > cls.id:
            print(f"illegal id, recieved {id}")
        return (cls.pages[id].page, cls.pages[id].state, cls.pages[id].ws_addr)

    @classmethod
    async def getPageByWs_addr(cls, ws_addr: int) -> PageState | None:
        for idx in cls.pages:
            if cls.pages[idx].ws_addr == ws_addr:
                return cls.pages[idx].state
        return None

    @classmethod
    async def getIdByWs_addr(cls, ws_addr: int) -> int | None:
        for idx in cls.pages:
            if cls.pages[idx].ws_addr == ws_addr:
                return idx
        return None

    @classmethod
    async def clear(cls) -> None:
        cls.id = 0
        cls.pages = {}
        return

    @classmethod
    async def idCheck(cls, id: int) -> bool:
        if id < 0 or id > cls.id:
            print(f"Illegal id, recieved {id}")
            return False
        return True


appstate = AppState()
pagestate = PageState()
