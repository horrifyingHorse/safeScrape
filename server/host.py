import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from playwright.async_api import Page
from pydantic import BaseModel
from uvicorn.config import Config
from uvicorn.server import Server

from service.browser_controls import newPage
from service.controls import BrowserManager, PageManager, PageState, appstate


class getAppStateSchema(BaseModel):
    serviceIndex: int
    storageState: str
    contextURL: str
    autoLogIn: bool


class setStatusSchema(BaseModel):
    status: bool


class updatePageStateSchema(BaseModel):
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
    if not data.status:
        await BrowserManager.killBrowser()
    return {"success": True}


@app.post("/api/appstate")
async def newState(data: getAppStateSchema):
    pageState = PageState()
    pageState.service = appstate.services[data.serviceIndex]
    pageState.storage_state = data.storageState
    pageState.custom_url = data.contextURL
    pageState.auto_login = data.autoLogIn
    page: Page = await newPage(await BrowserManager.getBrowser(), pageState)
    id: int = await PageManager.addPage(page, pageState)
    return {"id": id, "pageState": pageState}


@app.post("/api/pagestate/update")
async def updatePageState(data: updatePageStateSchema):
    _ = await PageManager.updatePage(data.id, data.pageState)
    return {"success": True}


@app.get("/api/appstate")
async def getState(id: int):
    data: tuple[Page, PageState] = await PageManager.getPage(id)

    return {"id": id, "pageState": data[1]}


@app.get("/api/appstate/service")
async def handleServices():
    return {"service": appstate.services}


@app.get("/api/appstate/storagestate")
async def handleStorageState():
    storageStateFiles: list[str] = []
    for _, _, files in os.walk("./state"):
        for file in files:
            if file[-6:] == ".state":
                storageStateFiles.append(file)
    return {"storageState": storageStateFiles}


app.mount("/", StaticFiles(directory="./dist/", html=True), name="static")


async def serveServer():
    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    await server.serve()
