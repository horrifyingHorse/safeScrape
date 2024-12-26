import asyncio

from dotenv import load_dotenv
from playwright.async_api import Playwright, Request, async_playwright

from service.delay import human_like_delay
from service.discord import loginDiscord, scrapeDiscord
from service.github import loginGithub
from service.instagram import loginInstagram, scrapeInstagram

# from playwright_stealth import stealth_sync

_ = load_dotenv()


async def displayUrl(request: Request):
    print(request.url)


async def run(playwright: Playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        viewport={"width": 1366, "height": 768},
        locale="en-IN",
        timezone_id="Asia/Kolkata",
        geolocation={
            "latitude": 21.1458,
            "longitude": 79.0882,
        },  # Coordinates for Nagpur
        permissions=["geolocation"],
        color_scheme="dark",
        # storage_state="instagram_state.session",
        # storage_state="discord_state.session",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    )
    page = await context.new_page()

    # page.on("request", displayUrl)

    # _ = await page.goto("localhost:8000/discord.html")
    # _ = await page.goto("https://instagram.com/")
    # _ = await page.goto("https://discord.com/channels/@me")

    await loginInstagram(context)

    # _ = await asyncio.gather(pageSeeker(page), handle())
    _ = await asyncio.gather(scrapeInstagram(page))
    await page.pause()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
