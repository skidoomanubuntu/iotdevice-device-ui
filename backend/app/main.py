from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool
from requests.adapters import HTTPAdapter
import requests, socket, pprint, json as js
import os

app = FastAPI()

class SnapdConnection(HTTPConnection):
    def __init__(self):
        super().__init__("localhost")

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect("/run/snapd.socket")


class SnapdConnectionPool(HTTPConnectionPool):
    def __init__(self):
        super().__init__("localhost")

    def _new_conn(self):
        return SnapdConnection()


class SnapdAdapter(HTTPAdapter):
    def get_connection(self, url, proxies=None):
        return SnapdConnectionPool()

@app.get("/revert")
def revert():
    session = requests.Session()
    session.mount("http://snapd/", SnapdAdapter())
    response = session.post("http://snapd/v2/snaps/dashboard-controller", data = js.dumps({"action": "revert"}) )
    pprint.pprint(response.json())
    return response.json()

@app.get("/update/{color}")
def update(color: str):
   #command = 'sudo curl -sS --unix-socket /run/snapd.socket -H "Content-type: multipart/form-data" -F filename=controller-%s.snap -F snap="@controller-%s.snap" -F dangerous="true"   http://localhost/v2/snaps' % (color, color)
   session = requests.Session()
   session.mount("http://snapd/", SnapdAdapter())
   print (os.getcwd())
   response = session.post("http://snapd/v2/snaps", files=dict(filename='/var/snap/dashboard-ui/common/controller-%s.snap' % color, snap=open('/var/snap/dashboard-ui/common/controller-%s.snap' % color, 'rb')), data={"dangerous":"true"} )
   pprint.pprint(response.json())
   return response.json()

'''from fastapi import FastAPI
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


@app.get("/revert")
def revert():
    #print (snap.name)
    #response = snap_client.revert(snap.name)
    print ('made it here')
    response = snap_client.revert("iotdevice-device-controller")
    return response
'''
