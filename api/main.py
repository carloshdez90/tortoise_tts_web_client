import os
from typing import Union, Optional
from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helper.tts import get_voices, get_quality, get_candidates, get_audios, generate_tts
from helper.bucket import get_folder_list, generate_download_signed_urls
from helper.sso import validate_token
from models import TTSParams

# declarations
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './bucket-service-account.json'

# Utility methods


def folders(prefix: Union[str, None] = None):
    folder_list = get_folder_list(prefix)
    return dict(zip(folder_list, folder_list))

# Endpoints


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, folder: Union[str, None] = None):
    params = {
        "request": request,
        "voices": get_voices(),
        "quality_list": get_quality(),
        "candidates": get_candidates(),
        "audios": get_audios()
    }

    if folder is not None:
        params['object_list'] = generate_download_signed_urls(
            get_folder_list(folder))

    return templates.TemplateResponse("index.html", params)


@app.post("/do-tts")
async def do_tts(request: Request, item: TTSParams):

    # if api_mode:
    #     # validate if the provided token is valid
    #     try:
    #         response = validate_token(token)
    #     except:
    #         raise HTTPException(
    #             status_code=400, detail="Invalid provided token")

    #     if response.status_code != 200 or dict(response.json())['active'] == False:
    #         raise HTTPException(
    #             status_code=400, detail="Invalid provided token")

    url = app.url_path_for("index")
    response = generate_tts(item.voice,
                            item.text,
                            preset=item.quality,
                            candidates=item.candidate)

    if item.api_mode:
        return generate_download_signed_urls(get_folder_list(response['folder']))
    else:
        return RedirectResponse(f"{url}?folder={response['folder']}", status_code=status.HTTP_303_SEE_OTHER)
