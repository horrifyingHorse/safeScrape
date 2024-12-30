import asyncio
import json
import os

from bs4 import BeautifulSoup
from playwright.async_api import Locator, Page

from .delay import human_like_delay


async def loginDiscord(page: Page):
    _ = await page.goto("https://discord.com/login/")

    await page.locator('input[name="email"][type="text"]').fill(
        f"{os.getenv("DISCORD_USERNAME")}"
    )
    await human_like_delay()
    await page.locator('input[name="password"][type="password"]').fill(
        f"{os.getenv("DISCORD_PASSWORD")}"
    )
    await human_like_delay()

    button = page.locator('button[type="submit"]')
    await button.hover()
    await human_like_delay()
    await button.click()
    await human_like_delay()

    print("Complete 2FA")
    await page.pause()
    _ = await page.context.storage_state(path="discord_state.session")
    await page.close()
    return


async def scrapeDiscord(page: Page):
    locators = {
        "username": 'span[class="username_f9f2ca desaturateUserColors_c7819f clickable_f9f2ca"]',
        "timestamp": 'span[class="timestamp_f9f2ca timestampInline_f9f2ca"] time',
        "content": 'div[class="markup_f8f345 messageContent_f9f2ca"]',
        "mentionedContent": 'div[class="repliedTextContent_f9f2ca markup_f8f345 messageContent_f9f2ca"]',
        "emojiWrapper": 'span[class="emojiContainer_bae8cb emojiContainerClickable_bae8cb"] img]',
    }

    async def getDetails(
        div: Locator, fresh: bool = False, details: dict[str, str] | None = None
    ) -> dict[str, str]:

        username = ""
        timeStamp = ""
        if not fresh and details:
            username = details["username"]
            timeStamp = await div.locator(
                'span[class="latin12CompactTimeStamp_f9f2ca timestamp_f9f2ca timestampVisibleOnHover_f9f2ca alt_f9f2ca"]'
            ).inner_text(timeout=5000)
        else:
            username = await div.locator(locators["username"]).inner_text(timeout=5000)
            timeStamp = (
                await div.locator(locators["timestamp"]).inner_text(timeout=5000)
            )[3:]
        contentDiv = div.locator(locators["content"])
        msgID = await contentDiv.get_attribute("id")
        content = await contentDiv.inner_text(timeout=5000)
        soup = BeautifulSoup(await contentDiv.inner_html(timeout=5000), "html.parser")
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

    async def getMentioned(div: Locator) -> dict[str, str]:
        mentionedContext = div.locator('div[class~="repliedMessage_f9f2ca"]')
        mentionedUser = await mentionedContext.locator(locators["username"]).inner_text(
            timeout=5000
        )
        mentionedContentDiv = mentionedContext.locator(locators["mentionedContent"])
        mentionedMsgID = await mentionedContentDiv.get_attribute("id")
        return {
            "mentionedMsgID": f"{mentionedMsgID}",
            "mentionedUser": mentionedUser,
            "mentionedContent": await mentionedContentDiv.inner_text(timeout=5000),
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
        await asyncio.sleep(0.25)
        trackChanges = False
        divs = page.locator(
            'div[class~="message_d5deea"][class~="cozyMessage_d5deea"][class~="wrapper_f9f2ca"][class~="cozy_f9f2ca"][class~="zalgo_f9f2ca"]'
            # [class~="groupStart_d5deea"] -> optional, only for start of a msg by same user
            # 'mentioned_d5deea hasReply_f9f2ca' -> when mentioned/replied
            # 'hasThread_f9f2ca isSystemMessage_f9f2ca' -> skip
        )

        divCount = await divs.count()
        # print(divCount)
        for i in range(divCount):
            div = divs.nth(i)
            boundingBox = await div.bounding_box()
            if not boundingBox:
                continue
            # Avoid interacting with elements outside viewport
            if (
                page.viewport_size
                and boundingBox["y"] > page.viewport_size["height"]
                or boundingBox["y"] < 0
            ):
                continue

            if "hasThread_f9f2ca" in (await div.get_attribute("class") or ""):
                continue

            mentioned = {
                "mentionedMsgID": "",
                "mentionedUser": "",
                "mentionedContent": "",
            }
            try:
                if "hasReply_f9f2ca" in (await div.get_attribute("class") or ""):
                    mentioned = await getMentioned(div)
                details = await getDetails(
                    div.locator('div[class="contents_f9f2ca"]'),
                    "groupStart_d5deea" in (await div.get_attribute("class") or ""),
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
