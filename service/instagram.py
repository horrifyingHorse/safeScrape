import asyncio
import os

from playwright.async_api import Page

from service.controls import pagestate
from service.delay import human_like_delay


async def loginInstagram(page: Page):
    _ = await page.goto("https://instagram.com/")

    await page.locator('input[type="text"][name="username"]').fill(
        f"{os.getenv("INSTAGRAM_USERNAME")}"
    )
    await page.locator('input[type="password"][name="password"]').fill(
        f"{os.getenv("INSTAGRAM_PASSWORD")}"
    )

    button = page.locator('button[type="submit"]')

    await human_like_delay() if pagestate.allow_delay else None
    await button.hover()
    await human_like_delay() if pagestate.allow_delay else None
    await button.click()

    print("Complete 2FA")
    await page.pause()
    _ = await page.context.storage_state(path="instagram_state.session")
    await page.close()
    return


async def scrapeInstagram(page: Page):
    uniqMsgs = {}
    _ = input("Start?")

    print("\nlistenin msgs")
    msgID: int = 0
    while True:
        replyID = ""
        await asyncio.sleep(0.5)
        divs = page.locator(
            'div[class*="html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a"]'
        ).or_(page.locator('div[class="x5n08af x1f6kntn x1btupbp x1mzt3pk"]'))

        divCount = await divs.count()
        for i in range(divCount):
            author = ""
            div = divs.nth(i)

            bounding_box = await div.bounding_box()
            if not bounding_box:
                continue

            # Avoid interacting with elements outside viewport
            if (
                page.viewport_size
                and bounding_box["y"] > page.viewport_size["height"]
                or bounding_box["y"] < 0
            ):
                continue

            msg = await div.inner_text(timeout=5000)
            if "x18lvrbx" in (await div.get_attribute("class") or ""):
                author = "palubhai"
            elif "xyk4ms5" in (await div.get_attribute("class") or ""):
                author = "prompter"
            else:
                replyID = uniqMsgs.get(msg, {}).get("msgID", "")

            if msg in uniqMsgs and replyID == "":
                continue

            uniqMsgs[msg] = {
                "msgID": f"I{msgID}",
                "author": author,
                "replyID": replyID if author == "" else "",
                "content": msg,
            }

            print(f"[I{msgID}]\t\t{author}\t\t[{replyID}]\t\t{msg}")

            msgID += 1
