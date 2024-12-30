import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from uvicorn.config import Config
from uvicorn.server import Server

from service.browser_controls import newPage
from service.controls import BrowserManager, PageState, appstate


class getAppState(BaseModel):
    serviceIndex: int
    storageState: str
    contextURL: str
    autoLogIn: bool


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/appstate")
async def startNew(data: getAppState):
    pageState = PageState()
    pageState.service = appstate.services[data.serviceIndex]
    pageState.storage_state = data.storageState
    pageState.custom_url = data.contextURL
    pageState.auto_login = data.autoLogIn

    _ = await newPage(await BrowserManager.getBrowser(), pageState)

    return pageState


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
