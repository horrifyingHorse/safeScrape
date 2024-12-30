import asyncio

from dotenv import load_dotenv

from server.host import serveServer
from service.browser_controls import newPage
from service.controls import BrowserManager, PageState, appstate

_ = load_dotenv()


async def run(state: PageState):
    while appstate.status:
        if not state.execute:
            continue
        page = await newPage(await BrowserManager.getBrowser(), state)

        # page.on("request", displayUrl)

        # _ = await page.goto("localhost:8000/discord.html")
        # _ = await page.goto("https://instagram.com/")
        # _ = await page.goto("https://discord.com/channels/@me")

        # _ = await asyncio.gather(pageSeeker(page), handle())
        # _ = await asyncio.gather(scrapeInstagram(page))

        await page.pause()


async def main():
    # async with async_playwright() as playwright:
    #     # await run(playwright)
    #     return
    _ = await BrowserManager.getBrowser()
    _ = await asyncio.gather(serveServer())


if __name__ == "__main__":
    asyncio.run(main())
