from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .snapd import SnapdClient

class Snap(BaseModel):
    name: str

app = FastAPI()
snap_client = SnapdClient()

origins = [
    "http://localhost",
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/refresh")
def refresh():
    response = snap_client.refresh()
    return response


@app.post("/revert")
def revert(snap: Snap):
    print (snap.name)
    response = snap_client.revert(snap.name)
    return response

