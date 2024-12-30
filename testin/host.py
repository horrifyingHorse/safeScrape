import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class Demo(BaseModel):
    rec: bool


class getAppState(BaseModel):
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

    return {"status": True}


@app.get("/api/appstate/storagestate")
async def handleStorageState():
    storageStateFiles: list[str] = []
    for _, _, files in os.walk("./state"):
        for file in files:
            if file[-6:] == ".state":
                storageStateFiles.append(file)

    return {"storageState": storageStateFiles}


@app.post("/api/send")
async def send(data: Demo):
    return {"state set to": data.rec}


app.mount("/", StaticFiles(directory="./dist/", html=True), name="static")
