from typing import Annotated
from fastapi import UploadFile, File

from pydantic import BaseModel


class EnQueueBody(BaseModel):
    video: Annotated[UploadFile, File()]
