from playwright.async_api import Browser, BrowserContext, Page

from service.controls import PageState
from service.delay import human_like_delay
from service.discord import loginDiscord
from service.github import loginGithub
from service.instagram import loginInstagram

# async def launchBrowser() -> Browser:
#     global browser, playright_instance
#     print(browser, "what?")
#     if browser != None:
#         return browser
#
#     playright_instance = await async_playwright().start()
#     browser = await playright_instance.chromium.launch(headless=False)
#     print(browser, "what?2")
#     return browser


async def newContext(browser: Browser, state: PageState) -> BrowserContext:
    return await browser.new_context(
        viewport={"width": 1366, "height": 768},
        locale="en-IN",
        timezone_id="Asia/Kolkata",
        geolocation={
            "latitude": 21.1458,
            "longitude": 79.0882,
        },
        permissions=["geolocation"],
        color_scheme="dark",
        storage_state=f"./state/{state.storage_state}",
        # storage_state="instagram_state.session",
        # storage_state="discord_state.session",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    )


async def loginRouter(page: Page, state: PageState):
    if state.service == "github.com":
        await loginGithub(page)
    elif state.service == "discord.com":
        await loginDiscord(page)
    else:
        await loginInstagram(page)
    return


async def newPage(browser: Browser, state: PageState) -> Page:
    context: BrowserContext = await newContext(browser, state)
    page: Page = await context.new_page()
    if state.auto_login:
        await loginRouter(page, state)
    await human_like_delay() if state.allow_delay else None
    if state.custom_url == "":
        _ = await page.goto(f"https://{state.service}/")
    else:
        _ = await page.goto(state.custom_url)

    return page
