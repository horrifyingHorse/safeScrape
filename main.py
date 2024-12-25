import os
import random
import time

from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page, Request, sync_playwright

# from playwright_stealth import stealth_sync

_ = load_dotenv()


def human_like_delay(min_time: float = 0.5, max_time: float = 3.5):
    """Simulate human-like random delays."""
    time.sleep(random.uniform(min_time, max_time))


def displayUrl(request: Request):
    print(request.url)


def githubLogin(context: BrowserContext):
    # One time login
    page = context.new_page()
    # stealth_sync(page)
    _ = page.goto("https://github.com/login")

    page.locator("#login_field").fill(f"{os.getenv("GITHUB_USERNAME")}")
    page.locator("#password").fill(f"{os.getenv("GITHUB_PASSWORD")}")

    human_like_delay()  # Delay before finding the button

    button = page.locator('input[type="submit"][name="commit"]')

    button.hover()
    human_like_delay()  # Delay before clicking

    button.click()

    print("Complete 2FA")
    try:
        while True:
            time.sleep(1)  # Prevent high CPU usage
            _ = context.storage_state(path="github_state.session")
    except KeyboardInterrupt:
        print("\nReturning from github login..")
    finally:
        page.close()

    return


def instagramLogin(context: BrowserContext):
    page = context.new_page()
    # stealth_sync(page)
    _ = page.goto("https://instagram.com/")

    page.locator('input[type="text"][name="username"]').fill(
        f"{os.getenv("INSTAGRAM_USERNAME")}"
    )

    page.locator('input[type="password"][name="password"]').fill(
        f"{os.getenv("INSTAGRAM_PASSWORD")}"
    )

    button = page.locator('button[type="submit"]')

    human_like_delay()  # Delay before finding the button
    button.hover()

    human_like_delay()  # Delay before finding the button
    button.click()

    print("Complete 2FA")
    try:
        while True:
            time.sleep(1)  # Prevent high CPU usage
            _ = context.storage_state(path="instagram_state.session")
    except KeyboardInterrupt:
        print("\nReturning from instagram login..")
    finally:
        page.close()

    return


def getAllMsgs(page: Page):
    uniqMsgs = {}
    _ = input("Start?")

    print("\nlistenin msgs")
    msgID: int = 0
    replyID: int = -1
    while True:
        time.sleep(1)

        divs = page.locator(
            'div[class*="html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a"]'
        ).or_(page.locator('div[class="x5n08af x1f6kntn x1btupbp x1mzt3pk"]'))

        divCount = divs.count()

        for i in range(divCount):
            author = ""
            div = divs.nth(i)

            if not div.is_visible():
                break

            msg = div.inner_text(timeout=5000)

            if "x18lvrbx" in (div.get_attribute("class") or ""):
                author = "palubhai"
            elif "xyk4ms5" in (div.get_attribute("class") or ""):
                author = "prompter"
            else:
                replyID = uniqMsgs[msg]["msgID"]

            if msg in uniqMsgs:
                continue

            uniqMsgs[msg] = {
                "msgID": msgID,
                "author": author,
                "replyID": replyID,
                "content": msg,
            }

            print(f"[{msgID}]\t{author}\t[{replyID}]\t {msg}")

            replyID = -1
            msgID += 1


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        color_scheme="dark",
        storage_state="instagram_state.session",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    )
    page = context.new_page()

    # page.on("request", displayUrl)

    # _ = page.goto("localhost:8000/index.html")
    _ = page.goto("https://instagram.com/")

    getAllMsgs(page)

    # chillyDawg: https://www.instagram.com/direct/t/17846189409278954/

    # githubLogin(context)
    # instagramLogin(context)

    print(page.title())

    try:
        while True:
            time.sleep(1)  # Prevent high CPU usage
    except KeyboardInterrupt:
        print("\nClosing the browser...")
    finally:
        browser.close()
