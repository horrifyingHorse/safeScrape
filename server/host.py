import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from playwright.async_api import Browser, Page
from pydantic import BaseModel
from uvicorn.config import Config
from uvicorn.server import Server

from service.browser_controls import newPage, saveStorageState
from service.controls import BrowserManager, PageManager, PageState, appstate


class getAppStateSchema(BaseModel):
    serviceIndex: int
    newStorageState: bool
    storageState: str
    contextURL: str
    autoLogIn: bool


class setStatusSchema(BaseModel):
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
        page: Page = await newPage(browser, pageState)
        id = await PageManager.addPage(page, pageState)
        return {
            "success": True,
            "data": {"id": id, "pageState": pageState},
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
        pageInfo: tuple[Page, PageState] = await PageManager.getPage(data.id)
        _ = await saveStorageState(pageInfo[0], pageInfo[1])
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        errMsg = f"Error while storin State: " + str(e)
        return {"success": False, "data": None, "error": errMsg}


@app.get("/api/appstate")
async def getState(id: int):
    data: tuple[Page, PageState] = await PageManager.getPage(id)
    return {"success": True, "data": {"id": id, "pageState": data[1]}, "error": None}


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
