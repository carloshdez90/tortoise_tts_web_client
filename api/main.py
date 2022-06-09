import os
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helper.tts import get_voices, get_quality, get_candidates
from helper.bucket import get_folder_list

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './bucket-service-account.json'


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request, "id": 7})

@app.get("/voices")
def voices():
    print(get_voices())
    voices = get_voices()
    return dict(zip(voices, voices))

@app.get("/quality")
def quality():
    quality = get_quality()
    return dict(zip(quality, quality))

@app.get("/candidates")
def candidates():
    return {"candidates": get_candidates()}

@app.get("/folders")
def folders(prefix: Union[str, None] = None):
    folder_list = get_folder_list(prefix)
    return dict(zip(folder_list, folder_list))