import asyncio
import os

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from playwright.async_api import Browser, Page
from pydantic import BaseModel
from uvicorn.config import Config
from uvicorn.server import Server

from service.browser_controls import newPage, saveStorageState
from service.controls import BrowserManager, PageManager, PageState, appstate
from service.instagram import scrapeInstagram


class getAppStateSchema(BaseModel):
    serviceIndex: int
    newStorageState: bool
    storageState: str
    contextURL: str
    autoLogIn: bool


class setStatusSchema(BaseModel):
    status: bool


class ScrapeStatusSchema(BaseModel):
    id: int
    status: bool


class PageStateSchema(BaseModel):
    id: int
    pageState: PageState


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/socky")
async def tests(ws: WebSocket):
    await ws.accept()
    return


@app.websocket("/scrapy/{ws_addr}")
async def consoleConnect(ws: WebSocket, ws_addr: int):
    await ws.accept()
    await ws.send_json([{"status": f"Connection was made with ws_addr#{ws_addr}"}])
    state: PageState | None = await PageManager.getPageByWs_addr(ws_addr)
    if not state:
        print("No state thus returnin")
        return
    id: int | None = await PageManager.getIdByWs_addr(ws_addr)
    if id == None:
        print("No id thus returnin:", id)
        return
    await ws.send_json([{"status": "ws fine"}])
    while True:
        print("ws pollin")
        newMsgs: int = await PageManager.pollData(id)
        data = PageManager.scrapedData[id]
        await ws.send_json([d.model_dump() for d in data[-newMsgs:]])
        print("sent: ", data)


@app.post("/api/appstate/status")
async def setStatus(data: setStatusSchema):
    result: tuple[bool, str] = (False, "")
    if not data.status:
        result = await BrowserManager.killBrowser()
    return {"success": result[0], "data": None, "error": result[1]}


@app.post("/api/appstate")
async def newState(data: getAppStateSchema):
    pageState = PageState()
    pageState.service = appstate.services[data.serviceIndex]
    pageState.new_state = data.newStorageState
    pageState.storage_state = data.storageState
    pageState.custom_url = data.contextURL
    pageState.auto_login = data.autoLogIn
    id: int = -1
    errMsg: str = ""
    try:
        browser: Browser = await BrowserManager.getBrowser()
        print("Bowser")
        page: Page = await newPage(browser, pageState)
        print("Page")
        id, ws_addr = await PageManager.addPage(page, pageState)
        print("Page added")
        return {
            "success": True,
            "data": {"id": id, "pageState": pageState, "ws_addr": ws_addr},
            "error": None,
        }
    except Exception as e:
        errMsg = "Error while launching newPage: " + str(e)
        return {"success": False, "data": None, "error": errMsg}


@app.post("/api/pagestate/update")
async def updatePageState(data: PageStateSchema):
    try:
        _ = await PageManager.updatePage(data.id, data.pageState)
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        errMsg = f"Error while updating Page(#{data.id}) State: " + str(e)
        return {"success": False, "data": None, "error": errMsg}


@app.post("/api/pagestate/savestoragestate")
async def saveState(data: PageStateSchema):
    try:
        page, pageState, _ = await PageManager.getPage(data.id)
        _ = await saveStorageState(page, pageState)
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        errMsg = f"Error while storin State: " + str(e)
        return {"success": False, "data": None, "error": errMsg}


@app.post("/api/pagestate/scrape")
async def scrapeStatus(data: ScrapeStatusSchema):
    if data.status:
        page, state, _ = await PageManager.getPage(data.id)
        if state.service == "instagram.com":
            print("Ordered Scrapin")
            _ = asyncio.create_task(scrapeInstagram(data.id, page))
    _ = await PageManager.updateScrapeStatus(data.id, data.status)
    return {"success": True, "data": None, "error": None}


@app.get("/api/appstate")
async def getState(id: int):
    _, pageState, ws_addr = await PageManager.getPage(id)
    return {
        "success": True,
        "data": {"id": id, "pageState": pageState, "ws_addr": ws_addr},
        "error": None,
    }


@app.get("/api/appstate/service")
async def handleServices():
    return {"success": True, "data": {"service": appstate.services}, "error": None}


@app.get("/api/appstate/storagestate")
async def handleStorageState():
    storageStateFiles: list[str] = []
    for _, _, files in os.walk("./state"):
        for file in files:
            if file[-6:] == ".state":
                storageStateFiles.append(file)
    return {"success": True, "data": {"storageState": storageStateFiles}, "error": None}


app.mount("/", StaticFiles(directory="./dist/", html=True), name="static")


async def serveServer():
    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    await server.serve()
