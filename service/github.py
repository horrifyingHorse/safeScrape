import os

from playwright.async_api import Page

from .delay import human_like_delay


async def loginGithub(page: Page):
    _ = await page.goto("https://github.com/login")

    await page.locator("#login_field").fill(f"{os.getenv("GITHUB_USERNAME")}")
    await page.locator("#password").fill(f"{os.getenv("GITHUB_PASSWORD")}")
    await human_like_delay()

    button = page.locator('input[type="submit"][name="commit"]')
    await button.hover()
    await human_like_delay()
    await button.click()

    print("Complete 2FA")
    _ = await page.pause()
    _ = await page.context.storage_state(path="./states/github_state.session")
    await page.close()
    return
