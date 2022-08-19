from typing import Union
from pydantic import BaseModel


class TTSParams(BaseModel):
    voice: str
    text: str
    quality: str
    candidate: Union[int, None] = 1
    api_mode: Union[bool, None] = True
    token: Union[str, None] = None
