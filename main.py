import json
import os
import random
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Locator, Page, Request, sync_playwright

# from playwright_stealth import stealth_sync

_ = load_dotenv()


def human_like_delay(min_time: float = 0.5, max_time: float = 3.5):
    """Simulate human-like random delays."""
    time.sleep(random.uniform(min_time, max_time))


def displayUrl(request: Request):
    print(request.url)


def githubLogin(context: BrowserContext):
    page = context.new_page()
    _ = page.goto("https://github.com/login")

    page.locator("#login_field").fill(f"{os.getenv("GITHUB_USERNAME")}")
    page.locator("#password").fill(f"{os.getenv("GITHUB_PASSWORD")}")
    human_like_delay()

    button = page.locator('input[type="submit"][name="commit"]')
    button.hover()
    human_like_delay()
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

    human_like_delay()
    button.hover()
    human_like_delay()
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


def discordLogin(context: BrowserContext):
    page = context.new_page()
    _ = page.goto("https://discord.com/login/")

    page.locator('input[name="email"][type="text"]').fill(
        f"{os.getenv("DISCORD_USERNAME")}"
    )
    human_like_delay()
    page.locator('input[name="password"][type="password"]').fill(
        f"{os.getenv("DISCORD_PASSWORD")}"
    )
    human_like_delay()

    button = page.locator('button[type="submit"]')
    button.hover()
    human_like_delay()
    button.click()
    human_like_delay()

    print("Complete 2FA")
    try:
        while True:
            time.sleep(1)  # Prevent high CPU usage
            _ = context.storage_state(path="discord_state.session")
    except KeyboardInterrupt:
        print("\nReturning from instagram login..")
    finally:
        page.close()

    return


def scrapeDiscord(page: Page):
    locators = {
        "username": 'span[class="username_f9f2ca desaturateUserColors_c7819f clickable_f9f2ca"]',
        "timestamp": 'span[class="timestamp_f9f2ca timestampInline_f9f2ca"] time',
        "content": 'div[class="markup_f8f345 messageContent_f9f2ca"]',
        "mentionedContent": 'div[class="repliedTextContent_f9f2ca markup_f8f345 messageContent_f9f2ca"]',
        "emojiWrapper": 'span[class="emojiContainer_bae8cb emojiContainerClickable_bae8cb"] img]',
    }

    def getDetails(
        div: Locator, fresh: bool = False, details: dict[str, str] | None = None
    ) -> dict[str, str]:
        username = ""
        timeStamp = ""

        if not fresh and details:
            username = details["username"]
            timeStamp = div.locator(
                'span[class="latin12CompactTimeStamp_f9f2ca timestamp_f9f2ca timestampVisibleOnHover_f9f2ca alt_f9f2ca"]'
            ).inner_text(timeout=5000)
        else:
            username = div.locator(locators["username"]).inner_text(timeout=5000)
            timeStamp = div.locator(locators["timestamp"]).inner_text(timeout=5000)[3:]

        contentDiv = div.locator(locators["content"])
        msgID = contentDiv.get_attribute("id")
        content = contentDiv.inner_text(timeout=5000)
        soup = BeautifulSoup(contentDiv.inner_html(timeout=5000), "html.parser")
        if soup.find_all("img"):
            for imgTag in soup.find_all("img"):
                emoji = imgTag.get("alt", "")
                imgTag.replace_with(emoji)
            content = " ".join(soup.get_text(separator=" ").split())

        return {
            "username": username,
            "timeStamp": timeStamp,
            "content": content,
            "msgID": f"{msgID}",
        }

    def getMentioned(div: Locator) -> dict[str, str]:
        mentionedContext = div.locator('div[class~="repliedMessage_f9f2ca"]')
        mentionedUser = mentionedContext.locator(locators["username"]).inner_text(
            timeout=5000
        )
        mentionedContentDiv = mentionedContext.locator(locators["mentionedContent"])
        mentionedMsgID = mentionedContentDiv.get_attribute("id")
        return {
            "mentionedMsgID": f"{mentionedMsgID}",
            "mentionedUser": mentionedUser,
            "mentionedContent": mentionedContentDiv.inner_text(timeout=5000),
        }

    details = {
        "username": "",
        "timeStamp": "",
        "content": "",
        "msgID": "",
    }
    uniqMsgs = {}
    _ = input("Begin?")

    while True:
        time.sleep(0.25)
        trackChanges = False
        divs = page.locator(
            'div[class~="message_d5deea"][class~="cozyMessage_d5deea"][class~="wrapper_f9f2ca"][class~="cozy_f9f2ca"][class~="zalgo_f9f2ca"]'
            # [class~="groupStart_d5deea"] -> optional, only for start of a msg by same user
            # 'mentioned_d5deea hasReply_f9f2ca' -> when mentioned/replied
            # 'hasThread_f9f2ca isSystemMessage_f9f2ca' -> skip
        )

        divCount = divs.count()
        # print(divCount)
        for i in range(divCount):
            div = divs.nth(i)
            boundingBox = div.bounding_box()
            if not boundingBox:
                continue
            # Avoid interacting with elements outside viewport
            if (
                page.viewport_size
                and boundingBox["y"] > page.viewport_size["height"]
                or boundingBox["y"] < 0
            ):
                continue

            if "hasThread_f9f2ca" in (div.get_attribute("class") or ""):
                continue

            mentioned = {
                "mentionedMsgID": "",
                "mentionedUser": "",
                "mentionedContent": "",
            }
            try:
                if "hasReply_f9f2ca" in (div.get_attribute("class") or ""):
                    mentioned = getMentioned(div)
                details = getDetails(
                    div.locator('div[class="contents_f9f2ca"]'),
                    "groupStart_d5deea" in (div.get_attribute("class") or ""),
                    details,
                )
                if details["msgID"] in uniqMsgs:
                    continue

            except:
                print(f"skipping: {i}th div")
                print("---------\n", div, "\n--------\n")
                continue

            trackChanges = True
            uniqMsgs[details["msgID"]] = {
                "msgID": f"{details["msgID"]}",
                "replyID": f"{mentioned["mentionedMsgID"]}",
                "timestamp": f"{details["timeStamp"]}",
                "author": details["username"],
                "content": details["content"],
            }
            if mentioned["mentionedMsgID"] != "":
                print(
                    f"{mentioned["mentionedUser"]}:{mentioned['mentionedMsgID']}\t\t{mentioned["mentionedContent"]}"
                )
            print(
                f"div no:{i}\t[{details["msgID"]}]\t{details["username"]}\t{details["timeStamp"]}\n\t{details["content"]}\n"
            )

        if not trackChanges:
            continue
        exportJson = json.dumps(uniqMsgs)
        with open("msgs.json", "w") as f:
            _ = f.write(exportJson)
            f.close()


def scrapeInstagram(page: Page):
    uniqMsgs = {}
    _ = input("Start?")

    print("\nlistenin msgs")
    msgID: int = 0
    replyID = ""
    while True:
        time.sleep(0.5)
        divs = page.locator(
            'div[class*="html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a"]'
        ).or_(page.locator('div[class="x5n08af x1f6kntn x1btupbp x1mzt3pk"]'))

        divCount = divs.count()
        for i in range(divCount):
            author = ""
            div = divs.nth(i)

            bounding_box = div.bounding_box()
            if not bounding_box:
                continue

            # Avoid interacting with elements outside viewport
            if (
                page.viewport_size
                and bounding_box["y"] > page.viewport_size["height"]
                or bounding_box["y"] < 0
            ):
                continue

            msg = div.inner_text(timeout=5000)
            if "x18lvrbx" in (div.get_attribute("class") or ""):
                author = "palubhai"
            elif "xyk4ms5" in (div.get_attribute("class") or ""):
                author = "prompter"
            else:
                replyID = uniqMsgs[msg]["msgID"]

            if msg in uniqMsgs and replyID == "":
                continue

            uniqMsgs[msg] = {
                "msgID": f"I{msgID}",
                "author": author,
                "replyID": replyID,
                "content": msg,
            }

            print(f"[I{msgID}]\t\t{author}\t\t[{replyID}]\t\t{msg}")

            replyID = ""
            msgID += 1


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
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
        storage_state="discord_state.session",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    )
    page = context.new_page()

    # page.on("request", displayUrl)

    # _ = page.goto("localhost:8000/discord.html")
    # _ = page.goto("https://instagram.com/")
    _ = page.goto("https://discord.com/channels/@me")

    scrapeDiscord(page)

    # discordLogin(context)

    # scrapeInstagram(page)

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
